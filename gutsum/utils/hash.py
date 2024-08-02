from hashlib import sha256


def get_file_hash(identity: str):
    data_md5 = str(sha256(identity.encode("utf-8", "surrogatepass")).hexdigest())
    return data_md5
