#!/bin/bash -x


STACK_NAME=Familyday2018
TEMPLATE_URL=https://s3-us-west-2.amazonaws.com/midaisuk-templates/familyday2018/template.yaml

# (cd lambda/faceindex; zip -r ../../faceindex.zip *)
# aws s3 cp faceindex.zip s3://midaisuk-templates/familyday2018/faceindex.zip
# rm faceindex.zip

# (cd lambda/addtags; zip -r ../../addtags.zip *)
# aws s3 cp addtags.zip s3://midaisuk-templates/familyday2018/addtags.zip
# rm addtags.zip

# aws s3 cp templates/familyday2018_faceindex.yaml s3://midaisuk-templates/familyday2018/template.yaml

aws cloudformation validate-template --template-url ${TEMPLATE_URL}

aws cloudformation create-stack --stack-name ${STACK_NAME} \
--template-url ${TEMPLATE_URL} \
--parameters \
ParameterKey=BucketName,ParameterValue=isdfamilyday2018faceindex \
ParameterKey=PhotosBucketName,ParameterValue=isdfamilyday2018photos \
ParameterKey=IndexDynamoDBTableName,ParameterValue=familyday2018faceindex \
ParameterKey=PhotosDynamoDBTableName,ParameterValue=familyday2018photos \
ParameterKey=CollectionName,ParameterValue=familyday2018-faceindex \
--capabilities CAPABILITY_IAM \
--region us-west-2

# aws cloudformation delete-stack --stack-name Familyday2018 --region us-west-2

