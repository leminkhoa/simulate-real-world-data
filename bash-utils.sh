function deploy-lambda-function {
    
    # This function takes 4 arguments:
        # arg 1: local_path
        # arg 2: temp_path
        # arg 3: function_zip_package
        # arg 4: function_name

    # Load env
    source ./set_env.sh
    
    # Zip
    echo 'Zip lambda package'
    cp $1 $2 # Copy lambda function to a temp path
    zip -r $3 $2 src

    # Publish lambda handler
    echo 'Publish code to Lambda'
    JSON=$(aws lambda list-layers) # Get all lambda layers

    aws lambda update-function-code \
        --function-name $4 \
        --zip-file fileb://$3

    if [ "$?" -eq "0" ] # If the update command is successful
    then
        echo Successfully updated function $4
    else # Else create a new lambda function
        echo Function $4 does not exists, starting to create a new one
        # Find the latest layer arn by name
        aws_layer_arn=$(echo $JSON | jq --arg AWS_LAMBDA_LAYER \
            "$AWS_LAMBDA_LAYER" -r '.Layers[] | select(.LayerName == $AWS_LAMBDA_LAYER) | .LatestMatchingVersion.LayerVersionArn'
            )
        variables="{DB_DATABASE=${DB_DATABASE},DB_HOSTNAME=${DB_HOSTNAME},DB_PASSWORD=${DB_PASSWORD},DB_PORT=${DB_PORT},DB_USER=${DB_USER}}"
        
        aws lambda create-function \
        --function-name $4 \
        --role ${AWS_LAMBDA_ROLE_ARN} \
        --zip-file fileb://$3 \
        --runtime python3.9 \
        --handler $4.lambda_handler \
        --layer ${aws_layer_arn} \
        --environment Variables=${variables}
        echo Successfully created function $4
    fi

    # Delete resources
    echo Start clean up resources
    rm $2
    echo - deleted $2
    rm $3
    echo - deleted $3
    echo Finished!
}



function deploy-lambda-layer {
    
    # This function takes 1 arguments:
        # arg 1: zip package name
    
    # Load env
    source ./set_env.sh

    # Create folder
    mkdir python
    cd python

    # Install
    echo 'Install packages'
    pip install -r ../requirements.txt -t .
    rm -rf *dist-info
    cd ..

    # Zip
    echo 'zip package'
    zip -r ${1} python


    # Upload to s3
    echo 'Start uploading layer to s3'
    aws s3 cp ${1} s3://${S3_BUCKET}/

    # Delete resources
    echo 'Start clean up resources'
    rm ${1}
    rm -r python

    # Publish to aws lambda
    echo 'Publish layer to Lambda'
    aws lambda publish-layer-version \
        --layer-name ${AWS_LAMBDA_LAYER} \
        --description "Layer to be used for lambda functions in this project" \
        --content S3Bucket=${S3_BUCKET},S3Key=$1 \
        --compatible-runtimes python3.9

    echo 'Finished!'

}