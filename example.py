import requests

TOKEN = "YOUR_BOT_API_TOKEN"
url = f"https://api.telegram.org/bot{'7642183378:AAGgc1MG27OBkUbdUM2R_HaTx9IohsMZnTQ'}/getUpdates"

response = requests.get(url)
print(response.json())