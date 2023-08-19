import boto3
from pprint import pprint

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')


def create_volume_with_client():
    new_volume = ec2_client.create_volume(
        AvailabilityZone='ap-southeast-2a',
        Size=5,
        VolumeType='gp2',
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Python & Boto3'
                    }
                ]
            }
        ]
    )

    return "Created Volume ID : {} ".format(new_volume["VolumeId"])


def create_volume_with_resource():
    new_volume = ec2_client.create_volume(
        AvailabilityZone='ap-southeast-2b',
        Size=5,
        VolumeType='gp2',
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Python & Boto3 with resource'
                    }
                ]
            }
        ]
    )

    return "Created Volume ID : {} ".format(new_volume.id)


# print(create_volume_with_client())


def list_volumes():
    for volume in ec2_resource.volumes.all():
        print(volume)


# list_volumes()

def find_volume():
    for volume in ec2_resource.volumes.filter(
            Filters=[
                        {
                            'Name': 'tag:Name',
                            'Values': [
                                'Python & Boto3',
                            ]
                        }
                    ]
            ):
        print(f'Volume {volume.id} ({volume.size} Gib) -> {volume.state}')

        # print(ec2_resource.volumes.filter(id='vol-0bfc81221a962a7d4'))

# find_volume()


def attach_volume_ec2():
    volume = ec2_resource.Volume('vol-0c67796a52fa4688e ')
    print(f'Volume {volume.id} status -> {volume.state}')

    volume.attach_to_instance(
        Device='/dev/sdh',
        InstanceId='i-00992b0dd6126d3e3'
    )

    print(f'Volume {volume.id} Status -> {volume.state}')

# attach_volume_ec2()


def detach_volume_ec2():
    volume = ec2_resource.Volume('vol-0c67796a52fa4688e ')
    print(f'Volume {volume.id} status -> {volume.state}')

    volume.detach_from_instance(
        Device='/dev/sdh',
        InstanceId='i-00992b0dd6126d3e3'
    )

    waiter = ec2_client.get_waiter('volume_available')
    waiter.wait(
        VolumeIds=[
            volume.id
        ]
    )

    print(f'Volume {volume.id} Status -> {volume.state}')


# detach_volume_ec2()

def increase_volume(volume_id):

    response = ec2_client.modify_volume(
        VolumeId=volume_id,
        Size=7
    )

    return response


# print(increase_volume('vol-0c67796a52fa4688e'))

def delete_ebs_volume(volume_id):
    volume = ec2_resource.Volume(volume_id)

    if volume.state == "available":
        volume.delete()
        print("Volume Deleted")
    else:
        print("Can not delete volume attached")


delete_ebs_volume('vol-0e7fb0e6d9a7392b0')


def create_snap_Shot(volume_id):

    snapshot = ec2_resource.create_snapshot(
        VolumeId=volume_id,
        TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Python Snapshot'
                    }
                ]
            }
        ]
    )

    print('Snapshot is created')
    return snapshot


# print(create_snap_Shot('vol-0e7fb0e6d9a7392b0'))
