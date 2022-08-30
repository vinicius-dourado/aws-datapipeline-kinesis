resource "aws_s3_bucket" "buckets" {
  count  = length(var.bucket_names)
  bucket = "${var.prefix}-${var.bucket_names[count.index]}-${var.environment}"

  force_destroy = true
  tags = local.common_tags
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_sse" {
  count  = length(var.bucket_names)
  bucket = "${var.prefix}-${var.bucket_names[count.index]}-${var.environment}"

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  count  = length(var.bucket_names)
  bucket = "${var.prefix}-${var.bucket_names[count.index]}-${var.environment}"
  acl    = "private"
}

# Rules for public access block
resource "aws_s3_bucket_public_access_block" "public_access_block" {
  count  = length(var.bucket_names)
  bucket = "${var.prefix}-${var.bucket_names[count.index]}-${var.environment}"

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
