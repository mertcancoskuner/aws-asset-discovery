import boto3, json
from datetime import date

client = boto3.client('ec2', region_name='eu-west-2')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
today = date.isoformat(date.today())

print("AWS instance list \n")

for region in regions:
    client = boto3.client('ec2', region_name=region)
    try:
        #response = client.describe_instances(Filters=[{'Name':'launch-time', 'Values':[today + '*']}]) # Fetch instances which opened today. It can be changed to filter a specific date. (Format: Year-Month-Day)
        response = client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
	                print("Instance: {}, IP: {}, LaunchTime: {}".format(instance['InstanceId'], 
									    instance['PublicIpAddress'], instance['LaunchTime']))
	                for securityGroup in instance['SecurityGroups']:
	                    print("SecurityGroup ID: {}, SecurityGroup Name: {}, \n SecurityGroup Details: {}".format(securityGroup['GroupId'], securityGroup['GroupName'], 
														      json.dumps((client.describe_security_groups(GroupIds=[securityGroup['GroupId']])), indent=2)))
            print('\n')
    except Exception as E:
        print(region, E)
        continue
