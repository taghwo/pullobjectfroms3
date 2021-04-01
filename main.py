import boto3
import os
from zipfile import ZipFile
from dotenv import load_dotenv
load_dotenv()
import time
import shutil
import datetime
import random

def pulls3object():
     now = datetime.datetime.now()
     s3 = boto3.resource('s3', endpoint_url = 'https://s3.wasabisys.com',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                      config=boto3.session.Config(signature_version='s3v4'),
                      region_name=os.getenv('AWS_REGION')
                      )
     bucket = s3.Bucket(os.getenv('AWS_PUBLIC_S3_BUCKET_NAME'))
     files_payload = []
     for file in bucket.objects.all():
         if (file.last_modified).replace(tzinfo = None) >= datetime.datetime(2021, 3, 16,tzinfo = None) and (file.last_modified).replace(tzinfo = None) <= datetime.datetime(2021, 3, 19,tzinfo = None):
            if('resume' not in file.key):
                files_payload.append({'file':file.key,'timestamp':file.last_modified})
                download_template_from_aws(file.key,file.last_modified)
     print('zipping files')
     root_dir = 'remotefiles'
     base_dir = f"remotefiles-{now.strftime('%d-%m-%y')}"
     shutil.make_archive(base_dir, 'zip', root_dir)

def download_template_from_aws(s3_file_name,last_modified):
    s3 = boto3.client('s3',endpoint_url = 'https://s3.wasabisys.com', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    try:
        '''
        check if directory exist
        '''
        root_dir = "remotefiles"

        date = datetime.datetime.strptime(str(last_modified).replace('+00:00',''),"%Y-%m-%d %H:%M:%S")
        tuple = date.timetuple()
        timestamp = time.mktime(tuple)

        human_read_able_time = time.ctime(timestamp).replace(' ','-').replace(':','-')

        sub_dir = f'{root_dir}/{human_read_able_time}-{random.randint(0,100)}-{random.randint(0,100)}'

        os.mkdir(sub_dir)

        file_path = f'{sub_dir}/{human_read_able_time}-{random.randint(0,100)}-{random.randint(0,100)}.mp3'

        s3.download_file(
            Bucket=os.getenv('AWS_PUBLIC_S3_BUCKET_NAME'),
            Key=s3_file_name,
            Filename=file_path
        )
        print('downloaded')

    except Exception as e:
        print('downloadFileS3@Error')
        print(e.args)
pulls3object()