import hashlib
import hmac


def signature(message: str | bytes, secret: str | bytes) -> str:
    if isinstance(message, str):
        message = message.encode()

    if isinstance(secret, str):
        secret = secret.encode()

    return hmac.new(
        key=secret,
        msg=message,
        digestmod=hashlib.sha256,
    ).hexdigest()
