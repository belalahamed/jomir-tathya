import base64

# function to encode citizen user type
def encode_user_type(user_type_str='2'):
    encoded_user_type = "RGxycyMxMjM=" + base64.b64encode(user_type_str.encode()).decode()
    return encoded_user_type

# function to encode username or user id
def encode_user_id(username):
    encoded_user_id = "RGxycyMxMjM=" + base64.b64encode(username.encode()).decode()
    return encoded_user_id