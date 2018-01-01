from smartcab.agent import LearningAgent
from smartcab.simulator import Simulator
from smartcab.environment import Environment
import random

# Set global random seed
random.seed(42)


def reset(self, destination=None, testing=False):
    """
    The reset function is called at the beginning of each trial.
    'testing' is set to True if testing trials are being used once training
    trials have completed.
    """

    # Select the destination as the new location to route to
    self.planner.route_to(destination)

    ###########
    ## TO DO ##
    ###########
    # Update epsilon using a decay function of your choice
    # Update additional class parameters as needed
    # If 'testing' is True, set epsilon and alpha to 0


def run():
    """
    Driving function for running the simulation.
    Press ESC to close the simulation, or [SPACE] to pause the simulation.
    """

    # Add the reset function to LearningAgent
    LearningAgent.reset = reset

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    # grid_size   - discrete number of intersections (columns, rows), default
    # is (8, 6)
    env = Environment()

    ##############
    # Create the driving agent
    # Flags:
    #   learning - set to True to force the driving agent to use Q-learning
    #   epsilon  - continuous value for the exploration factor, default is 1
    #   alpha    - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent)

    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, update_delay=0.01, log_metrics=True)

    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=10)


if __name__ == '__main__':
    run()

