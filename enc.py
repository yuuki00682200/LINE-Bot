from Crypto.Cipher import AES

import hashlib
import hmac
import base64

def get_hashed_text_with_secret_key(secret_key: str, payload: str, method = hashlib.sha256) -> str:
    return hmac.new(secret_key.encode("utf-8"), payload.encode("utf-8"), method).hexdigest()

def get_encrypt_data(payload: str, secret_key: str, vector: str):
    b64_payload = base64.b64encode(payload.encode("utf-8"))

    if len(b64_payload) % 16 != 0:
        for _ in range(16 - (len(b64_payload) % 16)):
            b64_payload += b"_"

    secret_key = hashlib.sha256(secret_key.encode("utf-8")).digest()
    vector = hashlib.md5(vector.encode("utf-8")).digest()

    aes = AES.new(secret_key, AES.MODE_CBC, vector)
    cipher_data = aes.encrypt(b64_payload)
    return base64.b64encode(cipher_data).decode("utf-8")

def get_decrypt_data(b64_cipher: str, secret_key: str, vector: str):
    cipher_data = base64.b64decode(b64_cipher.encode("utf-8"))

    secret_key = hashlib.sha256(secret_key.encode("utf-8")).digest()
    vector = hashlib.md5(vector.encode("utf-8")).digest()
    aes = AES.new(secret_key, AES.MODE_CBC, vector)

    b64_payload = aes.decrypt(cipher_data)
    return base64.b64decode(b64_payload.partition(b"_")[0]).decode("utf-8")


secret_key = "encrypted_mid_key"
mid = "u62b4fa33289fabbf0712b8d2f65a889c"
primary_key = get_hashed_text_with_secret_key(secret_key, mid)
print("primary key:", primary_key)

token = "9QJLuIM65ythiRCV9wMc.yRt6mYIFQ78heRJs9LQiNa.brbx6SnGaMrjksjfpNjjjUa2HAaYry9Iy7BfPMV0pVK0ZghDnvEVZUtMEdSv7CzM.abcdef"
enc_token = get_encrypt_data(token, mid, primary_key)
print("enc token:", enc_token)

token = get_decrypt_data(enc_token, mid, primary_key)
print("token:", token)

