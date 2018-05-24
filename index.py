
import json
import urllib.parse
import boto3
import textract

print('Loading function')

s3 = boto3.client('s3')
sns = boto3.client('sns')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = 'aws-ps-boe'
    key = urllib.parse.unquote_plus('art.rtf', encoding='utf-8')
    
    try:
        s3.Bucket(bucket).download_file(key, 'local.rtf')

        text = textract.process('local.rtf')

        response = client.publish(
            TargetArn='arn:aws:sns:eu-west-1:676831350542:tim',
            Message=json.dumps({'default': json.dumps(text)}),
            MessageStructure='json'
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e