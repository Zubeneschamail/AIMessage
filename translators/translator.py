"""Translation module for AI news"""
import requests
from deep_translator import GoogleTranslator

# 设置请求超时
requests.adapters.DEFAULT_RETRIES = 1

def translate_to_chinese(text, max_length=4500, timeout=5):
    """Translate text from English to Chinese using Google Translate."""
    if not text or not text.strip():
        return text
    
    # Google Translate has a 5000 char limit per request
    if len(text) > max_length:
        text = text[:max_length]
    
    try:
        translator = GoogleTranslator(source='auto', target='zh-CN')
        translated = translator.translate(text)
        return translated if translated else text
    except Exception as e:
        # 翻译失败时返回原文
        return text

def translate_item(item):
    """Translate a single news item (title and summary)."""
    try:
        translated_title = translate_to_chinese(item['title'])
        # 限制摘要长度，减少翻译时间
        summary = item['summary'][:200] if item['summary'] else ''
        translated_summary = translate_to_chinese(summary)
        return {
            **item,
            'title': translated_title,
            'summary': translated_summary,
            'original_title': item['title']  # Keep original for reference
        }
    except Exception as e:
        # 翻译失败时返回原始item
        return item

def translate_items(items):
    """Translate a list of news items with error handling."""
    translated = []
    for i, item in enumerate(items):
        try:
            translated.append(translate_item(item))
        except Exception as e:
            print(f"[Translate] Skipping item {i+1}, using original")
            translated.append(item)  # 使用原文
    return translated
