import base64
import logging

from cryptography.exceptions import AlreadyFinalized
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from vc import settings

logger = logging.getLogger(__name__)


def decrypt(ciphertext: str, keyPath: str = settings.PATH_RSA_PRIVATE):
    try:
        # load private key
        print(keyPath)
        with open(keyPath, "rb") as key_file:
            privateKey = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )

        # decrypt string
        plaintext = privateKey.decrypt(
            base64.b64decode(ciphertext),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plaintext.decode()
    except Exception as e:
        logger.exception(f"Decode failed: {e}")


# function to be used to generate the hashed fingerprint, input argument is the fingerprint order concatenated string
def fingerprintHash(fingerprint):
    try:
        # get digest instance
        digest = hashes.Hash(
            algorithm=hashes.SHA512(),
            backend=default_backend()
        )

        # create hash
        digest.update(fingerprint.encode('utf-8'))
        hash_bytes = digest.finalize()

        # convert/encode in hex
        return hash_bytes.hex()

    except (UnsupportedAlgorithm, AlreadyFinalized):
        logger.exception("Hashing failed")


# function to be used to generate the fingerprint signature, input arguments are the hashed fingerprint to be signed and the private 2048 RSA key file path
def fingerprintSignature(fingerprintH, keyPath: str = settings.PATH_RSA_PRIVATE):
    try:
        # load private key
        with open(keyPath, "rb") as key_file:
            privateKey = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # sign string
        signature = privateKey.sign(
            data=fingerprintH.encode('utf-8'),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA512()
        )

        return base64.b64encode(signature)
    except UnsupportedAlgorithm:
        logger.exception("Signing failed")
