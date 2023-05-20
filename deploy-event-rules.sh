aws events put-rule \
    --name schedule-generate-transactions-test \
    --schedule-expression "rate(1 hour)" \
    --state DISABLED \
    --description "Event Rules to trigger lambda to generate transactions and insert results to S3"
