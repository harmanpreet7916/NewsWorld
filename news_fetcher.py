#!/usr/bin/env python3
"""
Daily News Fetcher Bot 🤖📰
===========================
Fetches news from multiple RSS feeds, categorizes them, and sends
a beautiful daily report to your Telegram.

Usage:
    python news_fetcher.py

Environment Variables:
    TELEGRAM_BOT_TOKEN    - Your Telegram bot token (from BotFather)
    TELEGRAM_CHAT_ID      - Your Telegram chat/user ID
"""

import os
import re
import sys
import html
import time
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

import feedparser
import requests

# Try to import config, fallback to default paths
try:
    import config
except ImportError:
    print("ERROR: config.py not found! Make sure it's in the same directory.")
    sys.exit(1)

# ─── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ─── Helper Functions ────────────────────────────────────────────────────────

def get_today_date() -> str:
    """Return today's date as a readable string."""
    return datetime.now().strftime("%A, %B %d, %Y")


def clean_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return text.strip()


def truncate_text(text: str, max_length: int = config.TITLE_MAX_LENGTH) -> str:
    """Truncate text to max_length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rsplit(" ", 1)[0] + "..."


def extract_summary(entry) -> str:
    """Extract a clean summary from an RSS entry."""
    # Try common summary fields
    summary = ""

    if hasattr(entry, "summary") and entry.summary:
        summary = entry.summary
    elif hasattr(entry, "description") and entry.description:
        summary = entry.description
    elif hasattr(entry, "content") and entry.content:
        summary = entry.content[0].get("value", "")

    summary = clean_html(summary)

    # Truncate to first ~200 chars - try to end at sentence boundary
    if len(summary) > 200:
        truncated = summary[:200]
        # Find last sentence-ending punctuation
        for punct in [".", "!", "?"]:
            idx = truncated.rfind(punct)
            if idx > 80:  # Only split at sentence if we have enough context
                return truncated[: idx + 1].strip()
        # Fallback: last space
        idx = truncated.rfind(" ")
        if idx > 0:
            return truncated[:idx] + "..."
        return truncated + "..."

    return summary.strip()


def get_article_date(entry) -> Optional[datetime]:
    """Extract the published date from an RSS entry."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pass
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pass
    return None


def is_article_recent(entry) -> bool:
    """Check if article is within the configured max age."""
    pub_date = get_article_date(entry)
    if pub_date is None:
        return True  # No date = assume recent
    age = datetime.now(timezone.utc) - pub_date
    return age < timedelta(hours=config.MAX_ARTICLE_AGE_HOURS)


def article_id(entry) -> str:
    """Generate a unique ID for deduplication."""
    url = entry.get("link", "") or ""
    title = entry.get("title", "") or ""
    raw = (url + title).encode("utf-8")
    return hashlib.md5(raw).hexdigest()


# ─── Categorization Engine ───────────────────────────────────────────────────

def score_article(text: str, keywords: list) -> int:
    """
    Score an article text against a list of keywords.
    Returns the number of keyword matches found (case-insensitive).
    """
    text_lower = text.lower()
    score = 0
    for keyword in keywords:
        pattern = re.compile(r"\b" + re.escape(keyword.lower()) + r"\b")
        score += len(pattern.findall(text_lower))
    return score


def categorize_article(title: str, summary: str) -> str:
    """
    Determine which category an article belongs to based on keyword scoring.
    Returns the category key (e.g., 'market', 'business', etc.).
    """
    combined_text = f"{title} {summary}"

    scores = {}
    for category, keywords in config.CATEGORY_KEYWORDS.items():
        scores[category] = score_article(combined_text, keywords)

    # Find the best category
    best_category = "other"  # default
    best_score = 0

    for category, score in scores.items():
        if score > best_score:
            best_score = score
            best_category = category

    # If no keywords matched at all, still "other"
    return best_category


# ─── RSS Feed Fetcher ────────────────────────────────────────────────────────

