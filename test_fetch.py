"""Quick test script to fetch one news item"""
import feedparser

# 测试多个RSS源
urls = [
    ('机器之心', 'https://rsshub.app/jiqizhixin'),
    ('量子位', 'https://rsshub.app/qbitai'),
    ('36氪AI', 'https://rsshub.app/36kr/information/ai'),
    ('Hacker News', 'https://hnrss.org/frontpage'),
]

for name, url in urls:
    print(f"\n正在抓取: {name} ({url})")
    try:
        feed = feedparser.parse(url)
        items = feed.entries
        print(f"抓取到 {len(items)} 条资讯")
        if items:
            break
    except Exception as e:
        print(f"错误: {e}")
        items = []
        continue

print()

if items:
    item = items[0]
    print("=" * 50)
    print(f"标题: {item['title']}")
    print(f"链接: {item['link']}")
    summary = item['summary'][:150] + "..." if len(item['summary']) > 150 else item['summary']
    print(f"摘要: {summary}")
    print("=" * 50)
else:
    print("未抓取到任何资讯，请检查网络或RSS源地址")
