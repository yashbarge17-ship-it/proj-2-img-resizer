import json
import boto3
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "cloud-image-resizer-proj2"


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    query_params = event.get("queryStringParameters") or {}

    action = query_params.get("action")


    # ==========================================
    # UPLOAD
    # ==========================================

    if action == "upload":

        file_name = query_params.get("fileName")
        content_type = query_params.get("contentType")

        if not file_name:
            return response(
                400,
                {
                    "error": "fileName is required"
                }
            )

        if not content_type:
            content_type = "application/octet-stream"


        unique_name = (
            str(uuid.uuid4())
            + "-"
            + file_name
        )

        object_key = (
            "original/"
            + unique_name
        )


        upload_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key,
                "ContentType": content_type
            },
            ExpiresIn=300
        )


        return response(
            200,
            {
                "uploadUrl": upload_url,
                "key": object_key
            }
        )


    # ==========================================
    # VIEW / DOWNLOAD
    # ==========================================

    if action == "view":

        key = query_params.get("key")

        if not key:
            return response(
                400,
                {
                    "error": "key is required"
                }
            )


        download = (
            query_params.get("download")
            == "true"
        )


        params = {
            "Bucket": BUCKET_NAME,
            "Key": key
        }


        if download:

            filename = key.split("/")[-1]


            params[
                "ResponseContentDisposition"
            ] = (
                'attachment; filename="'
                + filename
                + '"'
            )


            params[
                "ResponseContentType"
            ] = "application/octet-stream"


        view_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=300
        )


        return response(
            200,
            {
                "viewUrl": view_url
            }
        )


    # ==========================================
    # INVALID ACTION
    # ==========================================

    return response(
        400,
        {
            "error": "Invalid action"
        }
    )