def fetch_feed(url: str, timeout: int = 15) -> list:
    """Fetch and parse a single RSS feed, returning list of articles."""
    articles = []
    try:
        log.info(f"  Fetching: {url}")
        feed = feedparser.parse(url)

        if feed.bozo and not feed.entries:
            log.warning(f"  ⚠ Could not parse: {url}")
            return []

        for entry in feed.entries:
            if not is_article_recent(entry):
                continue

            title = entry.get("title", "Untitled")
            link = entry.get("link", "")
            summary = extract_summary(entry)

            articles.append({
                "title": clean_html(title),
                "link": link,
                "summary": summary,
                "source": feed.feed.get("title", url.split("/")[2]),
                "id": article_id(entry),
            })

    except Exception as e:
        log.warning(f"  ⚠ Error fetching {url}: {e}")

    return articles


def fetch_all_feeds() -> dict:
    """Fetch all RSS feeds and categorize articles."""
    # Initialize ALL possible categories (from CATEGORY_KEYWORDS) to handle
    # cases where RSS_FEEDS doesn't include a category like "other"
    all_possible_categories = set(config.CATEGORY_KEYWORDS.keys()) | set(config.RSS_FEEDS.keys())
    categorized = {cat: [] for cat in all_possible_categories}
    all_articles = []
    seen_ids = set()

    log.info(f"📡 Fetching news from {sum(len(v) for v in config.RSS_FEEDS.values())} RSS feeds...")

    for category, urls in config.RSS_FEEDS.items():
        for url in urls:
            articles = fetch_feed(url)
            for article in articles:
                # Deduplicate across ALL feeds
                if article["id"] in seen_ids:
                    continue
                seen_ids.add(article["id"])

                # Determine the best category
                assigned_category = categorize_article(
                    article["title"], article["summary"]
                )

                article_entry = {
                    "title": article["title"],
                    "link": article["link"],
                    "summary": article["summary"],
                    "source": article["source"],
                }

                # Use setdefault to handle any unexpected category gracefully
                categorized.setdefault(assigned_category, []).append(article_entry)
                all_articles.append(article_entry)

    log.info(f"✅ Collected {len(all_articles)} unique articles total")

    # Sort by category and limit per category
    for category in categorized:
        categorized[category] = categorized[category][
            : config.MAX_ARTICLES_PER_CATEGORY
        ]

    return categorized


# ─── Telegram Integration ────────────────────────────────────────────────────

