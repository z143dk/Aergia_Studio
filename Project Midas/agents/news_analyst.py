import sys
import os
import logging
from googlesearch import search

# Add root to pass
sys.path.append(r"c:\Users\z143d\OneDrive\Desktop\Project Aergia")

from intelligence_router import router, TaskType

class NewsAnalyst:
    def __init__(self):
        self.role = "News Sentiment Analyst"
        
    def get_news_headlines(self, ticker):
        """
        Scrapes Google News headlines for the ticker.
        """
        query = f"{ticker} stock news"
        headlines = []
        try:
            # Fetch top 5 results
            results = search(query, num_results=5, advanced=True)
            for res in results:
                headlines.append(f"- {res.title} ({res.description})")
        except Exception as e:
            return f"News Fetch Error: {e}"
            
        return "\n".join(headlines) if headlines else "No recent news found."

    def analyze_sentiment(self, ticker):
        """
        Fetches news and uses Gemini Flash (SPEED task) for quick sentiment check.
        """
        headlines = self.get_news_headlines(ticker)
        
        system_prompt = (
            "You are a News Sentiment Analyst. "
            "Analyze the following headlines for immediate market impact to a $100 micro-account. "
            "Ignore generic market noise. Focus on lawsuits, earnings, or CEO changes. "
            "Output JSON: { 'sentiment': 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL', 'score': -1.0 to 1.0, 'summary': '...' }"
        )
        
        prompt = f"Ticker: {ticker}\nHeadlines:\n{headlines}"
        
        # Use SPEED (Gemini Flash) for fast text processing
        response = router.generate(prompt, task_type=TaskType.SPEED, system_prompt=system_prompt)
        return response

if __name__ == "__main__":
    news = NewsAnalyst()
    print(news.analyze_sentiment("TSLA"))
