import base64

import boto3
from django.conf import settings


class KMSHelper:
    def __init__(self):
        self.kms = boto3.client("kms")

    def encrypt(self, plaintext: str) -> str:
        response = self.kms.encrypt(
            KeyId=settings.AWS_KMS_KEY_ID,
            Plaintext=plaintext.encode("utf-8"),
        )
        return base64.b64encode(response["CiphertextBlob"]).decode("utf-8")

    def decrypt(self, ciphertext_b64: str) -> str:
        ciphertext = base64.b64decode(ciphertext_b64)
        response = self.kms.decrypt(
            KeyId=settings.AWS_KMS_KEY_ID,
            CiphertextBlob=ciphertext,
        )
        return response["Plaintext"].decode("utf-8")

    def create_kms_key_for_customer(self, customer_id: str) -> str:
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
