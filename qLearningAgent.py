import random

class QLearningAgent:
    def __init__(self, environment, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.env = environment
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_state_key(self, state):
        # Convertir l'état en une structure immuable (tuple)
        state_key = tuple(sorted((k, tuple(v) if isinstance(v, (list, dict)) else v) for k, v in state.items()))
        return state_key

    def choose_action(self, state):
        state_key = self.get_state_key(state)
        available_actions = self.env.get_actions()  # Obtenir les actions possibles

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in available_actions}

        # Epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: choisir une action aléatoire parmi les actions disponibles
            return random.choice(available_actions)
        else:
            # Exploitation: choisir l'action avec la valeur Q maximale
            return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update_q_table(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        available_actions = self.env.get_actions()  # Obtenir les actions possibles pour le nouvel état

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0 for a in available_actions}

        best_next_action = max(self.q_table[next_state_key], key=self.q_table[next_state_key].get)
        td_target = reward + self.gamma * self.q_table[next_state_key][best_next_action]
        td_error = td_target - self.q_table[state_key][action]
        self.q_table[state_key][action] += self.alpha * td_error

    def train(self, episodes):
        for _ in range(episodes):
            state = self.env.reset()
            done = False
            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update_q_table(state, action, reward, next_state)
                state = next_state
