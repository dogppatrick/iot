"""
Created on Thu May 17 16:27:21 2018

@author: Orozco Hsu

This is a demo cralwering to S3 crawler-20180517
"""

from boto3.s3.transfer import S3Transfer
import boto3
import io

AWS_ACCESS_KEY_ID = 'AKIAIL4R7JYZ3JJTSTFQ'
AWS_SECRET_ACCESS_KEY = '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'

import requests
from bs4 import BeautifulSoup

def get_head_text(url, head_tag):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            return soup.find(head_tag).text
    except Exception as e:
        return None

import json
url = 'http://blog.castman.net/web-crawler-tutorial/ch1/connect.html'
title = get_head_text(url, 'h1')

j = {'title': title, 'url': url}
s=json.dumps(j,ensure_ascii=False,encoding='utf8')

with io.open('output.json','w',encoding='utf8') as file:
    file.write(s)


client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
transfer = S3Transfer(client)
filepath="output.json"
bucket_name="crawler-20180517"
filename="output.json"
transfer.upload_file(filepath, bucket_name, filename)


