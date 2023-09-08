import requests

proxies = {
  'http': 'http://127.0.0.1:10809',
  'https': 'http://127.0.0.1:10809',
}

response = requests.get('https://www.youtube.com/', proxies=proxies)
print(response.text)
