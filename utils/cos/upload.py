# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

import time
import sys
import logging

from GameNews.settings import COS_SECRETKEY, COS_SECRETID, COS_REGION, COS_BUCKET

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

token = None  # 使用临时密钥需要传入Token，默认为空,可不填
config = CosConfig(Region=COS_REGION, SecretId=COS_SECRETID, SecretKey=COS_SECRETKEY, Token=token)  # 获取配置对象
client = CosS3Client(config)


def upload_img_byte_stream(file, file_name):
    """
    字节流上传文件
    """
    ts = time.time()
    response = client.put_object(
        Bucket=COS_BUCKET,
        Body=file,
        Key='image' + str(ts) + file_name
    )

    return response['ETag']
