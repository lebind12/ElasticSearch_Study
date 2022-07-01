import os
import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
from pprint import pprint

region = 'ap-northeast-2'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = os.environ["SEARCH_ENGINE_URL"]
index = 'movies'

def searching_movies(match_string):
    query = {
        "size" : 25,
        "query" : {
            "multi_match" : {
                "query" : match_string,
                "fields" : ["title^4", "plot^2", "actors", "directors"]
            }
        }
    }
    
    url = host + '/' + index + '/_search?q=%s&pretty' % match_string
    # print
    headers = {"Content-Type" : "application/json"}
    r = requests.get(url=url, auth=(os.environ["MASTER_ID"],os.environ["MASTER_PASSWORD"]), headers=headers, data=json.dumps(query))
    pprint(r.text)


if __name__ == '__main__' : 
    searching_movies("mars");