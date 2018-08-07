import io
from decimal import Decimal
import json
import urllib
import boto3
from botocore.exceptions import ClientError
from PIL import Image, ImageDraw, ExifTags
import PIL

REGION = 'us-west-2'
resource_map = {
        'us-west-2': {'BucketName': 'familydayphoto', 'CollectionId': 'familydayphoto', 'TableName': 'familydayphoto'}
    }

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb', region_name=REGION)
rekognition = boto3.client('rekognition', region_name=REGION)


def get_exif(img):

    if not img._getexif():
        return {'Orientation': 1}
    
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    return exif

def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response

def crop_faces(image, detect_faces_response):    
    faces_binary_list = []
    cropped_list = []
    for faces in detect_faces_response['FaceDetails']:
        bb = faces['BoundingBox']
        
        x, y, w, h = int(bb['Left']*image.size[0]), int(bb['Top']*image.size[1]), int(bb['Width']*image.size[0]), int(bb['Height']*image.size[1])
        face = image.crop((x, y, x+w, y+h))
        
        stream = io.BytesIO()
        face.save(stream,format="JPEG")
        
        image_binary = stream.getvalue()
        faces_binary_list.append(image_binary)
        
        cropped_list.append(face)
        
    return faces_binary_list, cropped_list

def get_name(face_binary):
    name = ''
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=resource_map[REGION]['CollectionId'],
#             Image={'S3Object':{'Bucket':bucket,'Name':fileName}}
            Image={'Bytes':face_binary}
        )
        for match in response['FaceMatches']:
            face = dynamodb.get_item(
                TableName=resource_map[REGION]['TableName'],
                Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                )
            if 'Item' in face:
                name = face['Item']['FullName']['S']
                return name
            else:
                name = 'UNKNOWN'
    except ClientError as err:
        code = err.response['Error']['Code']
        if code == 'InvalidParameterException':
            name = 'NOFACE'
        elif code == 'AccessDeniedException':
            name = 'DENIED'
        elif code == 'InvalidImageFormatException':
            name = 'ILLFORMED'
        else:
            name = 'ERR'
#     return name

def rotate(img):
    exif = get_exif(img)
    orientation = exif['Orientation']

    if orientation == 6:
        return img.rotate(270, expand=True)
    elif orientation == 3:
        return img.rotate(180)
    elif orientation == 1:
        return img


def get_names(bucket, key):
    print('detct faces')
    bbs = detect_faces(bucket, key)
    print('route')
    img = Image.open(s3.get_object(Bucket=bucket, Key=key)['Body'])
    img = rotate(img)
    print('crop')
    faces_binary_list, face_list = crop_faces(img, bbs)
    print('get_names')
    name_list = [get_name(face_binary) for face_binary in faces_binary_list]
    return list(filter(None.__ne__, name_list))


if __name__ == '__main__':
    img_key = 'test/img8.jpg'

    print(get_names(resource_map[REGION]['BucketName'], img_key))
