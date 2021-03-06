import random
import numpy as np
import math
class Robot(object):

    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon0=0.5):

        self.maze = maze
        self.valid_actions = self.maze.valid_actions
        self.state = None
        self.action = None

        # Set Parameters of the Learning Robot
        self.alpha = alpha
        self.gamma = gamma

        self.epsilon0 = epsilon0
        self.epsilon = epsilon0
        self.t = 0
        self.a = math.pi/2/3000
        self.Qtable = {}
        self.reset()

    def reset(self):
        """
        Reset the robot
        """
        self.state = self.sense_state()
        self.create_Qtable_line(self.state)

    def set_status(self, learning=False, testing=False):
        """
        Determine whether the robot is learning its q table, or
        exceuting the testing procedure.
        """
        self.learning = learning
        self.testing = testing

    def update_parameter(self):
        """
        Some of the paramters of the q learning robot can be altered,
        update these parameters when necessary.
        """
        if self.testing:
            # TODO 1. No random choice when testing
            self.epsilon = 0
            pass
        else:
            # TODO 2. Update parameters when learning
            self.epsilon -= 0.01
            self.t += 1
            if self.epsilon <= 0:
                self.epsilon = 0
            else:
                self.epsilon = 0.5*math.cos(self.a * self.t)

        return self.epsilon

    def sense_state(self):
        """
        Get the current state of the robot. In this
        """

        # TODO 3. Return robot's current state
        pos = self.maze.sense_robot()
        return pos

    def create_Qtable_line(self, state):
        """
        Create the qtable with the current state
        """
        # TODO 4. Create qtable with current state
        # Our qtable should be a two level dict,
        # Qtable[state] ={'u':xx, 'd':xx, ...}
        # If Qtable[state] already exits, then do
        # not change it.
        if state not in self.Qtable:
            data = {}
            data['u'] = 0    
            data['d'] = 0
            data['l'] = 0
            data['r'] = 0
            self.Qtable[state] = data
   

    def choose_action(self):
        """
        Return an action according to given rules
        """
        def is_random_exploration():
            # TODO 5. Return whether do random choice
            # hint: generate a random number, and compare
            # it with epsilon
            value = random.uniform(0,1)
            #print("random select value is:",value)
            if value < self.epsilon:
                return True
            else:
                return False
        state = self.maze.sense_robot()
        if self.learning:
            if is_random_exploration():
                # TODO 6. Return random choose aciton
                actions = ['u','r','d','l']
                max_index = actions.index(max(self.Qtable[state], key=self.Qtable[state].get))
                #print("max index is : ",max_index)
                policys = np.ones(4) * self.epsilon / 4
                policys[max_index] = 1 - self.epsilon + self.epsilon / 4
                self.action = np.random.choice(actions,p=policys)
                return self.action
            else:
                # TODO 7. Return action with highest q value
                actions = ['u','r','d','l']
                self.action = max(self.Qtable[state], key=self.Qtable[state].get)
                #self.action = actions[max_index]
                return self.action
        elif self.testing:
            # TODO 7. choose action with highest q value
            actions = ['u','r','d','l']
            #max_index = actions.index(max(self.Qtable[state], key=self.Qtable[state].get))
            #self.action = actions[max_index]
            self.action = max(self.Qtable[state], key=self.Qtable[state].get)
            return self.action
        else:
            actions = ['u','r','d','l']
            max_index = actions.index(max(self.Qtable[state], key=self.Qtable[state].get))
            policys = np.ones(4) * self.epsilon / 4
            policys[max_index] = 1 - self.epsilon + self.epsilon / 4
            self.action = np.random.choice(actions,p=policys)
            return self.action

    def update_Qtable(self, r, action, next_state):
        """
        Update the qtable according to the given rule.
        """
        if self.learning:
            pass
            # TODO 8. When learning, update the q table according
            # to the given rules
            actions = ['u','r','d','l']
            maxa = actions.index(max(self.Qtable[next_state], key=self.Qtable[next_state].get))
            next_action = actions[maxa]
            #print("update Qtable max next action is:",next_action)
            self.Qtable[self.state][action] = self.Qtable[self.state][action] + self.alpha*(r + self.gamma * self.Qtable[next_state][next_action] - self.Qtable[self.state][action])
            

    def update(self):
        """
        Describle the procedure what to do when update the robot.
        Called every time in every epoch in training or testing.
        Return current action and reward.
        """
        self.state = self.sense_state() # Get the current state
        self.create_Qtable_line(self.state) # For the state, create q table line
        
        action = self.choose_action() # choose action for this state
        reward = self.maze.move_robot(action) # move robot for given action

        next_state = self.sense_state() # get next state
        self.create_Qtable_line(next_state) # create q table line for next state

        if self.learning and not self.testing:
            self.update_Qtable(reward, action, next_state) # update q table
            self.update_parameter() # update parameters

        return action, reward
