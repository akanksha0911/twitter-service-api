import json

from flask import Flask, make_response, request
import boto3
import base64
from botocore.exceptions import ClientError
import oauth2 as oauth


def get_secret():
    secret_name = "arn:aws:secretsmanager:us-east-1:559976405953:secret:twitterSecret-P4Xo84"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    secret_client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = secret_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])


app = Flask(__name__)

secrets = json.loads(get_secret())
CONSUMER_KEY = secrets['consumer_key']
CONSUMER_SECRET = secrets['consumer_secret']
ACCESS_KEY = secrets['access_token']
ACCESS_SECRET = secrets['access_token_secret']

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)


@app.route("/sendTweet", methods=["POST", "GET"])
def tweet():
    print(request.json['text'])
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/update.json?status=" + request.json['text']
    response, data = client.request(timeline_endpoint, method="POST")

    resp = make_response(data)  # here you could use make_response(render_template(...)) too
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/getTweet", methods=["POST", "GET"])
def get_tweet():
    print(request.json['id'])
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/lookup.json?id=" + request.json['id']
    response, data = client.request(timeline_endpoint, method="GET")

    resp = make_response(data)  # here you could use make_response(render_template(...)) too
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/deleteTweet", methods=["POST", "GET"])
def delete_tweet():
    print(request.json['id'])
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/destroy/" + request.json['id'] + ".json"
    response, data = client.request(timeline_endpoint, method="POST")

    resp = make_response(data)  # here you could use make_response(render_template(...)) too
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
