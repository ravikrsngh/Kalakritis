import json
import base64
import hashlib


def dict_to_base64(dictionary):
    json_string = json.dumps(dictionary)
    json_bytes = json_string.encode()
    base64_bytes = base64.b64encode(json_bytes)
    base64_string = base64_bytes.decode()
    return base64_string


def toSHA256(data):
    sha256_hash = hashlib.sha256(data.encode())
    hashed_data = sha256_hash.hexdigest()
    return hashed_data


def base64_to_dict(base64_string):
    binary_data = base64.b64decode(base64_string)
    json_string = binary_data.decode('utf-8')
    data = json.loads(json_string)
    return data
