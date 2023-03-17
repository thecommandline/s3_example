import boto3
from datetime import datetime, timedelta


def get_buckets():
    client = boto3.client("s3")

    buckets = []
    response = client.list_buckets()
    for bucket in response["Buckets"]:
        buckets.append(bucket["Name"])
    return buckets


def get_bucket_size(bucket, storage_class):
    client = boto3.client("cloudwatch")

    end_time = datetime.now() - timedelta(days=1)
    start_time = end_time - timedelta(days=1)

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "abc123",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/S3",
                        "MetricName": "BucketSizeBytes",
                        "Dimensions": [
                            {"Name": "BucketName", "Value": bucket},
                            {"Name": "StorageType", "Value": storage_class},
                        ],
                    },
                    "Period": 86400,
                    "Stat": "Average",
                    "Unit": "Bytes",
                },
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    return response


def format_bytes(bytes):
    if bytes < 1000:
        return {"Value": round(bytes, 2), "Units": "Bytes"}
    if bytes >= 1000 and bytes < 1000000:
        return {"Value": round(bytes / 1000, 2), "Units": "KB"}
    if bytes >= 1000000 and bytes < 1000000000:
        return {"Value": round(bytes / 1000000, 2), "Units": "MB"}
    return {"Value": round(bytes / 1000000000, 2), "Units": "GB"}
