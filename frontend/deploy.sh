#!/bin/bash -xeu
BUCKET_NAME=photomanagerweb

npm run build
aws s3 sync dist/ s3://${BUCKET_NAME}/
