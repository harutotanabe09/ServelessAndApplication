#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import datetime
import urllib.request
import json
import os

# Slack投稿
def post_slack(mode):
    SLACK_POST_URL = os.environ.get('slack_url') 
    set_fileds = [{
        "title": "test",
        "value": "message",
        "short": False
    }]
    DIFF_JST_FROM_UTC = 9
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    message = {}
    if mode == '1':
        message["msg"] = "始業"
        message["icon"] = "runner"
        message["color"] = "#0aff0a"
    if mode == '2':
        message["msg"] = "終業"
        message["icon"] = "end"
        message["color"] = "#f39800"

    data = {
        'attachments':  [{
            'pretext': '{0}しました :{1}: '.format(message.get('msg'),message.get('icon')),
            'author_icon': "http://flickr.com/icons/bobby.jpg",
            'color': message.get('color'),
            'text': "{0:%Y-%m-%d %H:%M:%S}".format(now),
        }]
    }
    request_headers = { 'Content-Type': 'application/json; charset=utf-8' }
    body = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(
        url=SLACK_POST_URL, 
        data=body,
        method='POST',
        headers=request_headers 
    )
    urllib.request.urlopen(request)

# メイン処置
def lambda_handler(event, context):
    mode = event['pathParameters']['uid']
    post_slack(mode)
    return {
        'statusCode': 200,
        'body': json.dumps('OK!')
    }