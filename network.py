import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import math
import random

from constants import *


class QNetwork(nn.Module):
    def __init__(self, lr, input_dims, layer1_dims, layer2_dims, n_actions):
        """!
        Initializes a Deep Q Network used to estimate Q-values of possible actions.

        @param lr           (float): Learning rate
        @param input_dims   (int): Input dimensions
        @param layer1_dims  (int): Dimensions in the first layer
        @param layer2_dims  (int): Dimensions in the second layer
        @param n_actions    (int): Number of possible actions
        """

        super(QNetwork, self).__init__()

        # TODO: check different types of layers
        self.fc1 = nn.Linear(*input_dims, layer1_dims)
        self.fc3 = nn.Linear(layer1_dims, n_actions)

        # TODO: Check different optimizer and loss
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.L1Loss()
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def feed_forward(self, state):
        """!
        Calculates the Q-values for each action.

        @param state (list): current environment's state
        """

        x = T.tanh(self.fc1(state))
        actions = self.fc3(x)

        return actions


class Agent():
    def __init__(self, gamma, epsilon, lr, input_dims, batch_size, n_actions, max_mem_size=25000, exploration_min=0.01, exploration_dec=3e-4, exploration=Exploration.EPSILON_GREEDY):
        """!
        Initializes an Agent. 
        Note that Agent is seperate from the Deep Q Network.

        @param gamma        (float): Discount factor
        @param epsilon      (float): Initial epsilon in the epsilon-greedy exploration strategy
        @param lr           (float): Learning rate
        @param input_dims   (int): Dimensions of the state space
        @param batch_size   (int): Batch size
        @param n_actions    (int): Size of the action space
        @param max_mem_size (float): Size of memory replay buffer
        @param exploration_min      (float): Minimum size of epsilon in the epsilon-greedy exploration strategy
        @param exploration_dec      (float): Decrease step of epsilon in the epsilon-greedy exploration strategy
        @param exploration  (Exploration): Exploration strategy, e.g. EPSILON_GREEDY or SOFTMAX
        """

        self.gamma = gamma

        self.exploration = exploration

        self.epsilon = epsilon
        self.exploration_min = exploration_min
        self.exploration_dec = exploration_dec

        self.lr = lr
        self.action_space = [i for i in range(n_actions)]
        self.buffer_size = max_mem_size
        self.batch_size = batch_size
        self.mem_cntr = 0

        self.q_eval = QNetwork(
            lr=lr, input_dims=input_dims, layer1_dims=32, layer2_dims=32, n_actions=n_actions)

        self.state_buffer = np.zeros(
            (self.buffer_size, *input_dims), dtype=np.float32)
        self.new_state_buffer = np.zeros(
            (self.buffer_size, *input_dims), dtype=np.float32)
        self.action_buffer = np.zeros(self.buffer_size, dtype=np.int32)
        self.reward_buffer = np.zeros(self.buffer_size, dtype=np.float32)
        self.terminal_buffer = np.zeros(self.buffer_size, dtype=np.bool)

    def store_transition(self, state, action, reward, new_state, done):
        """!
        Stores the state transition for later memory replay.

        @param state        (list): Vector describing current state
        @param action       (int): Action taken
        @param reward       (float): Received reward
        @param new_state    (list): Newly observed state.
        """

        index = self.mem_cntr % self.buffer_size

        self.state_buffer[index] = state
        self.new_state_buffer[index] = new_state
        self.reward_buffer[index] = reward
        self.action_buffer[index] = action
        self.terminal_buffer[index] = done

        self.mem_cntr += 1

    def choose_action(self, observation):
        """!
        Chooses agent's action based on observation and exploration strategy.

        @param observation (list): Vector describing current state

        @return int: Action to take
        """

        if self.exploration == Exploration.EPSILON_GREEDY:
            return self.__choose_action_eps_greedy(observation)
        elif self.exploration == Exploration.SOFTMAX:
            return self.__choose_action_softmax(observation)

    def learn(self):
        """! 
        Updates the network using memory replay.
        """

        if self.mem_cntr < self.batch_size:
            return

        self.q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr, self.buffer_size)
        batch = np.random.choice(max_mem, self.batch_size, replace=False)

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = T.tensor(self.state_buffer[batch]).to(self.q_eval.device)
        new_state_batch = T.tensor(
            self.new_state_buffer[batch]).to(self.q_eval.device)
        reward_batch = T.tensor(
            self.reward_buffer[batch]).to(self.q_eval.device)
        terminal_batch = T.tensor(
            self.terminal_buffer[batch]).to(self.q_eval.device)

        action_batch = self.action_buffer[batch]
        q_eval = self.q_eval.feed_forward(
            state_batch)[batch_index, action_batch]
        q_next = self.q_eval.feed_forward(new_state_batch)
        q_next[terminal_batch] = 0.0

        q_target = reward_batch + self.gamma * T.max(q_next, dim=1)[0]

        loss = self.q_eval.loss(q_target, q_eval).to(self.q_eval.device)
        loss.backward()
        self.q_eval.optimizer.step()

        self.epsilon = self.epsilon - \
            self.exploration_dec if self.epsilon > self.exploration_min else self.exploration_min

    def __choose_action_eps_greedy(self, observation):
        """!
        Chooses agent's action according to epsilon greedy strategy.

        @param observation (list): current environment's state

        return int: action to take
        """

        if np.random.random() > self.epsilon:
            state = T.tensor([observation]).to(self.q_eval.device)  # why []?
            actions = self.q_eval.feed_forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)

        return action

    def __choose_action_softmax(self, observation):
        """!
        Chooses agent's action according to softmax exploration strategy.

        @param observation (list): current environment's state

        return int: action to take
        """

        state = T.tensor([observation]).to(self.q_eval.device)  # why []?
        actions = self.q_eval.feed_forward(state)
        action = T.argmax(actions).item()

        probabilites = []
        q_values = []

        for a in actions[0]:
            q_values.append(a.item())

        a = False
        for q in q_values:
            try:
                probabilites.append(
                    math.exp((q-sum(q_values)/len(q_values)) / self.epsilon))
            except:
                probabilites.append(1e5)  # dealing with overflow

        s = sum(probabilites)

        for i, p in enumerate(probabilites):
            probabilites[i] /= s

        if a or random.uniform(0, 1) < 0.01:
            print(a, probabilites)

        return random.choices(self.action_space, weights=probabilites)[0]
