import json
import logging
import os
import subprocess  # nosec
import tempfile

import boto3
from botocore.exceptions import ClientError
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger()

s3 = boto3.client("s3")
sm = boto3.client("secretsmanager")


def get_secret_string(secret_id):
    secret_value = sm.get_secret_value(SecretId=secret_id)
    return json.loads(secret_value["SecretString"])  # pragma: allowlist secret


def get_engine():
    db_secret_id = os.getenv("DB_SECRET_ID")
    creds = get_secret_string(db_secret_id)
    url = (
        f"postgresql+psycopg2://{creds['username']}:{creds['password']}"
        f"@{creds['proxy']}:{creds['port']}/{creds['dbname']}"
    )
    return create_engine(url)


def already_converted(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise


def get_extension(file_id, conn, metadata):
    ffidmetadata = Table("FFIDMetadata", metadata, autoload_with=conn)
    file_table = Table("File", metadata, autoload_with=conn)

    try:
        stmt = (
            select(ffidmetadata.c.Extension)
            .where(ffidmetadata.c.FileId == file_id)
            .limit(1)
        )
        result = conn.execute(stmt).first()
        if result and result[0]:
            return result[0].lower()
    except SQLAlchemyError as e:
        conn.rollback()
        raise Exception(f"Error querying FFIDMetadata table: {e}")

    logger.info(
        f"No extension found in FFIDMetadata for {file_id}. Trying to extract from file_name instead"
    )
    try:
        stmt = (
            select(file_table.c.FileName)
            .where(file_table.c.FileId == file_id)
            .limit(1)
        )
        result = conn.execute(stmt).first()
        if result and result[0]:
            filename = result[0]
            if "." in filename:
                return filename.rsplit(".", 1)[1].lower()
            logger.warning("No extension in FileName")
    except SQLAlchemyError as e:
        conn.rollback()
        raise Exception(f"Error querying File table: {e}")


def convert_with_libreoffice(input_path, output_path, convert_to="pdf"):
    try:
        subprocess.run(  # nosec
            [
                "soffice",
                "--headless",
                "--convert-to",
                convert_to,
                "--outdir",
                os.path.dirname(output_path),
                input_path,
            ],
            check=True,
            stderr=subprocess.PIPE,
        )
        logger.info(f"Converted {input_path} to {output_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"LibreOffice conversion failed: {e.stderr.decode()}"
        )


def convert_xls_xlsx_to_pdf(tmpdir, input_path, output_path):
    temp_ods = os.path.join(tmpdir, "input.ods")
    convert_with_libreoffice(input_path, temp_ods, convert_to="ods")
    convert_with_libreoffice(
        temp_ods,
        output_path,
        convert_to='pdf:calc_pdf_Export:{"SinglePageSheets":{"type":"boolean","value":"true"}}',
    )


def process_consignment(
    consignment_ref, source_bucket, dest_bucket, convertible_extensions, conn
):
    prefix = f"{consignment_ref}/"
    metadata = MetaData()

    response = s3.list_objects_v2(Bucket=source_bucket, Prefix=prefix)
    if "Contents" not in response:
        logger.warning(f"No files found in consignment {consignment_ref}")
        return

    logger.info(
        f"{len(response['Contents'])} files in consignment {consignment_ref}"
    )

    for obj in response["Contents"]:
        key = obj["Key"]
        file_id = key.split("/")[-1]
        logger.info(f"Checking file_id: {file_id}")

        try:
            extension = get_extension(file_id, conn, metadata)
        except Exception as e:
            logger.error(f"Failed to get file_extension for {file_id}: {e}")
            continue
        logger.info(f"File extension: {extension}")

        if extension not in convertible_extensions:
            logger.info(f"File {file_id} does not require conversion")
            continue

        dest_key = f"{consignment_ref}/{file_id}"
        if already_converted(dest_bucket, dest_key):
            logger.info(f"Skipping {file_id}, already converted")
            continue

        logger.info(f"File {file_id} requires conversion to PDF")
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, f"input.{extension}")
            output_path = os.path.join(tmpdir, "input.pdf")

            s3.download_file(source_bucket, key, input_path)
            logger.info(f"Downloaded {key} to {input_path}")

            try:
                if extension in ("xls", "xlsx"):
                    convert_xls_xlsx_to_pdf(tmpdir, input_path, output_path)
                else:
                    convert_with_libreoffice(input_path, output_path)
                logger.info(f"Converted {file_id} to PDF")
            except Exception as e:
                logger.error(f"Conversion failed for {file_id}: {e}")
                continue

            s3.upload_file(output_path, dest_bucket, dest_key)
            logger.info(f"Uploaded converted file {file_id} to {dest_bucket}")


def create_access_copies_for_all_consignments(
    source_bucket, dest_bucket, convertible_extensions, conn
):
    paginator = s3.get_paginator("list_objects_v2")
    response = paginator.paginate(Bucket=source_bucket)
    consignments = set()
    for page in response:
        for obj in page["Contents"]:
            consignments.add(obj["Key"].split("/")[0])

    logger.info(f"Found {len(consignments)} consignments")
    for consignment_ref in consignments:
        logger.info(f"Processing consignment: {consignment_ref}")
        process_consignment(
            consignment_ref,
            source_bucket,
            dest_bucket,
            convertible_extensions,
            conn,
        )


def create_access_copy_from_sns(
    source_bucket, dest_bucket, convertible_extensions, conn
):
    raw_sns_message = os.getenv("SNS_MESSAGE")
    if not raw_sns_message:
        raise Exception("SNS_MESSAGE environment variable not found")
    logger.info(f"Message Received: {raw_sns_message}")

    try:
        sns_message = json.loads(raw_sns_message)
    except Exception as e:
        logger.error(f"Error parsing SNS_MESSAGE: {e}")
        raise

    consignment_ref = sns_message.get("parameters", {}).get("reference")

    if not consignment_ref:
        raise Exception("Missing consignment_reference in SNS Message")
    logger.info(f"Processing consignment: {consignment_ref}")
    process_consignment(
        consignment_ref,
        source_bucket,
        dest_bucket,
        convertible_extensions,
        conn,
    )


def main():
    app_secret_id = os.getenv("APP_SECRET_ID")
    app_secret = get_secret_string(app_secret_id)
    source_bucket = app_secret["RECORD_BUCKET_NAME"]
    dest_bucket = app_secret["ACCESS_COPY_BUCKET"]
    convertible_extensions = set(
        json.loads(app_secret["CONVERTIBLE_EXTENSIONS"])
    )

    conversion_type = os.getenv("CONVERSION_TYPE")
    if not conversion_type:
        raise Exception("CONVERSION_TYPE environment variable not found")
    engine = get_engine()
    conn = engine.connect()
    if conversion_type == "ALL":
        create_access_copies_for_all_consignments(
            source_bucket, dest_bucket, convertible_extensions, conn
        )

    elif conversion_type == "SINGLE":
        create_access_copy_from_sns(
            source_bucket, dest_bucket, convertible_extensions, conn
        )

    else:
        raise ValueError("Invalid CONVERSION_TYPE. Expected 'ALL' or 'SINGLE'")


if __name__ == "__main__":
    main()
