"""
Configuration for Daily News Fetcher Bot
==========================================
Edit this file to customize your news sources and categories.
"""

# ─── Telegram Config (set via GitHub Secrets or environment variables) ───────
# TELEGRAM_BOT_TOKEN = "your_bot_token_here"
# TELEGRAM_CHAT_ID   = "your_chat_id_here"

# ─── RSS Feeds organized by category ─────────────────────────────────────────

RSS_FEEDS = {
    "market": [
        # 📈 Indian & International Markets
        "https://www.moneycontrol.com/rss/market.xml",                     # Moneycontrol Markets
        "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",  # ET Markets
        "https://www.coindesk.com/arc/outboundfeeds/rss/",                # CoinDesk (Crypto)
        "https://feeds.content.dowjones.io/public/rss/mw_topstories",     # MarketWatch
        "https://www.business-standard.com/rss/markets-106.rss",          # Business Standard Markets
    ],
    "business": [
        # 💼 Business & Startups
        "https://www.business-standard.com/rss/companies-101.rss",        # Business Standard Companies
        "https://economictimes.indiatimes.com/news/company/rssfeeds/13357310.cms",  # ET Companies
        "https://techcrunch.com/feed/",                                   # TechCrunch (startups)
        "https://www.inc.com/rss/",                                       # Inc. Magazine
        "https://www.business-standard.com/rss/startups-108.rss",         # BS Startups
    ],
    "ai": [
        # 🤖 AI & Technology
        "https://www.technologyreview.com/feed/",                         # MIT Technology Review
        "https://feeds.arstechnica.com/arstechnica/index",               # Ars Technica
        "https://www.theverge.com/rss/index.xml",                       # The Verge
        "https://hnrss.org/frontpage",                                   # Hacker News
        "https://www.artificialintelligence-news.com/feed/",             # AI News
    ],
    "india": [
        # 🇮🇳 India General News
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",     # Times of India
        "https://www.thehindu.com/news/national/feeder/default.rss",      # The Hindu
        "https://indianexpress.com/feed/",                               # Indian Express
        "https://www.business-standard.com/rss/india-103.rss",           # BS India
        "https://www.hindustantimes.com/rss/topnews",                    # Hindustan Times
    ],
    "international": [
        # 🌍 International News
        "http://feeds.bbci.co.uk/news/world/rss.xml",                    # BBC World
        "https://feeds.npr.org/1001/rss.xml",                            # NPR News
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",        # NYT World
        "https://www.theguardian.com/world/rss",                         # Guardian World
        "https://feeds.reuters.com/reuters/worldnews",                   # Reuters World
    ],
    "other": [
        # 📋 Catch-all / Miscellaneous
        "http://feeds.bbci.co.uk/news/technology/rss.xml",               # BBC Tech
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",     # NYT Home
        "https://feeds.npr.org/1002/rss.xml",                            # NPR US News
    ],
}

# ─── Category Keywords (for article classification) ─────────────────────────

