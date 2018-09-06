#!/bin/bash -xeu

STACK_NAME=PhotoManagerBackend

TEMPLATE_BUCKET=s3://midaisuk-templates/photomanager/
PREFIX=photomanager

mkdir -p sync

# set up addtags lambda
mkdir -p addtags/build
pip-3.6 install Pillow -t addtags/build/
cp addtags/*.py addtags/build/
(cd addtags/build; zip -r9 ../../sync/addtags.zip .)

# set up faceindex lambda
mkdir -p faceindex/build
cp faceindex/*.py faceindex/build/
(cd faceindex/build; zip -r9 ../../sync/faceindex.zip .)

aws s3 sync sync ${TEMPLATE_BUCKET}

# check template
aws cloudformation validate-template \
    --template-body file://template.yaml

# create stack
aws cloudformation create-stack \
    --stack-name ${STACK_NAME} \
    --template-body file://template.yaml \
    --parameters \
        ParameterKey=BucketName,ParameterValue=${PREFIX}faceindex \
        ParameterKey=PhotosBucketName,ParameterValue=${PREFIX}photos \
        ParameterKey=IndexDynamoDBTableName,ParameterValue=${PREFIX}faceindex \
        ParameterKey=PhotosDynamoDBTableName,ParameterValue=${PREFIX}photos \
        ParameterKey=CollectionName,ParameterValue=${PREFIX}-faceindex \
    --capabilities CAPABILITY_IAM \
    --region us-west-2

# aws cloudformation delete-stack --stack-name PhotoManager --region us-west-2
