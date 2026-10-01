# AWS Cloud Image Compressor

## 1. Project Overview

AWS Cloud Image Compressor is a serverless image processing application built using AWS services.

The application allows a user to upload an image through a web interface. The image is securely uploaded to Amazon S3 using a presigned URL. When the image is uploaded, an S3 event automatically triggers an AWS Lambda function.

The Lambda function uses the Pillow library to compress the image and creates three compressed versions:

- Small — Quality 50
- Medium — Quality 70
- Large — Quality 85

The original image dimensions are preserved. The compressed images are stored in Amazon S3 and can be viewed or downloaded individually from the website.

---

## 2. Project Objective

The main objectives of this project are:

- Build a serverless image processing application.
- Upload images securely to Amazon S3.
- Automatically process uploaded images using AWS Lambda.
- Compress images without changing their original dimensions.
- Generate multiple compression-quality versions.
- Store processed images in Amazon S3.
- Allow users to view and download individual compressed images.
- Monitor Lambda execution using Amazon CloudWatch.
- Use IAM to control AWS resource permissions.

---

## 3. AWS Services Used

| AWS Service | Purpose |
|---|---|
| Amazon S3 | Stores original and compressed images |
| AWS Lambda | Generates presigned URLs and processes images |
| IAM | Controls permissions for Lambda |
| Amazon CloudWatch | Stores Lambda logs and helps with monitoring |

### Additional Library

**Pillow**

Pillow is a Python image-processing library used by the image-processing Lambda function.

---

## 4. Architecture

```text
                    User
                     |
                     v
              HTML Web Application
                     |
                     |
                     v
          GenerateUploadUrl Lambda
                     |
                     |
              Presigned S3 URL
                     |
                     v
             Amazon S3 Bucket
                     |
                     |
              original/
                     |
                     | S3 Object Created Event
                     v
          ImageResizeLambda-proj2
                     |
                     | Pillow
                     |
        +------------+------------+
        |            |            |
        v            v            v
     small/       medium/       large/
     Quality 50   Quality 70    Quality 85
        |            |            |
        +------------+------------+
                     |
                     v
              Amazon S3 Bucket
                     |
                     v
          GenerateUploadUrl Lambda
                     |
                     v
            Presigned Download URL
                     |
                     v
                   User