import time
from config import settings
from storage import dedup
from sources import rss
from notifiers import dingtalk
from formatters import markdown
from translators import translator

def fetch_and_push_job():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting fetch job...")
    dedup.init_db(settings.DB_PATH)
    
    for source in settings.RSS_URLS:
        print(f"Checking {source['name']}...")
        items = rss.fetch_feed(source['url'])
        
        new_items = []
        for item in items:
            if not dedup.is_processed(settings.DB_PATH, item['link']):
                new_items.append(item)
        
        if not new_items:
            print(f"No new items for {source['name']}")
            continue
        
        # 限制每个源最多推送10条，避免首次运行推送过多
        if len(new_items) > 10:
            print(f"Found {len(new_items)} new items, limiting to latest 10")
            new_items = new_items[:10]
        else:
            print(f"Found {len(new_items)} new items for {source['name']}")
        
        # 翻译资讯 (如果开启)
        if settings.ENABLE_TRANSLATION:
            print(f"Translating {len(new_items)} items...")
            new_items = translator.translate_items(new_items)
        
        # Batch processing to avoid message size limits
        batch_size = 5
        for i in range(0, len(new_items), batch_size):
            batch = new_items[i:i+batch_size]
            md_text = markdown.format_items(source['name'], batch)
            
            if md_text:
                dingtalk.send_markdown(f"{source['name']} 更新", md_text)
                
                # Mark as processed after sending
                for item in batch:
                    dedup.mark_processed(settings.DB_PATH, item['link'])
                
                # Avoid rate limiting
                time.sleep(2)

def cleanup_job():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting cleanup job...")
    dedup.cleanup_old_records(settings.DB_PATH, settings.CLEANUP_DAYS_RETAIN)
