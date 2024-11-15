# import os
# import requests
# from dotenv import load_dotenv

# # Load API key from .env file
# load_dotenv()
# NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# def get_news(topic, language='en'):
#     url = 'https://newsapi.org/v2/everything'
#     params = {
#         'q': topic,
#         'apiKey': NEWS_API_KEY,
#         'language': language,  # default to English, but can be changed
#         'pageSize': 5  # number of articles to retrieve (adjust as needed)
#     }
#     response = requests.get(url, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
#         articles = data.get('articles', [])
#         if articles:
#             print(f"Found {len(articles)} articles on '{topic}':")
#             return articles
#         else:
#             print("No articles found.")
#     else:
#         print(f"Failed to fetch news: {response.status_code}")
#     return []

# def display_articles(articles):
#     for idx, article in enumerate(articles, 1):
#         print(f"\nArticle {idx}: {article['title']}")
#         print(f"Source: {article['source']['name']}")
#         print(f"URL: {article['url']}")
#         print(f"Description: {article['description']}")

# # Test retrieval
# topic = "climate change"
# articles = get_news(topic)
# display_articles(articles)

# from transformers import pipeline

# # Load the BART summarization model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def summarize_article(article_text):
#     if len(article_text) > 512:  # BART works best with texts shorter than 512 tokens
#         article_text = article_text[:512]  # Truncate the text for summarization
    
#     summary = summarizer(article_text, max_length=130, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

# # Extend the display function to include summaries
# def display_articles_with_summaries(articles):
#     for idx, article in enumerate(articles, 1):
#         print(f"\nArticle {idx}: {article['title']}")
#         print(f"Source: {article['source']['name']}")
#         print(f"URL: {article['url']}")
#         print(f"Description: {article['description']}")
        
#         # Use article description or content for summarization
#         summary = summarize_article(article['description'] or article.get('content', ''))
#         print(f"Summary: {summary}")

# # Test the summarization with the retrieved articles
# topic = "climate change"
# articles = get_news(topic)
# display_articles_with_summaries(articles)


from transformers import pipeline
from GoogleNews import GoogleNews

# Initialize the summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_articles(articles):
    for idx, article in enumerate(articles, start=1):
        print(f"\nArticle {idx}: {article['title']}")
        print(f"URL: {article['link']}")
        print(f"Description: {article['desc']}")

        # Summarization
        try:
            # Using the description directly
            summary = summarizer(article['desc'], max_length=50, min_length=20, do_sample=False)[0]['summary_text']
            # Ensure summary is complete
            if len(summary.split()) < 10:
                summary = f"{article['desc'][:150]}... (Read more in the article)"
            print(f"Summary: {summary}\n")
        except Exception as e:
            print(f"Error summarizing article {idx}: {e}\n")

# Example usage
def fetch_news(topic="hacking"):
    googlenews = GoogleNews(lang="en")
    googlenews.search(topic)
    news = googlenews.result()[:5]
    return news

if __name__ == "__main__":
    topic = input("Enter a topic: ")  # User input for topic
    articles = fetch_news(topic)
    summarize_articles(articles)
