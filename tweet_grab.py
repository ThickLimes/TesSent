from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import boto3
import time


#Variables that contains the user credentials to access Twitter API
consumer_key = '74kYHUIi2qeskNxEO0HVsOeuD'
consumer_secret ='RCtvO2RCwANhQTFYc9HU3t3t92wEeMSx4NNum7mpJfXqcngPqa'
access_token = '704131740839751681-6pjtaxdgqjDgUN9m0zYX1RFDiIdmQcn'
access_token_secret = 'EPFjxHxPUyTXJuNHrkUP8DeWgpH6cdr3C2t7jgwZF6Wvm'

class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        try:
            if 'extended_tweet' in tweet.keys():
                #print (tweet['text'])
                message_lst = [tweet['extended_tweet']['full_text'],
                       str(tweet['created_at']),
                       '\n'
                       ]
                message = '\t'.join(message_lst)
                print(message)
                client.put_record(
                    DeliveryStreamName=delivery_stream,
                    Record={
                    'Data': message
                    }
                )
            elif 'text' in tweet.keys():
                #print (tweet['text'])
                message_lst = [tweet['text'].replace('\n',' ').replace('\r',' '),
                       str(tweet['created_at']),
                       '\n'
                       ]
                message = '\t'.join(message_lst)
                print(message)
                client.put_record(
                    DeliveryStreamName=delivery_stream,
                    Record={
                    'Data': message
                    }
                )
        except (AttributeError, Exception) as e:
                print (e)
        return True

    def on_error(self, status):
        print (status)
        
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #tweets = Table('tweets_ft',connection=conn)
    client = boto3.client('firehose', 
                          region_name='us-east-1',
                          aws_access_key_id='',
                          aws_secret_access_key='' 
                          )

    delivery_stream = 'tesla_sent'
    #
    while True:
        try:
            print('Twitter streaming...')
            stream = Stream(auth, listener)
            stream.filter(track=['tesla'], languages=['en'], stall_warnings=True)
        except Exception as e:
            print(e)
            print('Disconnected...')
            time.sleep(5)
            continue         
