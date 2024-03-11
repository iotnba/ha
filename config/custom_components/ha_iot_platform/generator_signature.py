import hashlib
import hmac
import base64
from urllib.parse import quote
from datetime import datetime, timedelta


def assemble_token(version, resource_name, access_key):
    # 自动生成过期时间
    # 获取当前时间
    current_time = datetime.now()

    # 在当前时间上添加30天（3600秒 * 24小时 * 30天）
    new_time = current_time + timedelta(days=30)

    # 获取新时间的Epoch秒数
    epoch_second = int(new_time.timestamp())

    signature_method = "sha256"
    res = quote(resource_name, safe="")
    sig = quote(
        generator_signature(
            version, resource_name, epoch_second, access_key, signature_method
        ),
        safe="",
    )

    return f"version={version}&res={res}&et={expiration_time}&method={signature_method}&sign={sig}"


def generator_signature(
    version, resource_name, expiration_time, access_key, signature_method
):
    encrypt_text = f"{expiration_time}\n{signature_method}\n{resource_name}\n{version}"
    key = base64.b64decode(access_key)

    hashed = hmac.new(key, msg=encrypt_text.encode(), digestmod=hashlib.sha256)
    signature = base64.b64encode(hashed.digest()).decode()

    return signature


if __name__ == "__main__":
    # Example usage
    version = "2018-10-30"
    resource_name = "ppppp"
    expiration_time = "1111111111"  # Replace with your actual expiration time
    signature_method = "sha256"  # Replace with your actual signature method
    access_key = "222222222222"  # Replace with your actual access key

    token = assemble_token(version, resource_name, signature_method, access_key)
    print("Generated Token:", token)
