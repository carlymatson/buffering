import random
from collections import defaultdict, Counter


class MarkovBot:
    def __init__(self, training_chains=None, stop_tokens=(None,)):
        self.stop_tokens = stop_tokens
        self.probabilities = defaultdict(list)
        self.tokens = []
        if training_chains:
            for chain in training_chains:
                self.train(chain)

    def train(self, chain, prefix_pair=(None, None), suffix=(None, None)):
        first_token, second_token = prefix_pair
        for next_token in chain + list(suffix):
            pair = (first_token, second_token)
            self.probabilities[pair].append(next_token)
            first_token = second_token
            second_token = next_token

    def get_last_pair(self):
        token_chain = [None, None] + self.tokens
        pair = token_chain[-2:]
        return tuple(pair)

    def next_word_probabilities(self):
        token_pair = self.get_last_pair()
        next_tokens = self.probabilities[token_pair]
        token_counts = Counter(next_tokens)
        total = len(next_tokens)
        token_probabilities = [
            (tok, count / total) for tok, count in token_counts.items()
        ]
        return sorted(token_probabilities, key=lambda p: -p[1])

    def generate_random_token(self):
        pair = self.get_last_pair()
        options = self.probabilities[pair]
        next_token = random.choice(options)
        if next_token is not None:
            self.tokens.append(next_token)
        return next_token

    def generate_chain(self, min_length=0, max_length=500):
        while True:
            next_token = self.generate_random_token()
            if len(self.tokens) >= min_length and next_token in self.stop_tokens:
                break
            if len(self.tokens) >= max_length:
                break
        return self.tokens
