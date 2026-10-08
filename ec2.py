import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)


def get_ec2_instances(region_name="us-east-1"):
    """
    Retrieve a list of EC2 instances in the specified AWS region.

    :param region_name: The AWS region to query for EC2 instances.
    :return: A list of dictionaries containing instance details.
    """
    ec2_client = boto3.client("ec2", region_name=region_name)

    try:
        response = ec2_client.describe_instances()
        instances = []

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_info = {
                    "InstanceId": instance["InstanceId"],
                    "InstanceType": instance["InstanceType"],
                    "State": instance["State"]["Name"],
                    "PublicIpAddress": instance.get("PublicIpAddress"),
                    "PrivateIpAddress": instance.get("PrivateIpAddress"),
                    "LaunchTime": instance["LaunchTime"].strftime("%Y-%m-%d %H:%M:%S"),
                }
                instances.append(instance_info)

        return instances
    except ClientError as e:
        logging.error(e)
        return []

    except Exception as e:
        logging.error(f"Error retrieving EC2 instances: {e}")
        return []


if __name__ == "__main__":
    options = ["list"]
    while True:
        print("Options:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        choice = input("Enter the number of your choice (or 'q' to quit): ")

        if choice.lower() == "q":
            break

        try:
            choice = int(choice)
            if choice < 1 or choice > len(options):
                raise ValueError
        except ValueError:
            print("Invalid choice. Please enter a valid number.")
            continue

        region = input("Enter AWS region (default: us-east-1): ") or "us-east-1"
        if options[choice - 1] == "list":
            instances = get_ec2_instances(region)
            if instances:
                print(f"\nEC2 Instances in {region}:")
                for instance in instances:
                    print(instance)
            else:
                print("No instances found.")
