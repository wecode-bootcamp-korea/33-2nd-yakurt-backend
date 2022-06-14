from unittest import result
import boto3, json

from django.http  import JsonResponse
from django.views import View

from subscriptions.models import Review, Subscription
from yakurt.settings      import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_IMAGE_URL
from core.utils           import login_decorator

class Reviewdetailview(View) :
    @login_decorator
    def post(self, request, subscription_id) :
        try :
            user    = request.user
            file    = request.FILES['file']
            content = request.POST['content']

            subscription = Subscription.objects.get(id=subscription_id)
            
            s3r = boto3.resource(
                's3', 
                aws_access_key_id     = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
            
            s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object( Key='%s'%(file), Body=file, ContentType='jpg')
            
            Review.objects.create(
                image_url    = AWS_IMAGE_URL+'%s'%(file),
                content      = content,
                user         = user,
                subscription = subscription
            )
            return JsonResponse({'Message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'Message': 'KEYERROR'}, status=400) 