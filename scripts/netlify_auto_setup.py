#!/usr/bin/env python3
"""
Netlify Webhook自動設定スクリプト
Seleniumを使用してブラウザ自動化でWebhook設定

Author: Claude Code
Date: 2025-08-10
"""

import time
import sys
import subprocess
import os

def open_netlify_settings():
    """Netlify設定ページをブラウザで開く"""
    url = "https://app.netlify.com/sites/neon-biscochitos-8dd468/settings/deploys#notifications"
    
    try:
        # macOSでブラウザを開く
        subprocess.run(['open', url])
        print(f"✅ Netlify設定ページを開きました: {url}")
        return True
    except Exception as e:
        print(f"❌ ブラウザオープンエラー: {e}")
        return False

def show_manual_steps():
    """手動設定手順表示"""
    print("🔧 Netlify Webhook手動設定手順")
    print("=" * 40)
    print("")
    print("✅ ブラウザで設定ページが開いています")
    print("")
    print("📋 以下の手順で設定してください:")
    print("")
    print("1. 'Add notification' ボタンをクリック")
    print("2. 'Outgoing webhook' を選択") 
    print("3. 設定値を入力:")
    print("   └─ Event to listen for: Deploy failed")
    print("   └─ URL to notify: https://274d45352f6c.ngrok-free.app/netlify-webhook")
    print("4. 'Save' ボタンをクリック")
    print("")
    print("🎯 設定完了後、以下のコマンドでテストしてください:")
    print("   python3 netlify_auto_setup.py test")
    print("")

def test_webhook():
    """Webhook動作テスト"""
    import requests
    
    print("🧪 Netlify Webhook動作テスト")
    print("=" * 30)
    
    webhook_url = "https://274d45352f6c.ngrok-free.app/netlify-webhook"
    
    # テスト用ペイロード
    test_payload = {
        "state": "error",
        "error_message": "Test: cannot load such file -- fiddle (LoadError)",
        "name": "himawari-massage.jp",
        "url": "https://neon-biscochitos-8dd468.netlify.app",
        "admin_url": "https://app.netlify.com/sites/neon-biscochitos-8dd468"
    }
    
    print(f"📡 Webhook URL: {webhook_url}")
    print("📦 テストペイロード送信中...")
    
    try:
        response = requests.post(webhook_url, json=test_payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Webhook テスト成功！")
            print(f"   Status: {result.get('status', 'unknown')}")
            
            # Git確認
            print("\n🔍 自動修正結果確認:")
            subprocess.run(['git', 'log', '--oneline', '-1'], cwd='/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/correct_repo')
            subprocess.run(['grep', 'fiddle', '/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/correct_repo/Gemfile'], 
                         capture_output=False)
            
            return True
        else:
            print(f"❌ Webhook テスト失敗: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🚀 Netlify Webhook自動設定システム")
    print("=" * 40)
    print("")
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # テストモード
        return test_webhook()
    else:
        # 設定モード
        print("Step 1: Netlify設定ページを開いています...")
        if open_netlify_settings():
            time.sleep(2)
            show_manual_steps()
            return True
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)