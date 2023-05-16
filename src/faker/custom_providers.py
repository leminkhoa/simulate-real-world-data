import os
import random
from faker.providers import BaseProvider
from src import utils

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


class EcommerceProvider(BaseProvider):
    product_data = utils.parse_yaml(os.path.dirname(__file__), 'ecommerce_provider.yml')
    
    def product_name(self):
        """Fake product name and category."""
        category_pool = self.product_data['category'].keys()
        category = self.random_element(category_pool)
        product = self.random_element(self.product_data['category'][category])
        adjective = self.random_element(self.product_data['adjective'])
        material = self.random_element(self.product_data['material'])
        color = self.random_element(self.product_data['color'])

        choices = [
            " ".join([adjective, product]),
            " ".join([material, product]),
            " ".join([color, product]),
            " ".join([adjective, color, material, product]),
        ]

        return category, random.choices(choices, k=1)[0]

    def product_price(self, as_int: bool = True):
        n = self.random_int(min=10, max=500)
        return round(n, 2) if as_int else n / 100
