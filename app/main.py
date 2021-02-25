import uvicorn
from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi import FastAPI, File

from app.utils import filename_generator, convert_audio, upload_file_to_s3, get_file_from_s3, reverse_audio

app = FastAPI()


class ReverbAudio(BaseModel):
    name: str
    price: int


@app.post("/upload/")
def upload_audio(file: bytes = File(...), ext: str = 'wav'):
    sound = convert_audio(file, ext)
    sound_name = filename_generator(ext)
    url = upload_file_to_s3(sound, sound_name)

    return JSONResponse({'name': sound_name, 'url': url})


@app.post("/reverse/")
def reverse_audio_endpoint(data: ReverbAudio):
    """
    Endpoint to reverse a audio file
    :param data: json data
    :return: Boolean value True if all go good or False if something wrong
    """

    data = data.dict()
    name = data.get('name')
    file = get_file_from_s3(name)

    response = reverse_audio(file, name)

    return JSONResponse(response)






@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

