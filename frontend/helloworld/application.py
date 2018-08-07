#!flask/bin/python
# -*- coding: utf-8 -*-

import json
import re
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, Response, render_template, request
from helloworld.flaskrun import flaskrun


application = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')


def dynamodb_scan(tag='', page=0, page_size=20):
    # image_path = 'http://midaisuk-yourphotos.s3-website-ap-northeast-1.amazonaws.com/images/'
    image_path = 'http://d1t3obqy4hw1u6.cloudfront.net/'
    items = []

    table = dynamodb.Table('your-photo')
    # paginator = dynamodb.get_paginator('scan')

    if tag != '':
        results = table.scan(FilterExpression=Attr('tags').contains(tag) | Attr('name_tags').contains(tag) | Attr('emotion_tags').contains(tag))
    else:
        results = table.scan()

    for result in results['Items']:
        item = {'name': result['name']}
        item['image_uri'] = image_path + 'originals/' + item['name']
        item['thumbnail_uri'] = image_path + 'thumbnails/' + item['name']

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

    return items    


@application.route('/', methods=['GET'])
def index():
    message = ''
    search_text = re.sub(re.compile("[!-/:-@[-`{-~]"), '', request.args.get('search', default=''))
    message += search_text

    try:
        items = dynamodb_scan(search_text)

    except Exception as e:
        message = 'connection error'
        print('ERROR!')
        print(e)

    return render_template('index.html', message=message, items=items, search_text=search_text)


@application.route('/api', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
