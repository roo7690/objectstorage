from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv('.env.local')

def key():
  key={
    "endpoint":'localhost:9000',
    "access_key":"minioadmin",
    "secret_key":"minioadmin"
  }
  if os.getenv('mode')=='prod':
    key={
      "endpoint":os.getenv('SERVER_NAME'),
      "access_key":os.getenv('MINIO_ROOT_USER'),
      "secret_key":os.getenv('MINIO_ROOT_PASSWORD')
    }
  return key

Manager=Minio(**key(),
  cert_check=False,
  secure=False)