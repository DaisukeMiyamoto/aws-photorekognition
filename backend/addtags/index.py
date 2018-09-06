from PIL import Image
import boto3
import os
from datetime import datetime
from get_name import get_names
import logging

logger = logging.getLogger()
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
        MaxLabels=6,
        MinConfidence=60
    )
    return response


def get_smiles_by_face_details(bucket, key):
    smiles = 0
    response = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        Attributes=['ALL']
    )
    for face in response['FaceDetails']:
        if face['Smile']['Value'] and face['Smile']['Confidence'] > 90:
            smiles += 1

    return smiles


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
    
    if not '_getexif' in dir(img):
        return img
        
    exif = img._getexif()
    if exif:
        orientation = exif.get(0x112, 1)
        new_img = convert_image[orientation](img)
        return new_img
    else:
        return img


def make_thumbnail(bucket, src, dest_large, dest_small):
    large_size=(1600, 1200)
    small_size=(640, 480)
    filename = os.path.basename(src)
    tmp_path = '/tmp/'
    src_file = tmp_path + filename
    dest_file_large = tmp_path + 'thumb_large_' + filename
    dest_file_small = tmp_path + 'thumb_small_' + filename

    s3.download_file(Bucket=bucket, Key=src, Filename=src_file)
    object_head = s3.head_object(Bucket=bucket, Key=src)
    content_type = 'image/jpeg'
    # print(object_head)
    if 'ContentType' in object_head:
        content_type = object_head['ContentType']
    
    tmp_img = Image.open(src_file)
    if tmp_img.mode != "RGB":
        tmp_img = tmp_img.convert("RGB")
    
    # rotate
    img = rotate_image(tmp_img)
    
    # make thumbnail
    if img.size[1] > img.size[0]:
        img.thumbnail((large_size[1], large_size[0]), Image.ANTIALIAS)
        img.save(dest_file_large, quality=90)
        img.thumbnail((small_size[0], small_size[1]/9*16), Image.ANTIALIAS)
        img = img.crop(
            [0,
            int((img.size[1] - small_size[1])/2),
            img.size[0],
            img.size[1] - int((img.size[1] - small_size[1])/2)]
        )
        img.save(dest_file_small, quality=90)

    else:
        img.thumbnail(large_size, Image.ANTIALIAS)
        img.save(dest_file_large, quality=90)
        img.thumbnail(small_size, Image.ANTIALIAS)
        img.save(dest_file_small, quality=90)
    
    s3.upload_file(Filename=dest_file_large, Bucket=bucket, Key=dest_large, ExtraArgs={'ContentType': content_type})
    s3.upload_file(Filename=dest_file_small, Bucket=bucket, Key=dest_small, ExtraArgs={'ContentType': content_type})
    
    os.remove(src_file)
    os.remove(dest_file_large)
    os.remove(dest_file_small)


def lambda_handler(event, context):

    
    bucket = event['Records'][0]['s3']['bucket']['name']
    src = event['Records'][0]['s3']['object']['key']
    logger.info('src: %s' % (src))

    dest_large = src.replace('originals', 'thumbnails_large')
    dest_small = src.replace('originals', 'thumbnails_small')
    make_thumbnail(bucket, src, dest_large, dest_small)
    search_tags = []
    
    # object tags
    response = get_tags(bucket, src)
    object_tags = []
    for tag in response['Labels']:
        if tag['Name'] != 'Human' and tag['Name'] != 'Person':
            object_tags.append({'text': tag['Name'], 'confidence': "%.1f" % tag['Confidence']})
            search_tags.append(tag['Name'])

    # name tags
    print('name_tags', bucket, src)
    name_tags = get_names(bucket, src, threshold=85)
    if not name_tags:
        name_tags = []
    for tag in name_tags:
        search_tags.append(tag['text'])

    # emotion tags by face details
    emotion_tags = []
    smiles = get_smiles_by_face_details(bucket, src)
    if smiles > 0:
        emotion_tags.append({'text': 'Smile', 'count': str(smiles)})
        search_tags.append('Smile')

    item = {
        'name': os.path.basename(src),
        'tags': object_tags,
        'name_tags': name_tags,
        'emotion_tags': emotion_tags,
        'search_tags': search_tags,
        'timestamp': datetime.utcnow().isoformat()
    }
    put_dynamodb_record(item)
    print(json.dumps(item))
    
    return 'Process Finished %s' % item
