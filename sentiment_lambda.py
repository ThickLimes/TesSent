from __future__ import print_function

import base64
import json
import boto3
from datetime import datetime

print('Sentinent Analysis')

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        
        dict_data = base64.b64decode(record['data']).decode('utf-8').strip()
        print(dict_data)
        
        comprehend = boto3.client(service_name='comprehend', region_name='eu-west-1')
        sent = comprehend.detect_sentiment(Text=dict_data, LanguageCode='en')
        sentiment = sent['Sentiment']
        pos = sent['SentimentScore']['Positive']
        neg = sent['SentimentScore']['Negative']
        total = pos - neg
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        data_record = {
            'message': dict_data,
            'sentiment': sentiment,
            'total': total,
            'timestamp':dt_string}
 
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(data_record).encode('utf-8')).decode('utf-8')}
        
        output.append(output_record)

    print(output)
    return {'records': output}
