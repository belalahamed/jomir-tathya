"""
Encode Module is used to encode userid and password in login form
"""

import base64


def encode_user_type(user_type: str) -> str:
    """Encoding user type in base64 format with a special string"""

    encoded_user_type = "RGxycyMxMjM=" + base64.b64encode(user_type.encode()).decode()
    return encoded_user_type


def encode_user_id(user_id: str) -> str:
    """Encoding user id in base64 format with a special string"""

    encoded_user_id = "RGxycyMxMjM=" + base64.b64encode(user_id.encode()).decode()
    return encoded_user_id