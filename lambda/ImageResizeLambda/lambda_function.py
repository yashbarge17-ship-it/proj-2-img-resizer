import boto3
import io
import urllib.parse
from PIL import Image

s3 = boto3.client("s3")


# Different compression levels
COMPRESSION = {
    "small": 50,
    "medium": 70,
    "large": 85
}


def lambda_handler(event, context):

    for record in event["Records"]:

        bucket = record["s3"]["bucket"]["name"]

        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        # Process only images inside original/
        if not key.startswith("original/"):
            continue

        # Get original image from S3
        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        image = Image.open(
            io.BytesIO(response["Body"].read())
        )

        # Convert image to RGB for JPEG compression
        if image.mode != "RGB":
            image = image.convert("RGB")

        filename = key.split("/")[-1]

        # Keep original dimensions
        original_width = image.width
        original_height = image.height

        print(
            f"Original dimensions: "
            f"{original_width}x{original_height}"
        )

        # Create 3 compressed versions
        for size_name, quality in COMPRESSION.items():

            output = io.BytesIO()

            # COMPRESSION ONLY
            # Width and height are NOT changed
            image.save(
                output,
                format="JPEG",
                quality=quality,
                optimize=True
            )

            output.seek(0)

            output_key = (
                f"resized/{size_name}/{filename}"
            )

            # Upload compressed image
            s3.put_object(
                Bucket=bucket,
                Key=output_key,
                Body=output,
                ContentType="image/jpeg"
            )

            print(
                f"Created: {output_key} | "
                f"Quality: {quality} | "
                f"Dimensions: "
                f"{original_width}x{original_height}"
            )

    return {
        "statusCode": 200,
        "body": "Image compressed successfully"
    }