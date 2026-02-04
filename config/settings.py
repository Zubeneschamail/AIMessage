import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# DingTalk Config - 支持多个 Webhook
# 格式: "url1|secret1,url2|secret2" 或 "url1,url2" (无密钥)
def parse_webhooks(webhooks_str):
    """解析多个 Webhook 配置"""
    if not webhooks_str:
        return []
    result = []
    for item in webhooks_str.split(','):
        item = item.strip()
        if not item:
            continue
        if '|' in item:
            url, secret = item.split('|', 1)
            result.append({'url': url.strip(), 'secret': secret.strip()})
        else:
            result.append({'url': item, 'secret': None})
    return result

DINGTALK_WEBHOOKS = parse_webhooks(os.getenv('DINGTALK_WEBHOOKS', ''))
# 兼容旧配置
if not DINGTALK_WEBHOOKS and os.getenv('DINGTALK_WEBHOOK'):
    DINGTALK_WEBHOOKS = [{
        'url': os.getenv('DINGTALK_WEBHOOK'),
        'secret': os.getenv('DINGTALK_SECRET')
    }]

# Database Config
DB_PATH = BASE_DIR / 'storage' / 'dedup.db'
CLEANUP_DAYS_RETAIN = int(os.getenv('CLEANUP_DAYS_RETAIN', 30))

# Schedule Config - 推送时间 (小时，逗号分隔)
PUSH_HOURS = os.getenv('PUSH_HOURS', '8,12,18')

# Translation Config - 是否开启翻译
ENABLE_TRANSLATION = os.getenv('ENABLE_TRANSLATION', 'true').lower() == 'true'

# RSS Sources - 精选AI资讯源
RSS_URLS = [
    {'name': 'TechCrunch AI', 'url': 'https://techcrunch.com/category/artificial-intelligence/feed/'},
]
