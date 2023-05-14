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
zip -r my-lambda-package.zip python


# Upload to s3
echo 'Start uploading layer to s3'
aws s3 cp my-lambda-package.zip s3://${S3_BUCKET}/

# Delete resources
echo 'Start clean up resources'
rm my-lambda-package.zip
rm -r python
echo 'Finished!'