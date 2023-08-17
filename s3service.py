import boto3, os

bucket_client = boto3.client('s3')
bucket_res = boto3.resource('s3')
from pprint import pprint


def create_bucket(bucket_name):
    response = bucket_client.create_bucket(
        ACL='private',
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-southeast-2'
        },
    )
    '''
        response = bucket_res.create_bucket(
            Bucket = "parwizforogh7777",
            ACL="private",
        )
    '''
    return response


def delete_bucket(bucket_name):
    """
        response_bucket = bucket_res.Bucket(bucket_name)
        response_bucket.delete()
    """
    response = bucket_client.delete_bucket(
        Bucket=bucket_name,
    )
    return response


def list_bucket():
    """
        response = bucket_res.buckets.all()
        for bucket in response:
            print(bucket)
    """
    return bucket_client.list_buckets()


def put_object(bucket_name, file_name):
    with open(file_name, 'rb') as fp:
        data = fp.read()
    response = bucket_client.put_object(
        ACL='private',
        Bucket=bucket_name,
        Body=data,
        Key=file_name
    )
    return response


def empty_bucket_objects(bucket_name):
    # deleting bucket inside objects
    bucket_s3 = bucket_res.Bucket(bucket_name)
    bucket_s3.objects.all().delete()

    # deleting bucket versions
    bucket_s3.object_versions.delete()


def upload_file(bucket_name, file_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    '''
    response = bucket_client.meta.upload_file(file_name, bucket_name, object_name)
    for pdf upload
    '''

    response = bucket_client.upload_file(file_name, bucket_name, object_name)
    return response


def download_file(bucket_name, file_name):
    file_object = bucket_res.Object(bucket_name, file_name)
    file_object.download_file('tiru.txt')


def list_objects(bucket_name):
    response = bucket_client.list_objects(
        Bucket=bucket_name
    )
    """    
        response = bucket_res.Bucket(bucket_name)
        for obj in response.objects.all():
            print(obj.key)
    """
    return response


def get_object_filtered_file(bucket_name,file_name):
    response = bucket_client.get_object(
        Bucket=bucket_name,
        Key=file_name)

    """
    response = bucket_res.Bucket(bucket_name)
    for obj in response.objects.filter(Prefix='file'):
        print(obj.key)
        
    """
    return response


def copy_object_from_bucket_bucket(destination_bucket,source_bucket,file_name):
    response = bucket_client.copy_object(
        Bucket=destination_bucket,
        CopySource='/'+source_bucket+'/'+file_name,
        Key=file_name,
    )

    return response


def delete_object(bucket_name,file_name):
    response = bucket_client.delete_object(Bucket=bucket_name,Key=file_name)
    """
    # delete multiple objects
    response = bucket_client.delete_objects(
        Bucket=bucket_name,
        Delete={
        'Objects':[
            {
            'Key':file_name,
            }
            {
            'Key':file_name2
            }
        ]}
    )
    """
    return response



# data = create_bucket('thirumalareddy79779')
# data = delete_bucket('thirumalareddy797797')
# data = list_bucket()
# data = put_object('thirumalareddy79779','Screenshot (16).png')
# empty_bucket_objects('thirumalareddy797797')
# data = upload_file('thirumalareddy79779','file.txt')
# download_file('thirumalareddy79779','file.txt')
# data = list_objects('thirumalareddy79779')
# data = get_object_filtered_file('thirumalareddy79779','file.txt')
# data = copy_object_from_bucket_bucket('thirumalareddy797','thirumalareddy79779','file.txt')
# data = delete_object('thirumalareddy797','file.txt')
# pprint(data)
