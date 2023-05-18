
# Load environment and defined functions
source ./bash-utils.sh

if [[ $1 == "generate_customers" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for customers
    deploy-lambda-function \
        "lambda/db/generate_customers.py" \
        "./generate_customers.py" \
        "deployments/generate_customers.zip" \
        "generate_customers"
fi

if [[ $1 == "generate_stores" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "lambda/db/generate_stores.py" \
        "./generate_stores.py" \
        "deployments/generate_stores.zip" \
        "generate_stores"
fi

if [[ $1 == "generate_staffs" || $1 == "all" ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "lambda/db/generate_staffs.py" \
        "./generate_staffs.py" \
        "deployments/generate_staffs.zip" \
        "generate_staffs"
fi

if [[ $1 == "generate_products" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for products
    deploy-lambda-function \
        "lambda/db/generate_products.py" \
        "./generate_products.py" \
        "deployments/generate_products.zip" \
        "generate_products"
fi

if [[ $1 == "generate_transactions" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for transactions
    deploy-lambda-function \
        "lambda/db/generate_transactions.py" \
        "./generate_transactions.py" \
        "deployments/generate_transactions.zip" \
        "generate_transactions"
fi

if [[ $1 == "get_transactions" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for transactions
    deploy-lambda-function \
        "lambda/db/get_transactions.py" \
        "./get_transactions.py" \
        "deployments/get_transactions.zip" \
        "get_transactions"
fi

valid_inputs=("generate_customers" "get_stores" "generate_staffs" "generate_products" 
"generate_stores" "generate_transactions" "get_transactions" "all")

if [[ ! " ${valid_inputs[@]} " =~ " ${1} " ]]; then
echo "This bash script receive following input:
- all (Deploy all lambda functions)
- generate_customers
- generate_stores
- generate_staffs
- generate_products
- generate_stores
- generate_transactions
- get_transactions
Please try again!"
fi