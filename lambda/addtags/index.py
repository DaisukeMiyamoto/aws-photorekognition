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
        MaxLabels=4,
        MinConfidence=50
    )
    return response


def put_dynamodb_record(item):
    table = dynamodb.Table(env_photos_dynamodb_table_name)
    table.put_item(Item=item)


def rotate_image(img):
    convert_image = {
        1: lambda img: img,
        2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
        3: lambda img: img.transpose(Image.ROTATE_180),
        4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
        5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Pillow.ROTATE_90),
        6: lambda img: img.transpose(Image.ROTATE_270),
        7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Pillow.ROTATE_270),
        8: lambda img: img.transpose(Image.ROTATE_90),
    }
    
    exif = img._getexif()
    if not exif:
        orientation = exif.get(0x112, 1)
        new_img = convert_image[orientation](img)
        return new_img
    else:
        return img


def make_thumbnail(bucket, src, dest_large, dest_small):
    large_size=(1920, 1080)
    small_size=(480,270)
    filename = os.path.basename(src)
    tmp_path = '/tmp/'
    src_file = tmp_path + filename
    dest_file_large = tmp_path + 'thumb_large_' + filename
    dest_file_small = tmp_path + 'thumb_small_' + filename

    s3.download_file(Bucket=bucket, Key=src, Filename=src_file)
    
    tmp_img = Image.open(src_file)
    img = rotate_image(tmp_img)
    # img.resize(size).save(dest_file)
    img.thumbnail(large_size, Image.ANTIALIAS)
    img.save(dest_file_large, quality=90)
    img.thumbnail(small_size, Image.ANTIALIAS)
    img.save(dest_file_small, quality=90)
    
    s3.upload_file(Filename=dest_file_large, Bucket=bucket, Key=dest_large, ExtraArgs={'ContentType': "application/json"})
    s3.upload_file(Filename=dest_file_small, Bucket=bucket, Key=dest_small, ExtraArgs={'ContentType': "application/json"})
    

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        src = event['Records'][0]['s3']['object']['key']
        dest_large = src.replace('originals', 'thumbnails_large')
        dest_small = src.replace('originals', 'thumbnails_small')
        make_thumbnail(bucket, src, dest_large, dest_small)
        
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
