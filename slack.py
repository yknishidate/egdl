from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import openai
import egdl
import dotenv
import os

dotenv.load_dotenv()

# Slack API token
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_CHANNEL = "#dev"

# OpenAI API key
openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize(title, abstract):
    system = """与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。```
    タイトルの日本語訳
    ・要点1
    ・要点2
    ・要点3
    ```"""

    text = f"title: {title}\nabstract: {abstract}"
    print("text:", text)
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': text}
                ],
                temperature=0.25,
            )
    print("response:", response)
    # result = 
    # return f"{title}\n{result}\n"
    return response['choices'][0]['message']['content']

def post_message(message):
    client = WebClient(token=SLACK_API_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        print(f"Message posted: {response['ts']}")
    except SlackApiError as e:
        print(f"Error posting message: {e}")

def check_new_articles(title):
    posted_articles_file = "posted_articles.txt"
    posted_articles = []
    with open(posted_articles_file, "r") as f:
        for line in f:
            posted_articles.append(line.strip())
    
    if title in posted_articles:
        return False
    else:
        # add title to posted_articles
        with open(posted_articles_file, "a") as f:
            f.write(title + "\n")
        return True

def main():
    page_links = egdl.get_recently_added_links()

    new_articles = []
    for page_link in page_links:
        if check_new_articles(page_link.title):
            article = page_link.get_article()
            new_articles.append(article)
        
    if new_articles == []:
        message = "新しい論文はありませんでした。"
        post_message(message)
    else:
        message = "新しい論文が追加されました！\n"
        for article in new_articles:
            summary = summarize(article.title, article.abstract)
            message += f"<{article.url}|{article.title}>\n{summary}\n"
        post_message(message)

if __name__ == "__main__":
    main()
