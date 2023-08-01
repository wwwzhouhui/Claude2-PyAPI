import os
from flask import Flask, request, jsonify
from claude_api import Client
from dotenv import load_dotenv


app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def create_chat():
    data = request.get_json()
    prompt = data['prompt']

    cookie = get_cookie()
    client = Client(cookie)
    conversation = client.create_new_chat()
    conversation_id = conversation['uuid']

    response = client.send_message(prompt, conversation_id)
    return jsonify({'conversation_id': conversation_id, 'response': response})

@app.route('/chat/<conversation_id>')
def get_chat_history(conversation_id):
    cookie = get_cookie()
    client = Client(cookie)
    history = client.chat_conversation_history(conversation_id)
    return jsonify(history)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    conversation_id = data['conversation_id']
    prompt = data['prompt']


    cookie = get_cookie()
    client = Client(cookie)
    response = client.send_message(prompt, conversation_id)
    return jsonify({'response': response})

@app.route('/sendattachment', methods=['POST'])
def send_message_attachment():
    conversation_id = request.form.get("conversation_id")
    prompt = request.form.get("prompt")
    file = request.files['file']

    cookie = get_cookie()
    client = Client(cookie)
    file_path = None
    if file:
        file_path = save_upload_file(file)

    response = client.send_message(prompt, conversation_id,file_path)
    return jsonify({'response': response})

@app.route('/reset', methods=['POST'])
def reset_conversations():
    cookie = get_cookie()
    client = Client(cookie)
    result = client.reset_all()
    return jsonify({'result': result})

@app.route('/rename', methods=['POST'])
def rename_conversation():
    data = request.get_json()
    conversation_id = data['conversation_id']
    title = data['title']

    cookie = get_cookie()
    client = Client(cookie)
    result = client.rename_chat(title, conversation_id)
    return jsonify({'result': result})

@app.route('/upload', methods=['POST'])
def upload_attachment():
    file = request.files['file']
    if file:
        file_path = save_upload_file(file)
        cookie = get_cookie()
        client = Client(cookie)
        response = client.upload_attachment(file_path)
        return jsonify({'result': response})
    else:
        return jsonify({'error': 'No file uploaded'}), 400

def save_upload_file(file):
    uploads_dir = os.getenv('uploads')  # 从环境变量中获取上传文件目录
    print(uploads_dir)
    file_path = os.path.join(uploads_dir, file.filename)
    file.save(file_path)
    return file_path

@app.route('/conversations')
def list_all_conversations():
    cookie = get_cookie()
    client = Client(cookie)
    conversations = client.list_all_conversations()
    return jsonify(conversations)

@app.route('/history/<conversation_id>')
def chat_conversation_history(conversation_id):
    cookie = get_cookie()
    client = Client(cookie)
    history = client.chat_conversation_history(conversation_id)
    return jsonify(history)
# 加载.env文件中的环境变量
load_dotenv()
def get_cookie():
    #cookie = os.environ.get('cookie')
    cookie = os.getenv('cookie')
    print(cookie)
    if not cookie:
        raise ValueError("Please set the 'cookie' environment variable.")
    return cookie
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
    app.default_encoding = 'utf-8'