def get_bot_config() -> tuple:
    """Get Telegram bot token and chat ID from environment."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token:
        log.error(
            "❌ TELEGRAM_BOT_TOKEN not set!\n"
            "   Set it as an environment variable or in GitHub Secrets."
        )
    if not chat_id:
        log.error(
            "❌ TELEGRAM_CHAT_ID not set!\n"
            "   Set it as an environment variable or in GitHub Secrets."
        )

    return token, chat_id


def escape_html(text: str) -> str:
    """Escape text for safe use in HTML parse_mode."""
    return html.escape(text, quote=False)


def escape_html_attr(text: str) -> str:
    """Escape text for use in HTML attributes (escapes quotes too)."""
    return html.escape(text, quote=True)


def format_category_section_html(category: str, articles: list) -> str:
    """Format a category section for the Telegram message (HTML parse_mode)."""
    emoji = config.CATEGORY_EMOJIS.get(category, "📌")
    display_name = escape_html(config.CATEGORY_DISPLAY_NAMES.get(category, category.title()))

    if not articles:
        if config.SEND_EMPTY_CATEGORIES:
            return f"{emoji} <b>{display_name}</b>\n  <i>No news today</i>\n\n"
        return ""

    section = [f"{emoji} <b>{display_name}</b>"]

    for i, article in enumerate(articles, 1):
        title = truncate_text(article["title"])
        summary = article["summary"]
        link = article["link"]
        source = article["source"]

        # Escape special HTML characters in text content
        safe_title = escape_html(title)
        safe_summary = escape_html(summary)
        safe_source = escape_html(source)

        # Clean links: escape quotes to prevent HTML injection in href
        safe_link = escape_html_attr(link.strip())

        # Format the article entry using HTML
        section.append(f"\n  {i}. <a href=\"{safe_link}\">{safe_title}</a>")
        if safe_summary:
            # Replace newlines with spaces in summary for clean display
            clean_summary = safe_summary.replace("\n", " ").replace("\r", "")
            section.append(f"     <i>{clean_summary}</i>")
        section.append(f"     <i>{safe_source}</i>")

    section.append("")  # spacing after category
    return "\n".join(section)


MAX_TELEGRAM_LENGTH = 4096


def build_telegram_messages(categorized_articles: dict) -> list:
    """
    Build the Telegram message(s) with all categories.
    Returns a list of message strings, splitting if > 4096 chars.
    """
    today = get_today_date()
    safe_today = escape_html(today)

    header = f"📰 <b>Daily News Digest</b>\n📅 <i>{safe_today}</i>\n"
    separator = "─" * 30

    category_order = ["market", "business", "ai", "india", "international", "other"]

    # Track total articles across categories
    total_articles = 0
    active_categories = 0
    for cat in category_order:
        articles = categorized_articles.get(cat, [])
        total_articles += len(articles)
        if articles:
            active_categories += 1

    # Build footer
    safe_footer = escape_html(
        f"Summary: {total_articles} articles across {active_categories} categories"
    )
    footer = (
        f"\n📊 <i>{safe_footer}</i>\n"
        f"⚡ <i>Powered by Free RSS Feeds + GitHub Actions</i>"
    )

    # Build individual category sections
    category_sections = []
    for category in category_order:
        articles = categorized_articles.get(category, [])
        section = format_category_section_html(category, articles)
        if section:
            category_sections.append(section)

    # Try to fit everything in one message
    full_message = header + separator + "\n" + "\n".join(category_sections) + footer

    if len(full_message) <= MAX_TELEGRAM_LENGTH:
        return [full_message]

    # Need to split - send header + first categories, then remaining categories, then footer
    messages = []
    current_parts = [header, separator]

    for section in category_sections:
        preview = "\n".join(current_parts + [section])
        if len(preview) > MAX_TELEGRAM_LENGTH - 100:  # Leave room for continuation note
            # Cap current message
            # Add part X of Y indicator
            messages.append("\n".join(current_parts))
            # Start new message
            current_parts = [section]
        else:
            current_parts.append(section)

    # Add remaining sections and footer to last message
    current_parts.append(footer)
    messages.append("\n".join(current_parts))

    # Add page indicators if split
    if len(messages) > 1:
        for i in range(len(messages)):
            page_tag = f"\n\n<i>Page {i+1} of {len(messages)}</i>"
            messages[i] += page_tag

    return messages


def send_telegram_message(message: str, token: str, chat_id: str) -> bool:
    """Send a message via Telegram Bot API with retry logic."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            log.info(f"📤 Sending message to Telegram (chat_id: {chat_id})...")
            response = requests.post(url, json=payload, timeout=20)
            data = response.json()

            if data.get("ok"):
                log.info("✅ Message sent successfully!")
                return True
            else:
                error_desc = data.get("description", "Unknown error")
                log.error(f"❌ Telegram API error: {error_desc}")

                # Don't retry on bad request errors
                if "can't parse entities" in error_desc.lower() or "bad request" in error_desc.lower():
                    log.error("   Fatal API error, not retrying.")
                    return False

        except requests.exceptions.Timeout:
            log.warning(f"⏱ Timeout (attempt {attempt+1}/{max_retries+1})")
        except requests.exceptions.ConnectionError as e:
            log.warning(f"🔌 Connection error (attempt {attempt+1}/{max_retries+1}): {e}")
        except requests.exceptions.RequestException as e:
            log.warning(f"⚠ Network error (attempt {attempt+1}/{max_retries+1}): {e}")

        if attempt < max_retries:
            wait = 2 ** attempt  # exponential backoff: 1s, 2s
            log.info(f"   Retrying in {wait}s...")
            time.sleep(wait)

    log.error("❌ All retry attempts failed")
    return False


