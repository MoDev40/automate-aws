import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)


def create_bucket(bucket_name, region="us-east-1"):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        bucket_config = {}
        s3_client = boto3.client("s3", region_name=region)
        if region != "us-east-1":
            bucket_config["CreateBucketConfiguration"] = {"LocationConstraint": region}

        s3_client.create_bucket(Bucket=bucket_name, **bucket_config)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_buckets():
    """List all buckets in the account

    :return: List of bucket names
    """
    s3_client = boto3.client("s3")
    response = s3_client.list_buckets()
    return [bucket["Name"] for bucket in response["Buckets"]]


if __name__ == "__main__":
    options = ["create", "list"]
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

        if options[choice - 1] == "create":
            bucket_name = input("Enter the name of the bucket to create: ")
            region = input("Enter the region (default is 'us-east-1'): ") or "us-east-1"
            if create_bucket(bucket_name, region):
                print(
                    f"Bucket '{bucket_name}' created successfully in region '{region}'."
                )
            else:
                print(f"Failed to create bucket '{bucket_name}'.")
        elif options[choice - 1] == "list":
            buckets = list_buckets()
            if buckets:
                print("Buckets in your account:")
                for bucket in buckets:
                    print(f"- {bucket}")
            else:
                print("No buckets found in your account.")
