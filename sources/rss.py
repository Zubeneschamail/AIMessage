import feedparser
import time

def fetch_feed(url):
    """Fetch and parse RSS feed."""
    try:
        # Some RSS sources might block default User-Agent, feedparser handles this reasonably well usually
        # If issues arise, might need to wrap with requests and custom headers
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries:
            item = {
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary if 'summary' in entry else '',
                # Handle published time safely
                'published': entry.published_parsed if 'published_parsed' in entry else time.localtime()
            }
            items.append(item)
        return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []
