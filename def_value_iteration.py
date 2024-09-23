def value_iteration(self, gamma=0.9, theta=0.001):
    while True:
        delta = 0
        for state in self.states:
            v = self.states_value.get(state, 0)
            max_value = float('-inf')
            for action in self.action:
                value = 0
                for next_state in self.states:
                    prob = self.transition_prob(state, action, next_state)
                    reward = self.reward(state, action, next_state)
                    value += prob * (reward + gamma * self.states_value.get(next_state, 0))
                max_value = max(max_value, value)
            self.states_value[state] = max_value
            delta = max(delta, abs(v - self.states_value[state]))
        if delta < theta:
            break
def reward(self, state, action, next_state):
    if self.is_win(next_state):
        return 1
    elif self.is_loss(next_state):
        return -1
    elif self.is_draw(next_state):
        return 0.5
    else:
        return -0.1

def is_win(self, state):
    pass

def is_loss(self, state):
    pass

def is_draw(self, state):
    pass