#!flask/bin/python
# -*- coding: utf-8 -*-

import json
import re
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, Response, render_template, request
from helloworld.flaskrun import flaskrun


application = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')


def dynamodb_scan(tag='', page=0, page_size=20):
    # image_path = 'http://midaisuk-yourphotos.s3-website-ap-northeast-1.amazonaws.com/images/'
    # image_path = 'http://d1t3obqy4hw1u6.cloudfront.net/'
    # image_path = 'http://isdfamilyday2018photos.s3-website-us-west-2.amazonaws.com/images/'
    image_path = 'images/'
    items = []
    table_name = 'familyday2018photos'

    table = dynamodb.Table(table_name)
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

        # while page*page_size > len(results['Items'])
        #     page -= 1
        #     results = table.scan(
        #         ExclusiveStartKey=results['LastEvaluatedKey'],
        #         FilterExpression=Attr('tags').contains(tag) | Attr('name_tags').contains(tag) | Attr('emotion_tags').contains(tag),
        #         Limit=page_size
        #     )

    else:
        results = table.scan(Limit=page_size)
        results_count = table.scan(Select='COUNT')

        while page>0 and 'LastEvaluatedKey' in results:
            page -= 1
            results = table.scan(
                ExclusiveStartKey=results['LastEvaluatedKey'],
                Limit=page_size
            )

    for result in results['Items']:
        item = {'name': result['name']}
        item['image_uri'] = image_path + 'thumbnails_large/' + item['name']
        item['thumbnail_uri'] = image_path + 'thumbnails_small/' + item['name']

        item['tags'] = []
        if result.has_key('tags'):
            item['tags'] = result['tags']

        item['name_tags'] = []
        if result.has_key('name_tags'):
            item['name_tags'] = result['name_tags']

        item['emotion_tags'] = []
        if result.has_key('emotion_tags'):
            item['emotion_tags'] = result['emotion_tags']


        items.append(item)

    return items, results_count['Count']


@application.route('/', methods=['GET'])
@application.route('/index', methods=['GET'])
def index():
    message = ''
    search_text = re.sub(re.compile("[!-/:-@[-`{-~]"), '', request.args.get('search', default=''))
    page = int(request.args.get('page', default=0))
    page_size = int(request.args.get('page_size', default=60))
    message += search_text
    pagination = dict()

    # scan dynamodb
    try:
        items, count = dynamodb_scan(search_text, page, page_size=page_size)
    except Exception as e:
        message = 'connection error'
        print('ERROR!')
        print(e)

    if count < page_size:
        pagination['display_items'] = count
    else:
        pagination['display_items'] = page_size
    pagination['total_items'] = count
    pagination['page_size'] = page_size
    pagination['max_page'] = int(count / page_size)
    pagination['page'] = page

    if page > 0: 
        if search_text:
            pagination['previous'] = '?page=%d&page_size=%d&search=%s' % (page-1, page_size, search_text)
        else:
            pagination['previous'] = '?page=%d&page_size=%d' % (page-1, page_size)

    if count > page_size * (page+1): 
        if search_text:
            pagination['next'] = '?page=%d&page_size=%d&search=%s' % (page+1, page_size, search_text)
        else:
            pagination['next'] = '?page=%d&page_size=%d' % (page+1, page_size)


    return render_template('index.html', message=message, items=items, search_text=search_text, pagination=pagination)


@application.route('/api', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
