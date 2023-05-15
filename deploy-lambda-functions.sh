
# Load environment and defined functions
source ./bash-utils.sh

if [[ $1 == "customers" ]]; then
    echo Build and deploy lambda function for customers
    deploy-lambda-function \
        "lambda/db/generate_customers.py" \
        "./generate_customers.py" \
        "deployments/generate_customers.zip" \
        "generate_customers"

elif [[ $1 == "stores" ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "lambda/db/generate_stores.py" \
        "./generate_stores.py" \
        "deployments/generate_stores.zip" \
        "generate_stores"

elif [[ $1 == "staffs" ]]; then
    echo Build and deploy lambda function for stores
    deploy-lambda-function \
        "lambda/db/generate_staffs.py" \
        "./generate_staffs.py" \
        "deployments/generate_staffs.zip" \
        "generate_staffs"

else
    echo "This bash script receive following input: [customers, stores, staffs]. Please try again!"

fi

