import uuid
import io
from pydub import AudioSegment
import boto3

from app import settings

# Let's use Amazon S3
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


def filename_generator(ext='wav'):
    return f"{str(uuid.uuid4())}.{ext}"


def convert_audio(file, ext: str):
    """
    Function to convert audio file
    :param file: file to convert
    :param ext: format to convert
    :return: converted audio file
    """

    sound = AudioSegment(file).export(format=ext)
    return sound.read()


def reverse_audio(file, name: str):
    """
    Function to reverse a audio
    :param file: file to reverse
    :param name: file name
    :return: dictionary containing file name and url
    """
    sound = AudioSegment.from_mp3(io.BytesIO(file.read())).reverse().export(format='mp3')
    url = upload_file_to_s3(sound.read(), name)
    return {'name': name, 'url': url}


def upload_file_to_s3(file, name: str) -> str:
    """
    Function to upload audio files to s3 bucket
    :param file: file to upload
    :param name: file name
    :return: url to access uploaded file from s3
    """

    s3.Bucket(settings.S3_BUCKET_NAME).put_object(Key=f"media/audio/{name}", Body=file)
    location = boto3.client('s3').get_bucket_location(Bucket=settings.S3_BUCKET_NAME)['LocationConstraint']
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, settings.S3_BUCKET_NAME, f"media/audio/{name}")

    return url


def get_file_from_s3(name: str):
    """
    Function to get file from s3
    :param name: file name on s3 bucket
    :return: file in byte code
    """
    file = s3_client.get_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=f"media/audio/{name}"
    )
    data = file['Body']

    return data
