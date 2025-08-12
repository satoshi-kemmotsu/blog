#!/usr/bin/env python3
"""
GitHub/Netlify Webhook自動設定スクリプト
エラー監視システムのWebhook設定を自動化

Author: Claude Code  
Date: 2025-08-10
"""

import requests
import json
import os
import sys

# 設定
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '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')
NETLIFY_ACCESS_TOKEN = os.getenv('NETLIFY_ACCESS_TOKEN')
WEBHOOK_SERVER_URL = os.getenv('WEBHOOK_SERVER_URL', 'http://your-server.com')

GITHUB_REPO = 'satoshi-kemmotsu/blog'
NETLIFY_SITE_ID = 'neon-biscochitos-8dd468'

def setup_github_webhook():
    """GitHub Webhook設定"""
    
    webhook_config = {
        "name": "web",
        "active": True,
        "events": [
            "push",
            "workflow_run", 
            "workflow_job"
        ],
        "config": {
            "url": f"{WEBHOOK_SERVER_URL}/github-webhook",
            "content_type": "json",
            "secret": "himawari-github-webhook-secret-2025",
            "insecure_ssl": "0"
        }
    }
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{GITHUB_REPO}/hooks'
    
    try:
        response = requests.post(url, headers=headers, json=webhook_config)
        
        if response.status_code == 201:
            print("✅ GitHub Webhook設定完了")
            print(f"   URL: {webhook_config['config']['url']}")
            print(f"   Events: {webhook_config['events']}")
            return True
        else:
            print(f"❌ GitHub Webhook設定失敗: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ GitHub Webhook設定エラー: {str(e)}")
        return False

def setup_netlify_webhook():
    """Netlify Webhook設定"""
    
    if not NETLIFY_ACCESS_TOKEN:
        print("❌ NETLIFY_ACCESS_TOKEN not provided")
        return False
    
    webhook_config = {
        "event": "deploy_failed",
        "url": f"{WEBHOOK_SERVER_URL}/netlify-webhook"
    }
    
    headers = {
        'Authorization': f'Bearer {NETLIFY_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/hooks'
    
    try:
        response = requests.post(url, headers=headers, json=webhook_config)
        
        if response.status_code in [200, 201]:
            print("✅ Netlify Webhook設定完了")
            print(f"   URL: {webhook_config['url']}")
            print(f"   Event: {webhook_config['event']}")
            return True
        else:
            print(f"❌ Netlify Webhook設定失敗: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Netlify Webhook設定エラー: {str(e)}")
        return False

def setup_netlify_success_webhook():
    """Netlify 成功通知Webhook設定"""
    
    if not NETLIFY_ACCESS_TOKEN:
        return False
    
    webhook_config = {
        "event": "deploy_succeeded", 
        "url": f"{WEBHOOK_SERVER_URL}/netlify-webhook"
    }
    
    headers = {
        'Authorization': f'Bearer {NETLIFY_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/hooks'
    
    try:
        response = requests.post(url, headers=headers, json=webhook_config)
        
        if response.status_code in [200, 201]:
            print("✅ Netlify成功通知Webhook設定完了")
            return True
        else:
            print(f"❌ Netlify成功通知設定失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Netlify成功通知設定エラー: {str(e)}")
        return False

def check_existing_webhooks():
    """既存Webhook確認"""
    
    print("\n🔍 既存Webhook確認...")
    
    # GitHub確認
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        url = f'https://api.github.com/repos/{GITHUB_REPO}/hooks'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            hooks = response.json()
            print(f"📋 GitHub Webhook数: {len(hooks)}件")
            
            for hook in hooks:
                config = hook.get('config', {})
                print(f"   - ID: {hook['id']}, URL: {config.get('url', 'N/A')}")
        
    except Exception as e:
        print(f"GitHub Webhook確認エラー: {str(e)}")
    
    # Netlify確認
    if NETLIFY_ACCESS_TOKEN:
        headers = {
            'Authorization': f'Bearer {NETLIFY_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        try:
            url = f'https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/hooks'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                hooks = response.json()
                print(f"📋 Netlify Webhook数: {len(hooks)}件")
                
                for hook in hooks:
                    print(f"   - ID: {hook['id']}, Event: {hook['event']}, URL: {hook['url']}")
            
        except Exception as e:
            print(f"Netlify Webhook確認エラー: {str(e)}")

def main():
    """メイン実行"""
    
    print("🚀 GitHub/Netlify Webhook自動設定開始")
    print(f"Webhook Server: {WEBHOOK_SERVER_URL}")
    print(f"GitHub Repo: {GITHUB_REPO}")
    print(f"Netlify Site: {NETLIFY_SITE_ID}")
    print()
    
    # 既存確認
    check_existing_webhooks()
    
    # セットアップ実行
    success_count = 0
    
    if setup_github_webhook():
        success_count += 1
    
    if setup_netlify_webhook():
        success_count += 1
    
    if setup_netlify_success_webhook():
        success_count += 1
    
    print(f"\n🎯 設定完了: {success_count}/3")
    
    if success_count == 3:
        print("🎉 全Webhook設定完了！エラー自動監視システムが稼働開始します。")
    else:
        print("⚠️  一部設定に失敗。手動確認が必要です。")
    
    print("\n📋 次のステップ:")
    print("1. error_monitor_server.py を起動")
    print("2. Webhookサーバーを公開URL（ngrok等）で外部公開")
    print("3. テストビルドでエラー自動修正を確認")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        WEBHOOK_SERVER_URL = sys.argv[1]
        print(f"Webhook URL: {WEBHOOK_SERVER_URL}")
    
    main()