CATEGORY_KEYWORDS = {
    "market": [
        # Indian Market
        "sensex", "nifty", "bse", "nse", "stock market", "share market",
        "ipo", "mutual fund", "mf", "sip", "sebi", "demat", "trading",
        "equity", "derivative", "f&o", "bullion", "commodity",
        # International Market
        "dow jones", "nasdaq", "s&p 500", "wall street", "stock exchange",
        "rbi", "repo rate", "inflation", "gdp growth", "fiscal",
        # Crypto
        "bitcoin", "ethereum", "crypto", "blockchain", "defi", "nft",
        "altcoin", "web3", "token",
        # Investment
        "gold price", "silver price", "investment", "portfolio",
        "dividend", "bonus share", "stock split", "bull run", "bear market",
        "market rally", "market crash", "volatility", "mutual fund scheme",
        "small cap", "mid cap", "large cap",
    ],
    "business": [
        "startup", "entrepreneur", "funding", "venture capital", "vc",
        "seed round", "series a", "series b", "unicorn", "valuation",
        "business", "enterprise", "revenue", "profit", "loss",
        "acquisition", "merger", "ipo filing", "drhp",
        "small business", "ecommerce", "d2c", "direct-to-consumer",
        "marketplace", "b2b", "b2c", "retail", "wholesale",
        "franchise", "business model", "pivot", "scale-up",
        "manufacturing", "supply chain", "logistics", "export", "import",
        "make in india", "atmanirbhar", "startup india",
        "new market", "market expansion", "global business",
    ],
    "ai": [
        "artificial intelligence", "machine learning", "deep learning",
        "ai", "llm", "large language model", "gpt", "chatgpt", "openai",
        "claude", "anthropic", "gemini", "bard", "copilot",
        "neural network", "computer vision", "nlp", "natural language",
        "generative ai", "genai", "diffusion model", "transformer",
        "stable diffusion", "midjourney", "dall-e",
        "autonomous", "self-driving", "robot", "robotics",
        "data science", "big data", "analytics", "predictive",
        "ai tool", "ai software", "ai initiative", "ai regulation",
        "ai safety", "alignment", "agi", "singularity",
        "fine-tuning", "rag", "retrieval augmented generation",
        "agent", "ai agent", "multi-modal", "multimodal",
    ],
    "india": [
        "india", "indian", "pm modi", "narendra modi", "government",
        "parliament", "supreme court", "high court", "judiciary",
        "policy", "law", "bill", "act", "amendment", "ordinance",
        "tax", "gst", "income tax", "direct tax", "indirect tax",
        "budget", "union budget", "economic survey",
        # Important events
        "election commission", "ec", "aadhaar", "upi", "digital india",
        "infrastructure", "highway", "railway", "metro",
        "defence", "army", "navy", "air force", "border",
        "disaster", "flood", "earthquake", "cyclone", "pandemic",
        "education", "healthcare", "ayushman bharat",
        "clean energy", "renewable", "solar", "green energy",
        "space", "isro", "chandrayaan", "gaganyaan",
    ],
    "international": [
        "world", "global", "international", "united nations", "un",
        "china", "beijing", "shanghai", "taiwan", "hong kong",
        "usa", "united states", "america", "washington", "white house",
        "russia", "moscow", "ukraine", "kremlin", "putin",
        "europe", "european union", "eu", "uk", "britain", "london",
        "nato", "g7", "g20", "brics", "imf", "world bank", "who",
        "middle east", "israel", "gaza", "iran", "saudi",
        "japan", "tokyo", "south korea", "seoul", "north korea",
        "australia", "canada", "germany", "france", "climate",
        "conflict", "war", "sanction", "treaty", "summit",
        "refugee", "humanitarian", "aid", "pandemic", "outbreak",
        "earthquake", "tsunami", "hurricane", "wildfire", "flood",
        "coup", "protest", "revolution", "democracy",
    ],
}


# ─── Settings ────────────────────────────────────────────────────────────────

MAX_ARTICLES_PER_CATEGORY = 5       # Max articles per category per run
MAX_ARTICLE_AGE_HOURS = 24          # Skip articles older than this
DEDUP_TIMEOUT_MINUTES = 30          # Time window for dedup across feeds
SEND_EMPTY_CATEGORIES = False       # Set True to show categories with no news
TITLE_MAX_LENGTH = 120              # Truncate long titles

# Emoji headers for each category in the Telegram message
CATEGORY_EMOJIS = {
    "market": "📈",
    "business": "💼",
    "ai": "🤖",
    "india": "🇮🇳",
    "international": "🌍",
    "other": "📋",
}

CATEGORY_DISPLAY_NAMES = {
    "market": "Market & Investments",
    "business": "Business & Startups",
    "ai": "AI & Technology",
    "india": "India News",
    "international": "International News",
    "other": "Other Highlights",
}
