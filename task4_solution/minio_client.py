from minio import Minio
from minio.error import S3Error
import random
import string
import io

#חיבוק לשרת מיניו
client = Minio(
    "localhost:9000",
    access_key="NoaK",
    secret_key="@4110803",
    secure=False
)
bucket_name = "task4"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
#שם אקראי לאוביקטים
object_name = "file_" + ''.join(random.choices(string.digits, k=3)) + ".txt"
object_name1 = "file_" + ''.join(random.choices(string.digits, k=3)) + ".txt"
#תוכן אקראי לאוביקטים
object_content = "".join(random.choices(string.ascii_letters + string.digits + "\n", k=20))
object_content1 = "".join(random.choices(string.ascii_letters + string.digits + "\n", k=20))
#יצירת אוביקטים
client.put_object(
    bucket_name,
    object_name,
    io.BytesIO(object_content.encode("utf-8")),
    length=len(object_content.encode("utf-8")),
    content_type="text/plain"
)
client.put_object(
    bucket_name,
    object_name1,
    io.BytesIO(object_content1.encode("utf-8")),
    length=len(object_content1.encode("utf-8")),
    content_type="text/plain"
)
print(f"Created object: {object_name} with content: {object_content}")
print(f"Created object: {object_name1} with content: {object_content1}")

#שליפת אוביקטים
print("Objects in bucket:")
for obj in client.list_objects(bucket_name):
    print(f"- {obj.object_name}")
#שליפת אוביקט קיים
print(f"reading data of object: {object_name}")
response = client.get_object(bucket_name, object_name)
data = response.read().decode("utf-8")
response.close()
response.release_conn()
print(f"Data: {data}")
#מחיקת אוביקט
client.remove_object(bucket_name, object_name1)
print(f"Deleted object: {object_name1}")
#עידכון אוביקט
new_content = "Updated content1: " + "".join(random.choices(string.ascii_letters + string.digits + "\n", k=20))
client.put_object(
    bucket_name,
    object_name,
    io.BytesIO(new_content.encode("utf-8")),
    length=len(new_content.encode("utf-8")),
    content_type="text/plain"
)
#שליפת האוביקט המעודכן
print(f"reading data of updated object: {object_name}")
response = client.get_object(bucket_name, object_name)
data = response.read().decode("utf-8")
response.close()
response.release_conn()
print(f"Data: {data}")