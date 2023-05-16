import uuid
from faker import Faker
from .custom_providers import *
from src import utils


faker = Faker(use_weighting=True)
faker.add_provider(GenderProvider)
faker.add_provider(MembershipProvider)
faker.add_provider(EmailDomainProvider)
faker.add_provider(EcommerceProvider)


def generate_stores(n=3):
    output = []
    for _ in range(n):
        store = dict()
        # storename
        store['name'] = ' '.join(faker.words(nb=2)).strip('.').title()
        # address
        store['address'] = faker.street_address()
        # phone
        store['phone'] = faker.phone_number()
        # store
        store['email'] = faker.email()
        
        output.append(store)
    return output


def generate_customers(n=10):
    output = []
    for _ in range(n):
        customer = dict()
        # id
        customer['customer_id'] = uuid.uuid4().hex
        # gender
        gender = faker.gender()
        customer['gender'] = gender
        # name
        first_name = faker.first_name_male() if gender == 'male' else faker.first_name_female()
        last_name = faker.last_name_male() if gender == 'male' else faker.last_name_female()
        customer['first_name'] = first_name
        customer['last_name'] = last_name
        # email
        company = faker.company().split()[0].strip(',')
        customer['email'] = f"{first_name}_{last_name}@{company}.{faker.domain()}".lower()
        # yob
        customer['yob'] = faker.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d')
        # phone number
        customer['phone_number'] = faker.phone_number()
        # profile
        customer['job'] = faker.job()
        # address
        customer['address'] = faker.street_address()
        # first_transaction
        customer['first_transaction'] = faker.past_date(start_date='-14d').strftime('%Y-%m-%d')
        # membership
        customer['membership'] = faker.membership()

        output.append(customer)

    return output


def generate_staffs(store_id: int, n=2):
    output = []
    for _ in range(n):
        staff = dict()
        # id
        staff['staff_id'] = uuid.uuid4().hex
        # gender
        gender = faker.gender()
        staff['gender'] = gender
        # name
        first_name = faker.first_name_male() if gender == 'male' else faker.first_name_female()
        last_name = faker.last_name_male() if gender == 'male' else faker.last_name_female()
        staff['first_name'] = first_name
        staff['last_name'] = last_name
        # store
        staff['store_id'] = store_id

        output.append(staff)
    
    return output


def generate_products(n=10):
    output = []
    for _ in range(n):
        product = dict()
        # id
        product['product_id'] = uuid.uuid4().hex
        # product name
        product['category'], product['product_name'] = faker.product_name()
        # product price
        product['unit_price'] = faker.product_price()

        output.append(product)

    return output


def generate_transactions(stores: dict, customers: dict, staffs: dict, products: dict, max_item: int, max_quantity: int, n=10):    
    def _process_data(data, filtered_fields):
        id = random.choice(list(data.keys()))
        filtered_data = utils.filter_dict(data[id], filtered_fields)
        return id, filtered_data
    
    output = []
    for _ in range(n):
        transaction = dict()
        
        # id
        transaction['transaction_id'] = uuid.uuid4().hex
        
        # store
        id, data = _process_data(stores, ['name'])
        appended_results = dict(store={'id': id, **data})
        transaction = dict(transaction, 
                           **appended_results
                        )

        # customer
        id, data = _process_data(customers, ['gender', 'first_name', 'last_name', 'email'])
        appended_results = dict(customer={'id': id, **data})
        transaction = dict(transaction, 
                           **appended_results
                        )
        
        # staffs
        id, data = _process_data(staffs, ['first_name', 'last_name'])
        appended_results = dict(staff={'id': id, **data})
        transaction = dict(transaction, 
                           **appended_results
                        )
        
        # product
        items = []
        purchased_items_number = utils.random_int(1, max_item)
        total_amount = 0
        for _ in range(purchased_items_number):
            id, data = _process_data(products, ['product_name', 'category', 'unit_price'])
            quantity = random.randint(1, max_quantity)
            appended_results = dict(item_id=id, quantity=quantity, **data)
            items.append(appended_results)
            total_amount += (int(data['unit_price']) * quantity)
        
        transaction = dict(transaction, 
                           **dict(transaction=items, purchased_number_items=purchased_items_number, total_amount=total_amount)
                        )



        output.append(transaction)

    return output
