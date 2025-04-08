import base64
import os
import uuid
from datetime import datetime

import boto3


def generate_timestamp_id():
    timestamp = datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix = uuid.uuid4().hex[:6]
    return f"run_{timestamp}_{suffix}"


class KMSUtil:
    def __init__(self):
        self.kms = boto3.client(
            "kms",
            region_name=os.getenv("AWS_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def encrypt(self, key_id, plaintext: str) -> str:
        if not key_id:
            msg = "Key ID is required for encryption."
            raise ValueError(msg)
        if not plaintext:
            msg = "Config is required for encryption."
            raise ValueError(msg)
        response = self.kms.encrypt(
            KeyId=key_id,
            Plaintext=plaintext.encode("utf-8"),
        )
        return base64.b64encode(response["CiphertextBlob"]).decode("utf-8")

    def decrypt(self, key_id, ciphertext_b64: str) -> str:
        if not key_id:
            msg = "Key ID is required for decryption."
            raise ValueError(msg)
        if not ciphertext_b64:
            msg = "Ciphertext is required for decryption."
            raise ValueError(msg)
        ciphertext = base64.b64decode(ciphertext_b64)
        response = self.kms.decrypt(
            KeyId=key_id,
            CiphertextBlob=ciphertext,
        )
        return response["Plaintext"].decode("utf-8")

    def create_kms_key_for_customer(self, customer_id: uuid.UUID) -> str:
        response = self.kms.create_key(
            Description=f"KMS key for customer {customer_id}",
            KeyUsage="ENCRYPT_DECRYPT",
            CustomerMasterKeySpec="SYMMETRIC_DEFAULT",
            Origin="AWS_KMS",
        )
        key_id = response["KeyMetadata"]["KeyId"]

        alias_name = f"alias/customer-{customer_id}"
        self.kms.create_alias(AliasName=alias_name, TargetKeyId=key_id)

        return key_id
