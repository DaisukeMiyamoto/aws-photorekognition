#!/bin/bash -xeu
BUCKET_NAME=photomanagerphotos

npm run build
aws s3 sync dist/ s3://${BUCKET_NAME}/
