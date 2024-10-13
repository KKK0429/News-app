import streamlit as st
import requests
from newspaper import Article
from textblob import TextBlob
import nltk

nltk.download('punkt')

# Function to get news data from the API
def get_news():
    url = "https://google-news13.p.rapidapi.com/business?lr=en-US"
    headers = {
        'x-rapidapi-key': "x-rapidapi-key",
        'x-rapidapi-host': "-rapidapi-host"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to summarize the article
def summarize_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()  # This performs natural language processing to extract summary

        analysis = TextBlob(article.text)
        sentiment = "positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"

        return {
            "title": article.title,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "summary": article.summary,
            "sentiment": sentiment
        }
    except Exception as e:
        return {"error": str(e)}

# Streamlit app layout
st.title("Top Business News and Summaries")

# Fetch news
news_data = get_news()

if news_data:
    for article in news_data['articles']:
        st.subheader(article['title'])
        st.write(f"Source: {article['source']['title']}")
        st.write(f"Published At: {article['publishedAt']}")
        st.write(f"[Read Full Article]({article['url']})")

        # Summarize the article
        summary_data = summarize_article(article['url'])
        if "error" in summary_data:
            st.write("Error summarizing the article:", summary_data['error'])
        else:
            st.write("**Summary**:")
            st.write(summary_data['summary'])
            st.write(f"**Sentiment:** {summary_data['sentiment']}")
            st.write("---")
else:
    st.write("Error fetching the news.")