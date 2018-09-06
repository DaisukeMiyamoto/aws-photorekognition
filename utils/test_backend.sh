#!/bin/bash

BUCKET_NAME=photomanagerphotos

aws s3 cp sample1.jpg s3://${BUCKET_NAME}/images/originals/
