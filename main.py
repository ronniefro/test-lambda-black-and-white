import json
import logging
from urllib.parse import unquote_plus
import boto3
from PIL import Image
import PIL.Image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def grayscale_image(image_path, modified_path):
    with Image.open(image_path) as image:
        grayscale = image.convert('L')
        grayscale.save(modified_path)

def lambda_handler(event, context):
    logger.info('Start of lambda handler')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}'.format(tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)
        grayscale_image(download_path, upload_path)
        s3_client.upload_file(upload_path, 'turn-images-black-and-white-output', 'bw-{}'.format(key))
    
    logger.info('End of lambda handler')
    return {
        'statusCode': 200,
        'body': json.dumps('Output from turning an image black and white!')
    }

