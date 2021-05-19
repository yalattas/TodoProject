from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    # bucket_name = 'munjiz-static' # Delete it
    # custom_domain = 'munjiz-static.s3-eu-west-1.amazonaws.com' #delete it
    location = 'media'
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False
