provider "aws" {
  region = "${var.region}"
  access_key = "AKIAUZWLBPGUCCNBF5EP"
  secret_key = "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"
}

data "aws_kms_alias" "kms_encryption" {
  name = "alias/aws/s3"
}

# Old working part.... before lambda function container image
resource "aws_s3_bucket" "bucket" {
  bucket = "bucket-firehose-ver1"
  acl    = "private"
}

resource "aws_kinesis_firehose_delivery_stream" "firehose_stream" {
  name        = "${var.app_name}_firehose_delivery_stream"
  destination = "s3"
  kinesis_source_configuration {
    kinesis_stream_arn = "${aws_kinesis_stream.kinesis_stream.arn}"
    role_arn           = "${aws_iam_role.firehose_role.arn}"
  }
  //refer the more s3 configuration at https://docs.aws.amazon.com/firehose/latest/APIReference/API_ExtendedS3DestinationConfiguration.html
  s3_configuration {
    role_arn        = "${aws_iam_role.firehose_role.arn}"
    bucket_arn      = aws_s3_bucket.bucket.arn
    buffer_size     = 5
    buffer_interval = "100"
    }
  }
