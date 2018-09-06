import boto3

bucket_name = 'photomanagerfaceindex'


def register(name):
    image_path = '../secret/'
    s3 = boto3.client('s3')
    
    s3.upload_file(
        image_path + name + '.jpeg',
        bucket_name,
        'index/' + name + '.jpeg',
        ExtraArgs={'Metadata': {'FullName': name}}
    )
    print('Successfully registered:', name)


name_list = [
    'hariby',
    'midaisuk',
    'kiiwami',
    'iizus',
    'okunotom'
]

for name in name_list:
    register(name)
