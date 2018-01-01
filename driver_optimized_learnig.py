from smartcab.agent import LearningAgent
from smartcab.simulator import Simulator
from smartcab.environment import Environment
import numpy as np
import pathlib


def reset_pot(self, destination=None, testing=False):
    a = 0.99

    # Select the destination as the new location to route to
    self.planner.route_to(destination)

    if not testing:
        self.epsilon = a**self.t
    else:
        self.epsilon = 0
        self.alpha = 0

    self.t += 1


def reset_inv_t(self, destination=None, testing=False):
    # Select the destination as the new location to route to
    self.planner.route_to(destination)

    if not testing:
        self.epsilon = self.t**(-2)
    else:
        self.epsilon = 0
        self.alpha = 0

    self.t += 1


def reset_exp(self, destination=None, testing=False):
    a = 0.01

    # Select the destination as the new location to route to
    self.planner.route_to(destination)

    if not testing:
        self.epsilon = np.exp(-a*self.t)
    else:
        self.epsilon = 0
        self.alpha = 0

    self.t += 1


def reset_cos(self, destination=None, testing=False):
    a = 0.005

    # Select the destination as the new location to route to
    self.planner.route_to(destination)

    if not testing:
        self.epsilon = np.cos(a*self.t)
    else:
        self.epsilon = 0
        self.alpha = 0

    self.t += 1


def reset_sig(self, destination=None, testing=False):
    a = 0.1
    t0 = 150

    # Select the destination as the new location to route to
    self.planner.route_to(destination)

    if not testing:
        self.epsilon = 1.0 - (1.0/(1.0+np.exp(-a*(t-t0))))
    else:
        self.epsilon = 0
        self.alpha = 0

    self.t += 1


def run(name, reset, alpha, tolerance):
    """
    Executes the run

    Parameters
    ----------
    name : str
        Name of the .csv and .txt file.
    reset : function
        The reset function to be used by LearningAgent.
    alpha : float
        The learning rate.
    tolerance : float
        Epsilon tolerance before beginning testing
    """

    # Add the reset function to LearningAgent
    LearningAgent.reset = reset

    # Create the environment
    env = Environment(verbose=False)
    # Create the driving agent
    agent = env.create_agent(LearningAgent, learning=True, alpha=alpha)
    # Follow the driving agent
    env.set_primary_agent(agent, enforce_deadline=True)
    # Create the simulation
    sim = Simulator(env, update_delay=0.01, display=False, log_metrics=True,
                    optimized=True)
    # Run the simulator
    sim.run(tolerance=tolerance, n_test=100)

    # Rename the output files
    logs_dir = pathlib.Path(__file__).parent.joinpath("logs")
    logs_dir.joinpath("sim_improved-learning.csv").\
        rename(logs_dir.joinpath(name + ".csv"))
    logs_dir.joinpath("sim_improved-learning.txt").\
        rename(logs_dir.joinpath(name + ".txt"))


def main():
    """
    The master driver which executes all simulations.
    """

    # Create the parameters to run
    parameters =\
        (
            ("pot_high_alpha", reset_pot, 0.75, 0.05),
            ("pot_low_alpha", reset_pot, 0.25, 0.05),
            ("inv_t_high_alpha", reset_inv_t, 0.75, 1e-5),
            ("inv_t_low_alpha", reset_inv_t, 0.25, 1e-5),
            ("exp_high_alpha", reset_exp, 0.75, 0.05),
            ("exp_low_alpha", reset_exp, 0.25, 0.05),
            ("cos_high_alpha", reset_cos, 0.75, 0.05),
            ("cos_low_alpha", reset_cos, 0.25, 0.05),
            ("sig_high_alpha", reset_sig, 0.75, 0.05),
            ("sig_low_alpha", reset_sig, 0.25, 0.05),
        )

    # Call the run function
    for name, reset, alpha, tolerance in parameters:
        run(name, reset, alpha, tolerance)


if __name__ == '__main__':
    main()

