import random
from faker.providers import BaseProvider

class GenderProvider(BaseProvider):
    choices = ['male', 'female']
    prob = [0.5, 0.5]

    def gender(self):
        return random.choices(self.choices, self.prob)[0]


class MembershipProvider(BaseProvider):
    choices = ['standard', 'gold', 'platinum', 'diamond']
    prob = [0.4, 0.3, 0.2, 0.1]

    def membership(self):
        return random.choices(self.choices, self.prob)[0]


class EmailDomainProvider(BaseProvider):
    choices = ['com', 'org', 'gov']

    def domain(self):
        return random.choice(self.choices)
