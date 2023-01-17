import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


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

        super(DQN, self).__init__()

        # TODO: check different types of layers
        self.layer1 = nn.Linear(*input_dims, layer1_dims)
        self.layer2 = nn.Linear(layer1_dims, layer2_dims)
        self.layer3 = nn.Linear(layer1_dims, n_actions)

        # TODO: Check different optimizer and loss
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def feed_forward(self, state):
        # TODO: check different activations
        x = F.relu(self.layer1(state))
        x = F.relu(self.layer2(x))
        actions = self.layer3(x)

        return actions


class Agent():
    def __init__(self, gamma, epsilon, lr, input_dims, batch_size, n_actions, max_mem_size=10000, eps_min=0.01, eps_dec=3e-4):
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
        @param eps_end      (float): Minimum size of epsilon in the epsilon-greedy exploration strategy
        @param eps_dec      (float): Decrease step of epsilon in the epsilon-greedy exploration strategy
        """
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        self.lr = lr
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = max_mem_size
        self.batch_size = batch_size
        self.mem_cntr = 0

        self.q_eval = QNetwork(
            lr=lr, input_dims=input_dims, fc1_dims=256, fc2_dims=256, n_actions=n_actions)

        self.state_memory = np.zeros(
            (self.mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros(
            (self.mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)

    def store_transition(self, state, action, reward, new_state, done):
        """!
        Stores the state transition for later memory replay.

        @param state        (list): Vector describing current state
        @param action       (int): Action taken
        @param reward       (float): Received reward
        @param new_state    (list): Newly observed state.
        """

        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = new_state
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done

        self.mem_cntr += 1

    def choose_action(self, observation):
        """!
        Chooses agent's action based on observation and exploration strategy.

        @param observation (list): Vector describing current state

        @return int: Action to take
        """

        # TODO: Implement softmax exploration
        if np.random.random() > self.epsilon:
            state = T.tensor([observation]).to(self.q_eval.device)  # why []?
            actions = self.q_eval.forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)

        return action

    def learn(self):
        """! 
        Updates the network using memory replay.
        """

        if self.mem_cntr < self.batch_size:
            return

        self.q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace=False)

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = T.tensor(self.state_memory[batch]).to(self.q_eval.device)
        new_state_batch = T.tensor(
            self.new_state_memory[batch]).to(self.q_eval.device)
        reward_batch = T.tensor(
            self.reward_memory[batch]).to(self.q_eval.device)
        terminal_batch = T.tensor(
            self.terminal_memory[batch]).to(self.q_eval.device)

        action_batch = self.action_memory[batch]
        q_eval = self.q_eval.forward(state_batch)[batch_index, action_batch]
        q_next = self.q_eval.forward(new_state_batch)
        q_next[terminal_batch] = 0.0

        q_target = reward_batch + self.gamma * T.max(q_next, dim=1)[0]

        loss = self.q_eval.loss(q_target, q_eval).to(self.q_eval.device)
        loss.backward()
        self.q_eval.optimizer.step()

        self.epsilon = self.epsilon - \
            self.eps_dec if self.epsilon > self.eps_min else self.eps_min
