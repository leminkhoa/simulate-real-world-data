
# Load environment and defined functions
source ./bash-utils.sh

if [[ $1 == "generate_customers" ]]; then
    echo Build and deploy lambda function for customers
    deploy-lambda-function \
        "lambda/db/generate_customers.py" \
        "./generate_customers.py" \
        "deployments/generate_customers.zip" \
        "generate_customers"

elif [[ $1 == "generate_stores" ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "lambda/db/generate_stores.py" \
        "./generate_stores.py" \
        "deployments/generate_stores.zip" \
        "generate_stores"

elif [[ $1 == "generate_staffs" ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "lambda/db/generate_staffs.py" \
        "./generate_staffs.py" \
        "deployments/generate_staffs.zip" \
        "generate_staffs"

elif [[ $1 == "generate_products" ]]; then
    echo Build and deploy lambda function for products
    deploy-lambda-function \
        "lambda/db/generate_products.py" \
        "./generate_products.py" \
        "deployments/generate_products.zip" \
        "generate_products"

elif [[ $1 == "generate_transactions" ]]; then
    echo Build and deploy lambda function for transactions
    deploy-lambda-function \
        "lambda/db/generate_transactions.py" \
        "./generate_transactions.py" \
        "deployments/generate_transactions.zip" \
        "generate_transactions"


elif [[ $1 == "get_transactions" ]]; then
    echo Build and deploy lambda function for transactions
    deploy-lambda-function \
        "lambda/db/get_transactions.py" \
        "./get_transactions.py" \
        "deployments/get_transactions.zip" \
        "get_transactions"

else
    echo "This bash script receive following input:
    - generate_customers
    - generate_stores
    - generate_staffs
    - generate_products
    - generate_stores
    - generate_transactions
    - get_transactions
    Please try again!"

fi
