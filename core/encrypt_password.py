import hashlib

def md5_hex(data: str) -> str:
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def md5_with_key(key: str, data: str) -> str:
    return md5_hex(data + key)

def encrypt_pass(password: str, salt: str) -> str:
    if not password:
        return ""

    md5_encrypted = md5_hex(password)
    salted_md5 = md5_with_key(salt, md5_encrypted)
    encrypted_password = sha256_hex(salted_md5)

    return encrypted_password