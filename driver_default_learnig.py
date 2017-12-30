from smartcab.agent import LearningAgent
from smartcab.simulator import Simulator
from smartcab.environment import Environment


def reset(self, destination=None, testing=False):
    """ The reset function is called at the beginning of each trial.
        'testing' is set to True if testing trials are being used
        once training trials have completed. """

    # Select the destination as the new location to route to
    self.planner.route_to(destination)

    if not testing:
        # epsilon_{t+1} = epsilon_{t} - 0.05
        self.epsilon -= 0.05
    else:
        self.epsilon = 0
        self.alpha = 0

    # Ensure positive epsilon
    if self.epsilon < 0:
        self.epsilon = 0


def run():
    """ Driving function for running the simulation.
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """


    # Add the reset function to LearningAgent
    LearningAgent.reset = reset

    # Create the environment
    env = Environment(verbose=True)
    # Create the driving agent
    agent = env.create_agent(LearningAgent, learning=True)
    # Follow the driving agent
    env.set_primary_agent(agent, enforce_deadline=True)
    # Create the simulation
    sim = Simulator(env, update_delay=0.0, log_metrics=True)
    # Run the simulator
    sim.run(n_test=10)


if __name__ == '__main__':
    run()

