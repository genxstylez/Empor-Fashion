from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

empor_storage = S3BotoStorage(bucket=settings.AWS_STORAGE_BUCKET_NAME, querystring_auth=False, \
    secure_urls=False)
