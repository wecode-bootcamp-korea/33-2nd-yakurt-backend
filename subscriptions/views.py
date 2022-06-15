import json
import uuid

import boto3
from django.http  import JsonResponse
from django.views import View

from core.utils           import login_decorator
from subscriptions.models import Review, Subscription
from yakurt.settings      import (
    AWS_ACCESS_KEY_ID, 
    AWS_SECRET_ACCESS_KEY, 
    AWS_STORAGE_BUCKET_NAME, 
    AWS_IMAGE_URL
)
class GoogleClient:
    pass

class NaverClient:
    pass

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key
        )
        self.s3_client   = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try: 
            file_id    = str(uuid.uuid4())
            extra_args = { 'ContentType' : file.content_type }

            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    file_id,
                    ExtraArgs = extra_args
                )
            return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}'
        except:
            return None

    def delete(self, file_name):
        return self.s3_client.delete_object(bucket=self.bucket_name, Key=f'{file_name}')

class FileHandler:
    def __init__(self, client):
        self.client = client
    
    def upload(self, file):
        return self.client.upload(file)


class Reviewdetailview(View) :
    @login_decorator
    def post(self, request, subscription_id) :
        try :
            user    = request.user
            file    = request.FILES['file']
            content = request.POST['content']

            subscription = Subscription.objects.get(id=subscription_id) # 예외 처리 추가
            
            client = MyS3Client(
                AWS_ACCESS_KEY_ID, 
                AWS_SECRET_ACCESS_KEY, 
                AWS_STORAGE_BUCKET_NAME
            )
            file_handler = FileHandler(client)
            file_url     = file_handler.upload(file)
            
            Review.objects.create(
                image_url    = file_url,
                content      = content,
                user         = user,
                subscription = subscription
            )
            return JsonResponse({'Message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'Message': 'KEYERROR'}, status=400) 