# ─── Main ────────────────────────────────────────────────────────────────────

def send_all_messages(messages: list, token: str, chat_id: str) -> bool:
    """Send all message parts to Telegram. Returns True if all succeeded."""
    all_success = True
    for i, msg in enumerate(messages):
        log.info(f"📤 Sending message {i+1} of {len(messages)}...")
        success = send_telegram_message(msg, token, chat_id)
        if not success:
            all_success = False
            log.error(f"❌ Failed to send message {i+1}")
        # Small delay between messages to avoid rate limiting
        if i < len(messages) - 1:
            time.sleep(0.5)
    return all_success


def main():
    """Main entry point."""
    print("\n" + "=" * 50)
    print("  📰 Daily News Fetcher Bot")
    print("=" * 50 + "\n")

    # Get Telegram config
    token, chat_id = get_bot_config()

    if not token or not chat_id:
        log.error(
            "Cannot proceed without Telegram credentials.\n"
            "Make sure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set."
        )
        sys.exit(1)

    # Fetch and categorize all articles
    start_time = time.time()
    categorized = fetch_all_feeds()

    # Build the message(s)
    messages = build_telegram_messages(categorized)
    elapsed = time.time() - start_time

    # Print stats
    total = sum(len(v) for v in categorized.values())
    log.info(f"📊 Total articles: {total}")
    for cat, articles in categorized.items():
        if articles:
            log.info(f"   {config.CATEGORY_EMOJIS.get(cat, '📌')} {cat}: {len(articles)} articles")

    log.info(f"⏱ Fetched & categorized in {elapsed:.1f}s")
    log.info(f"📏 Message will be sent in {len(messages)} part(s)")

    # Save a local copy for debugging
    debug_path = f"news_digest_{datetime.now().strftime('%Y%m%d')}.md"
    try:
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(messages[0] if messages else "")
        log.info(f"💾 Saved local copy: {debug_path}")
    except Exception as e:
        log.warning(f"⚠ Could not save local copy: {e}")

    # Send to Telegram
    success = send_all_messages(messages, token, chat_id)

    if success:
        print("\n" + "=" * 50)
        print("  ✅ News digest sent successfully!")
        print("=" * 50 + "\n")
    else:
        print("\n" + "=" * 50)
        print("  ⚠ News digest partially sent (some messages failed)")
        print("=" * 50 + "\n")
        sys.exit(1)


def test_local():
    """
    Run a local test without Telegram (prints to console).
    Use: python news_fetcher.py --test
    """
    print("\n" + "=" * 50)
    print("  🧪 LOCAL TEST MODE")
    print("=" * 50 + "\n")

    # Save and restore feeds to avoid mutating global config
    original_feeds = config.RSS_FEEDS
    try:
        config.RSS_FEEDS = {
            "ai": original_feeds["ai"][:2],
            "market": original_feeds["market"][:2],
            "india": original_feeds["india"][:2],
        }

        categorized = fetch_all_feeds()
        messages = build_telegram_messages(categorized)

        print("\n" + "─" * 50)
        print(f"📄 PREVIEW ({len(messages)} message(s)):")
        print("─" * 50)
        for i, msg in enumerate(messages):
            if len(messages) > 1:
                print(f"\n─── Message {i+1} of {len(messages)} ───")
            print(msg)
        print("─" * 50)
        print(f"\n📊 Total articles categorized and formatted successfully.")
        print("✓ Local test complete (no message sent to Telegram)")
    finally:
        config.RSS_FEEDS = original_feeds


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_local()
    else:
        main()
