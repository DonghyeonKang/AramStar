import slack 
import token

slack_token = token # 발급받은 Token 값
client = slack.WebClient(token=slack_token)

def sendToSlack(message):
    client.chat_postMessage(channel="#menu_scraping_log", text=message)