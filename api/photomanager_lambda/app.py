import json
import re
import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')


def get_imagelist(tag='', page=0, page_size=60):
    image_path = 'images/'
    items = []
    table = dynamodb.Table(os.environ['PhotosDynamoDBTableName'])
    # paginator = dynamodb.get_paginator('scan')

    if tag != '':
        # TODO: update scan method for over 1MB response
        tmp_results = table.scan(FilterExpression=Attr('search_tags').contains(tag))
        results_count = table.scan(Select='COUNT', FilterExpression=Attr('search_tags').contains(tag))

        if len(tmp_results['Items']) > page*page_size+page_size:
            results = {'Items': tmp_results['Items'][page*page_size:page*page_size+page_size]}
        elif len(tmp_results['Items']) > page*page_size:
            results = {'Items': tmp_results['Items'][page*page_size:]}
        else:
            results = {'Items': []}

    else:
        results = table.scan(Limit=page_size)
        results_count = table.scan(Select='COUNT')

        while page>0 and 'LastEvaluatedKey' in results:
            page -= 1
            results = table.scan(
                ExclusiveStartKey=results['LastEvaluatedKey'],
                Limit=page_size
            )

    logger.info(json.dumps(results['Items']))

    for result in results['Items']:
        item = {'name': result['name']}
        item['image_uri'] = image_path + 'thumbnails_large/' + item['name']
        item['thumbnail_uri'] = image_path + 'thumbnails_small/' + item['name']

        item['tags'] = []
        if 'tags' in result:
            item['tags'] = result['tags']

        item['name_tags'] = []
        if 'name_tags' in result:
            item['name_tags'] = result['name_tags']

        item['emotion_tags'] = []
        if 'emotion_tags' in result:
            item['emotion_tags'] = result['emotion_tags']


        items.append(item)

    return items, results_count['Count']


def event_photos(event, params):

    tag = ''
    page = 0
    page_size = 60
    
    if 'tag' in params:
        tag = params['tag']

    if 'page' in params:
        page = int(params['page'])

    if 'page_size' in params:
        page_size = int(params['page_size'])


    items, count = get_imagelist(tag, page, page_size)
    if page > 0:
        previous_page = page - 1
    else:
        previous_page = -1
    
    if (page+1)*page_size < count:
        next_page = page + 1
    else:
        next_page = -1

    pagination = {
        'count': count,
        'previous':previous_page, 
        'next': next_page,
        'page_size': page_size,
        'tag': tag,
        'page': page
    }

    return items, pagination


def lambda_handler(event, context):
    logger.info('got event: {}'.format(event))
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    
    
    params = None
    if event['httpMethod'] == 'GET':
        params = event['queryStringParameters']

    if params is None:
        params = dict()

    items, pagination = event_photos(event, params)
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(
            {'message': 'Photos', 'data': items, 'pagination': pagination}
        ),
    }


