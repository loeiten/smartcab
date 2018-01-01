import random
from environment import Agent
from planner import RoutePlanner
import numpy as np

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed

        # Initialize the trial variable
        # NOTE: We start at 1 in order to avoid negative powers
        self.t = 1
        random.seed(42)


    def build_state(self):
        """ The build_state function is called when the agent requests data from the
            environment. The next waypoint, the intersection inputs, and the deadline
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ###########
        ## TO DO ##
        ###########

        # NOTE : you are not allowed to engineer eatures outside of the inputs available.
        # Because the aim of this project is to teach Reinforcement Learning, we have placed
        # constraints in order for you to learn how to adjust epsilon and alpha, and thus learn about the balance between exploration and exploitation.
        # With the hand-engineered features, this learning process gets entirely negated.

        # Set 'state' as a tuple of relevant data for the agent
        state = (waypoint, inputs["light"], inputs["left"], inputs["oncoming"])

        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ###########
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        # From https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
        max_value = max(self.Q[state].values())
        maxQ = tuple(key for key in self.Q[state].keys()
                     if np.isclose(self.Q[state][key], max_value))

        if self.env.verbose:
            print("self.Q[state] = {}".format(self.Q[state]))
            print("max_value = {}".format(max_value))
            print("maxQ = {}".format(maxQ))
        return maxQ


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ###########
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        if self.learning:
            if state not in self.Q.keys():
                self.Q[state] = dict()
                for action in self.valid_actions:
                    self.Q[state][action] = 0.0


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        ###########
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        # Otherwise, choose an action with the highest Q-value for the current state
        # Be sure that when choosing an action with highest Q-value that you randomly select between actions that "tie".
        if not(self.learning):
            action = random.choice(self.valid_actions)
        else:
            # Randomly selecting from output states from get_maxQ
            best_action = random.choice(self.get_maxQ(state))

            other_actions = [action for action in self.valid_actions\
                             if action != best_action]
            # Generate the probabilities for the different choices
            # We give the best_action a probability of 1 - epsilon, and the
            # rest epsilon/len(other_actions)
            number_of_actions = len(other_actions)
            probabilities =\
                [float(self.epsilon)/number_of_actions] * number_of_actions
            probabilities.insert(0, 1 - self.epsilon)
            all_actions = other_actions
            all_actions.insert(0, best_action)
            action = np.random.choice(all_actions, size=1, p=probabilities)[0]

            if self.env.verbose:
                print("best_action = {}".format(best_action))
                print("all_actions = {}".format(all_actions))
                print("probabilities  = {}".format(probabilities))
                print("action = {}".format(action))

        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives a reward. This function does not consider future rewards
            when conducting learning. """

        ###########
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')

        if self.learning:
            # Q <- (1-alpha)*Q+alpha*(r+gamma*max(Q_next)) with gamma = 0
            self.Q[state][action] =\
                (1 - self.alpha)*self.Q[state][action]\
                + self.alpha*reward


    def update(self):
        """ The update function is called when a time step is completed in the
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

