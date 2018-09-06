#!/bin/bash -eux

curl https://53isy6xdtb.execute-api.us-west-2.amazonaws.com/Prod/photos/

curl https://53isy6xdtb.execute-api.us-west-2.amazonaws.com/Prod/photos/?tag=Food

curl https://53isy6xdtb.execute-api.us-west-2.amazonaws.com/Prod/photos/?page=1\&page_size=1
