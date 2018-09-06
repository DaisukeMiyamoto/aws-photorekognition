#!/bin/bash -xeu

STACK_NAME=PhotoManagerAPI
LAMBDA_DIR=photomanager_lambda
PREFIX=photomanager

# initialize
# sam init --runtime python3.6


# test
python3 -m pytest tests/ -v


# build lambda function
pip install -r requirements.txt -t ${LAMBDA_DIR}/build/
cp ${LAMBDA_DIR}/*.py ${LAMBDA_DIR}/build/


# deploy
sam validate

sam package \
    --template-file template.yaml \
    --s3-bucket midaisuk-templates \
    --output-template-file packaged.yaml

sam deploy \
    --template-file packaged.yaml \
    --stack-name ${STACK_NAME} \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        PhotosBucketName=${PREFIX}photos \
        PhotosDynamoDBTableName=${PREFIX}photos \
    --region us-west-2

# check endpoint
aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --query 'Stacks[].Outputs[1]'

