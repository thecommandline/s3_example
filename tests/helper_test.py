import boto3

from datetime import datetime, timedelta
from src.helper import get_bucket_size, get_buckets, format_bytes

# from src.app import generate_report


class TestFormatBytes:
    def test_format_value_bytes(self):
        assert format_bytes(123)["Value"] == 123

    def test_format_units_bytes(self):
        assert format_bytes(123)["Units"] == "Bytes"

    def test_format_value_kb(self):
        assert format_bytes(1234)["Value"] == 1.23

    def test_format_units_kb(self):
        assert format_bytes(1234)["Units"] == "KB"

    def test_format_value_mb(self):
        assert format_bytes(1234567)["Value"] == 1.23

    def test_format_units_mb(self):
        assert format_bytes(12345678)["Units"] == "MB"

    def test_format_value_gb(self):
        assert format_bytes(1234567890)["Value"] == 1.23

    def test_format_units_gb(self):
        assert format_bytes(1234567890)["Units"] == "GB"


def test_get_buckets(monkeypatch):
    # Define a mock response from the S3 API
    mock_buckets = [
        {"Name": "test-bucket1"},
        {"Name": "test-bucket2"},
        {"Name": "test-bucket3"},
    ]
    mock_response = {"Buckets": mock_buckets}

    # Define a mock client that returns the mock response
    class MockS3Client:
        def list_buckets(self):
            return mock_response

    # Patch the boto3 client with the mock client
    monkeypatch.setattr(boto3, "client", lambda _: MockS3Client())

    # test the function
    assert get_buckets() == ["test-bucket1", "test-bucket2", "test-bucket3"]


def test_get_bucket_size(monkeypatch):
    # Define a mock response from the CloudWatch API
    mock_response = {
        "MetricDataResults": [
            {
                "Id": "abc123",
                "Timestamps": [datetime.now() - timedelta(days=1)],
                "Values": [1024],
                "StatusCode": "Complete",
            }
        ],
        "ResponseMetadata": {"RequestId": "mock-request-id"},
    }

    # Define a mock client that returns the mock response
    class MockCloudWatchClient:
        def get_metric_data(self, **kwargs):
            return mock_response

    # Patch the boto3 client with the mock client
    monkeypatch.setattr(boto3, "client", lambda _: MockCloudWatchClient())

    # Test the function
    bucket_size = get_bucket_size("test-bucket", "STANDARD")
    assert bucket_size["MetricDataResults"][0]["Values"][0] == 1024


# def test_generate_report(monkeypatch):
#     # Define mock data for get_buckets() and get_bucket_size()
#     mock_buckets = ["test-bucket-1", "test-bucket-2"]
#     mock_bucket_size = {"MetricDataResults": [{"Values": [1024]}]}
#
#     # Patch the get_buckets() function to return mock_buckets
#     monkeypatch.setattr("your_module.get_buckets", lambda: mock_buckets)
#
#     # Patch the get_bucket_size() function to return mock_bucket_size for each bucket
#     monkeypatch.setattr("your_module.get_bucket_size", lambda _, __: mock_bucket_size)
#
#     # Test the function
#     generate_report()
#
#     # Assert that output.csv was created with the correct content
#     with open("output.csv", "r") as csvfile:
#         reader = csv.reader(csvfile)
#         assert next(reader) == ["Bucket", "Size", "Units"]
#         assert next(reader) == ["test-bucket-1", "1.00", "KB"]
#         assert next(reader) == ["test-bucket-2", "1.00", "KB"]
#
#     # Clean up the output.csv file
#     os.remove("output.csv")
