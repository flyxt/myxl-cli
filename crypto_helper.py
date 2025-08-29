import os, hmac, hashlib, requests, brotli, zlib, base64
from datetime import datetime, timezone, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

API_KEY = "vT8tINqHaOxXbGE7eOWAhA=="
AX_API_SIG_KEY_ASCII = b"18b4d589826af50241177961590e6693"

XDATA_DECRYPT_URL = "https://xdata.fuyuki.pw/api/decrypt"
XDATA_ENCRYPT_SIGN_URL = "https://xdata.fuyuki.pw/api/encryptsign"
PAYMENT_SIGN_URL = "https://xdata.fuyuki.pw/api/sign-payment"

AES_KEY_ASCII = "5dccbf08920a5527"
BLOCK = AES.block_size

def random_iv_hex16() -> str:
    return os.urandom(8).hex()

def _xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def b64(data: bytes, urlsafe: bool) -> str:
    enc = base64.urlsafe_b64encode if urlsafe else base64.b64encode
    return enc(data).decode("ascii")


def build_encrypted_field(iv_hex16: str | None = None, urlsafe_b64: bool = False) -> str:
    key = AES_KEY_ASCII.encode("ascii")
    iv_hex = iv_hex16 or random_iv_hex16()
    iv = iv_hex.encode("ascii") 

    pt = pad(b"", AES.block_size)
    ct = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pt)

    return b64(ct, urlsafe_b64) + iv_hex

def java_like_timestamp(now: datetime) -> str:
    ms2 = f"{int(now.microsecond/10000):02d}"
    tz = now.strftime("%z"); tz_colon = tz[:-2] + ":" + tz[-2:] if tz else "+00:00"
    return now.strftime(f"%Y-%m-%dT%H:%M:%S.{ms2}") + tz_colon

def decode_response(response):
    encoding = response.headers.get("Content-Encoding", "").lower()
    if encoding == "br":
        return brotli.decompress(response.content).decode("utf-8")
    elif encoding == "gzip":
        return zlib.decompress(response.content, zlib.MAX_WBITS | 16).decode("utf-8")
    elif encoding == "deflate":
        return zlib.decompress(response.content).decode("utf-8")
    else:
        return response.text

def ts_gmt7_without_colon(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone(timedelta(hours=7)))
    else:
        dt = dt.astimezone(timezone(timedelta(hours=7)))
    millis = f"{int(dt.microsecond / 1000):03d}"
    tz = dt.strftime("%z")
    return dt.strftime(f"%Y-%m-%dT%H:%M:%S.{millis}") + tz

def ax_api_signature(ts_for_sign: str, contact: str, code: str, contact_type: str) -> str:
    preimage = f"{ts_for_sign}password{contact_type}{contact}{code}openid"
    digest = hmac.new(AX_API_SIG_KEY_ASCII, preimage.encode("utf-8"), hashlib.sha256).digest()
    b64res = base64.b64encode(digest).decode("ascii")
    return b64res
    
def encryptsign_xdata(
        api_key: str,
        method: str,
        path: str,
        id_token: str,
        payload: dict
    ) -> str:
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }
    
    request_body = {
        "id_token": id_token,
        "method": method,
        "path": path,
        "body": payload
    }

    response = requests.request("POST", XDATA_ENCRYPT_SIGN_URL, json=request_body, headers=headers, timeout=30)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Encryption failed: {response.text}")
    
def decrypt_xdata(
    api_key: str,
    encrypted_payload: dict
    ) -> dict:
    if not isinstance(encrypted_payload, dict) or "xdata" not in encrypted_payload or "xtime" not in encrypted_payload:
        raise ValueError("Invalid encrypted data format. Expected a dictionary with 'xdata' and 'xtime' keys.")
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }
    
    response = requests.request("POST", XDATA_DECRYPT_URL, json=encrypted_payload, headers=headers, timeout=30)
    
    if response.status_code == 200:
        return response.json().get("plaintext")
    else:
        raise Exception(f"Decryption failed: {response.text}")

def get_x_signature_payment(
        api_key: str,
        access_token: str,
        sig_time_sec: int,
        package_code: str,
        token_payment: str,
        payment_method: str
    ) -> str:
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }
    
    request_body = {
        "access_token": access_token,
        "sig_time_sec": sig_time_sec,
        "package_code": package_code,
        "token_payment": token_payment,
        "payment_method": payment_method
    }
    
    response = requests.request("POST", PAYMENT_SIGN_URL, json=request_body, headers=headers, timeout=30)
    
    if response.status_code == 200:
        return response.json().get("x_signature")
    else:
        raise Exception(f"Signature generation failed: {response.text}")