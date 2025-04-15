# form.py
from fastapi import FastAPI, Form, File, UploadFile

app = FastAPI()


@app.post('/login')
def login(
        username: str = Form(...),
        password: str = Form(...),
        some_file: UploadFile = File(None),
):
    file_content = some_file.file.read().splitlines()
    return {
        'username': username,
        'password': password,
        'file': file_content
    }
