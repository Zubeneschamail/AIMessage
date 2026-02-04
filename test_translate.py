"""Test translation functionality"""
from translators.translator import translate_item

# 测试翻译一条资讯
test_item = {
    'title': 'OpenAI Announces GPT-5 With Revolutionary Reasoning Capabilities',
    'summary': 'OpenAI has unveiled its latest AI model, GPT-5, which demonstrates unprecedented reasoning and problem-solving abilities.',
    'link': 'https://example.com/test'
}

print('原文:')
print(f"  标题: {test_item['title']}")
print(f"  摘要: {test_item['summary']}")
print()

translated = translate_item(test_item)
print('翻译后:')
print(f"  标题: {translated['title']}")
print(f"  摘要: {translated['summary']}")
