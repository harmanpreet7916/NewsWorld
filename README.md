# 📰 Daily News Fetcher Bot

A **completely free** Python bot that fetches news from RSS feeds daily, categorizes them into topics, and sends a beautiful digest to your Telegram.

## ✨ Features

- ✅ **5 major news categories** — Market, Business, AI, India, International
- ✅ **20+ RSS feeds** — BBC, Reuters, NYT, TechCrunch, Times of India, and more
- ✅ **Smart categorization** — Uses keyword scoring to classify each article
- ✅ **Deduplication** — No duplicate articles across different feeds
- ✅ **Daily scheduling** — Runs automatically via GitHub Actions
- ✅ **Zero cost** — No paid APIs, no paid hosting, no credit card needed

## 📋 News Categories

| Category | Emoji | What's Covered |
|----------|-------|----------------|
| **Market & Investments** | 📈 | Indian stocks (Sensex/Nifty), mutual funds, crypto, gold/silver, international markets |
| **Business & Startups** | 💼 | Startups, funding news, new business models, global business trends |
| **AI & Technology** | 🤖 | New AI tools, LLMs (GPT, Claude, Gemini), robotics, tech breakthroughs |
| **India News** | 🇮🇳 | Indian policies, laws, government decisions, taxes, infrastructure |
| **International News** | 🌍 | Global events, geopolitics, world economy, climate |
| **Other Highlights** | 📋 | Catch-all for interesting news that doesn't fit above |

## 🚀 Setup Guide (10 minutes)

### Step 1: Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the prompts
3. Choose a name (e.g., `My Daily News`)
4. Choose a username (must end in `bot`, e.g., `MyDailyNewsBot`)
5. BotFather will give you a **token** — save it! It looks like:
   ```
   1234567890:ABCdefGHIjklmNOPqrstUVwxyz-1234567
   ```

### Step 2: Get Your Chat ID

1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Send `/start` — it will reply with your **Chat ID** (a number)
3. Save this ID

### Step 3: Fork / Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/daily-news-bot.git
cd daily-news-bot
```

### Step 4: Push to GitHub

Create a **public** repository on GitHub and push the code:

```bash
git init
git add .
git commit -m "Initial commit: Daily News Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/daily-news-bot.git
git push -u origin main
```

### Step 5: Add Secrets in GitHub

1. Go to your repo on GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add these two secrets:

| Secret Name | Value |
|-------------|-------|
| `TELEGRAM_BOT_TOKEN` | The token from BotFather |
| `TELEGRAM_CHAT_ID` | Your chat ID from @userinfobot |

### Step 6: Enable Workflows

1. Go to **Actions** tab in your repo
2. You should see the **"Daily News Digest"** workflow
3. Click **"Enable"** if prompted

### Step 7: Test It Manually

1. Go to **Actions** → **Daily News Digest** → **Run workflow**
2. Check the box for **"Send a test message immediately"**
3. Click **"Run workflow"**
4. Wait a minute and check your Telegram! 🎉

## ⏰ Schedule

The bot runs **daily at 7:00 AM IST** (1:30 AM UTC).
You can change this by editing the `cron` line in `.github/workflows/daily-news.yml`.

## 📝 Customization

### Add/Remove RSS Feeds

Edit `config.py` → `RSS_FEEDS` dictionary. Just add a URL to any category's list.

### Tweak Categorization

Edit `config.py` → `CATEGORY_KEYWORDS`. Add more keywords to improve article matching.

### Change Max Articles

Edit `config.py` → `MAX_ARTICLES_PER_CATEGORY`. Default is 5 per category.

## 🧪 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run in test mode (prints to console, no Telegram)
python news_fetcher.py --test

# Full run (requires TELEGRAM env vars)
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
python news_fetcher.py
```

## 📊 Sample Output

```
📰 Daily News Digest
──────────────────────────────

📈 Market & Investments
  1. Sensex rises 500 points amid positive global cues
     Market rallies on strong foreign investor buying
     _Moneycontrol_

  2. Bitcoin crosses $65,000 mark
     Crypto market sees renewed interest
     _CoinDesk_

💼 Business & Startups
  1. Indian edtech startup raises $50M in Series B
     Plans to expand to tier-2 cities
     _TechCrunch_

... (and more categories)
──────────────────────────────
📊 Summary: 18 articles across 5 categories
⚡ Powered by Free RSS Feeds + GitHub Actions
```

## ❓ FAQ

**Q: Is this really free?**
A: Yes! GitHub Actions gives 2000 free minutes/month. This bot uses ~1 minute per run = 100% free.

**Q: Will it hit any API limits?**
A: RSS feeds are free and unlimited. Telegram Bot API has no rate limits for regular use. GitHub Actions runs once daily — well within free limits.

**Q: Can I add more RSS feeds?**
A: Absolutely! Just add the URL to `config.py` under the right category.

**Q: What if an RSS feed stops working?**
A: The script gracefully skips failed feeds. Check the Actions logs if you notice missing news.

## 📜 License

MIT — Free for everyone. Use it, modify it, share it.
