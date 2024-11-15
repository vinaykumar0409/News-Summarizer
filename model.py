from transformers import pipeline

# Load the BART summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_article(article_text):
    if len(article_text) > 512:  # BART works best with texts shorter than 512 tokens
        article_text = article_text[:512]  # Truncate the text for summarization
    
    summary = summarizer(article_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Extend the display function to include summaries
def display_articles_with_summaries(articles):
    for idx, article in enumerate(articles, 1):
        print(f"\nArticle {idx}: {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"URL: {article['url']}")
        print(f"Description: {article['description']}")
        
        # Use article description or content for summarization
        summary = summarize_article(article['description'] or article.get('content', ''))
        print(f"Summary: {summary}")

# Test the summarization with the retrieved articles
topic = "climate change"
articles = get_news(topic)
display_articles_with_summaries(articles)