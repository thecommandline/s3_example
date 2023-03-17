import sys
import csv

from helper import get_bucket_size, get_buckets, format_bytes


def generate_report():
    buckets = get_buckets()

    if not buckets:
        print("No Buckets Found!")
        sys.exit()

    with open("output.csv", "w") as csvfile:
        output = csv.writer(csvfile)
        for bucket in buckets:
            bucket_size = get_bucket_size(bucket, "StandardStorage")[
                "MetricDataResults"
            ][0]["Values"]

            if len(bucket_size) == 0:
                bucket_size = {"Value": "0", "Units": "Bytes"}
            else:
                bucket_size = format_bytes(int(bucket_size[0]))

            output.writerow([bucket, bucket_size["Value"], bucket_size["Units"]])


if __name__ == "__main__":
    generate_report()
