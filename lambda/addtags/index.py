from PIL import Image
import boto3
import os
from datetime import datetime
from get_name import get_names


s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
client = boto3.client('rekognition')

env_collection_name = os.environ['CollectionName']
env_index_dynamodb_table_name = os.environ['IndexDynamoDBTableName']
env_photos_dynamodb_table_name = os.environ['PhotosDynamoDBTableName']

def get_tags(bucket, key):
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=3,
        MinConfidence=50
    )
    return response


def put_dynamodb_record(item):
    table = dynamodb.Table(env_photos_dynamodb_table_name)
    table.put_item(Item=item)


def make_thumbnail(bucket, src, dest, size=(480,270)):
    filename = os.path.basename(src)
    tmp_path = '/tmp/'
    src_file = tmp_path + filename
    dest_file = tmp_path + 'thumb_' + filename

    s3.download_file(Bucket=bucket, Key=src, Filename=src_file)
    
    img = Image.open(src_file)
    # img.resize(size).save(dest_file)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(dest_file, quality=90)
    
    s3.upload_file(Filename=dest_file, Bucket=bucket, Key=dest)
    

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        src = event['Records'][0]['s3']['object']['key']
        dest = src.replace('originals', 'thumbnails')
        make_thumbnail(bucket, src, dest)
        
        response = get_tags(bucket, src)
        object_tags = []
        for tag in response['Labels']:
            object_tags.append(tag['Name'])

        print('name_tags', bucket, src)
        name_tags = get_names(bucket, src)
        if not name_tags:
            name_tags = []

        emotion_tags = []

        print('put dynamodb')
        item = {
            'name': os.path.basename(src),
            'tags': object_tags,
            'name_tags': name_tags,
            'emotion_tags': emotion_tags,
            'timestamp': datetime.utcnow().isoformat()
        }
        put_dynamodb_record(item)
        
        return 'Resize Finished'

    except Exception as e:
        return e
