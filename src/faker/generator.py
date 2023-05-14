import uuid
from faker import Faker
from .custom_providers import *


faker = Faker(use_weighting=True)
faker.add_provider(GenderProvider)
faker.add_provider(MembershipProvider)
faker.add_provider(EmailDomainProvider)


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


def generate_staffs(store_id, n=2):
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
