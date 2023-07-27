import os
from claude_api import Client

def get_cookie():
    #cookie = os.environ.get('cookie')
    cookie = os.getenv('cookie')
    if not cookie:
        raise ValueError("Please set the 'cookie' environment variable.")
    return cookie

def main():
    cookie = get_cookie()
    claude = Client(cookie)
    conversation_id = None

    print("欢迎使用claude2!")

    while True:
        user_input = input("你: ")

        if user_input.lower() == 'exit':
            print("谢谢你!")
            break

        if not conversation_id:
            conversation = claude.create_new_chat()
            conversation_id = conversation['uuid']

        response = claude.send_message(user_input, conversation_id)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
