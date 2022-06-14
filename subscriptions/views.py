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

            subscription = Subscription.objects.get(id=subscription_id)
            
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
        
        except Subscription.DoesNotExist:
            return JsonResponse({'Message': 'SUBSCRIPTION_DOES_NOT_EXIST'}, status=404)

    @login_decorator
    def get(self, request, subscription_id) :
        results = [{
            'id'       : review.id,
            'nick_name': review.user.nick_name,
            'content'  : review.content,
            'image_url': review.image_url,
            'create_at': review.created_at,
            'products' : [subscription.product.name for subscription in review.subscription.subscriptionitem_set.all()]
        } for review in Review.objects.filter(subscription_id=subscription_id)
        ]
        
        return JsonResponse({'results': results,}, status=200)
    
    @login_decorator
    def delete(self, request, subscription_id):
        Review.objects.filter(subscription_id=subscription_id, user_id=request.user.id).delete()
        return JsonResponse({'Message': 'NO_CONTENT'}, status=204)

class SubscriptionListview(View) :
    @login_decorator
    def get(self, request):
        user = request.user
        
        subscription = Subscription.objects.filter(user_id = user.id)
        
        results = [{
            'subscription_id'        : subscription.id,
            'subscription_created_at': subscription.created_at,
            'subscription_product'   : [subscription.product.name for subscription in subscription.subscriptionitem_set.all()],
            'is_subscribing'         : subscription.is_subscribing,
            'subscription_review'    : [{
                'review_id'     : review.id,
                'review_img'    : review.image_url,
                'review_content': review.content,
                'create_at'     : review.created_at,
                }for review in subscription.review_set.all()]
        }for subscription in subscription]
        
        return JsonResponse({'results': results}, status=200)