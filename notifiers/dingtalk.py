import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
from config import settings

def _build_signed_url(webhook_url, secret):
    """为 Webhook URL 添加签名参数"""
    if not secret:
        return webhook_url
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"{webhook_url}&timestamp={timestamp}&sign={sign}"

def _send_to_webhook(webhook_config, title, text):
    """发送消息到单个 Webhook"""
    url = _build_signed_url(webhook_config['url'], webhook_config.get('secret'))
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        }
    }
    try:
        resp = requests.post(url, headers=headers, json=data)
        result = resp.json()
        if result.get('errcode') == 0:
            return True, "Success"
        else:
            return False, result.get('errmsg')
    except Exception as e:
        return False, str(e)

def send_markdown(title, text):
    """Send Markdown message to all configured DingTalk Webhooks."""
    if not settings.DINGTALK_WEBHOOKS:
        print("[DingTalk] No Webhooks configured.")
        return
    
    total = len(settings.DINGTALK_WEBHOOKS)
    success_count = 0
    
    for i, webhook in enumerate(settings.DINGTALK_WEBHOOKS, 1):
        ok, msg = _send_to_webhook(webhook, title, text)
        if ok:
            success_count += 1
            print(f"[DingTalk] Webhook {i}/{total}: Success")
        else:
            print(f"[DingTalk] Webhook {i}/{total}: Failed - {msg}")
    
    print(f"[DingTalk] Sent to {success_count}/{total} webhooks")
