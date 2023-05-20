
# Load environment and defined functions
source ./bash-utils.sh

if [[ $1 == "generate_customers" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for customers
    deploy-lambda-function \
        "aws/lambda/generate_customers.py" \
        "./generate_customers.py" \
        "deployments/generate_customers.zip" \
        "generate_customers" \
        "{DB_DATABASE=${DB_DATABASE},DB_HOSTNAME=${DB_HOSTNAME},DB_PASSWORD=${DB_PASSWORD},DB_PORT=${DB_PORT},DB_USER=${DB_USER}}"
fi

if [[ $1 == "generate_stores" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "aws/lambda/generate_stores.py" \
        "./generate_stores.py" \
        "deployments/generate_stores.zip" \
        "generate_stores" \
        "{DB_DATABASE=${DB_DATABASE},DB_HOSTNAME=${DB_HOSTNAME},DB_PASSWORD=${DB_PASSWORD},DB_PORT=${DB_PORT},DB_USER=${DB_USER}}"
fi

if [[ $1 == "generate_staffs" || $1 == "all" ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "aws/lambda/generate_staffs.py" \
        "./generate_staffs.py" \
        "deployments/generate_staffs.zip" \
        "generate_staffs" \
        "{DB_DATABASE=${DB_DATABASE},DB_HOSTNAME=${DB_HOSTNAME},DB_PASSWORD=${DB_PASSWORD},DB_PORT=${DB_PORT},DB_USER=${DB_USER}}"
fi

if [[ $1 == "generate_products" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for products
    deploy-lambda-function \
        "aws/lambda/generate_products.py" \
        "./generate_products.py" \
        "deployments/generate_products.zip" \
        "generate_products" \
        "{DB_DATABASE=${DB_DATABASE},DB_HOSTNAME=${DB_HOSTNAME},DB_PASSWORD=${DB_PASSWORD},DB_PORT=${DB_PORT},DB_USER=${DB_USER}}"
fi

if [[ $1 == "generate_transactions" || $1 == "all"  ]]; then
    echo Build and deploy lambda function for transactions
    deploy-lambda-function \
        "aws/lambda/generate_transactions.py" \
        "./generate_transactions.py" \
        "deployments/generate_transactions.zip" \
        "generate_transactions" \
        "{DB_DATABASE=${DB_DATABASE},DB_HOSTNAME=${DB_HOSTNAME},DB_PASSWORD=${DB_PASSWORD},DB_PORT=${DB_PORT},DB_USER=${DB_USER},S3_RAW_LAYER_BUCKET=${S3_RAW_LAYER_BUCKET}}"
fi


valid_inputs=("generate_customers" "get_stores" "generate_staffs" "generate_products" 
"generate_stores" "generate_transactions" "all")

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