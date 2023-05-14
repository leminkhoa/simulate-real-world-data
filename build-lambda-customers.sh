cp lambda/db/generate_customers.py ./generate_customers.py
zip -r deployments/generate_customers.zip generate_customers.py src
rm ./generate_customers.py
