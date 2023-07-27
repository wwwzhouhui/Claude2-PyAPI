from fastapi import FastAPI, BackgroundTasks,File, UploadFile
from claude_api import Client
import os

app = FastAPI()

def get_cookie():
    #cookie = os.environ.get('cookie')
    cookie = os.getenv('cookie')
    if not cookie:
        raise ValueError("Please set the 'cookie' environment variable.")
    return cookie

@app.post("/chat")
async def create_chat(prompt: str, background_tasks: BackgroundTasks):
    cookie = get_cookie()
    client = Client(cookie)

    conversation = client.create_new_chat()
    conversation_id = conversation['uuid']

    background_tasks.add_task(client.send_message, prompt, conversation_id)
    return {"conversation_id": conversation_id}

@app.get("/chat/{conversation_id}")
async def get_chat_history(conversation_id):
    cookie = get_cookie()
    client = Client(cookie)

    history = client.chat_conversation_history(conversation_id)
    return history

@app.post("/send")
async def send_message(conversation_id: str, prompt: str):
    cookie = get_cookie()
    client = Client(cookie)

    response = client.send_message(prompt, conversation_id)
    return {"response": response}

@app.post("/reset")
async def reset_conversations():
    cookie = get_cookie()
    client = Client(cookie)

    result = client.reset_all()
    return {"result": result}

@app.post("/rename")
async def rename_conversation(conversation_id: str, title: str):
    cookie = get_cookie()
    client = Client(cookie)

    result = client.rename_chat(title, conversation_id)
    return {"result": result}


@app.post("/upload")
async def upload_attachment(file: UploadFile):
    cookie = get_cookie()
    client = Client(cookie)

    file_path = save_upload_file(file)
    response = client.upload_attachment(file_path)
    return {"result": response}


def save_upload_file(uploaded_file):
    file_path = f"{uploaded_file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())
    return file_path


@app.get("/conversations")
async def list_all_conversations():
    cookie = get_cookie()
    client = Client(cookie)

    conversations = client.list_all_conversations()
    return {"conversations": conversations}


@app.get("/history/{conversation_id}")
async def chat_conversation_history(conversation_id):
    cookie = get_cookie()
    client = Client(cookie)

    history = client.chat_conversation_history(conversation_id)
    return {"history": history}