#!/usr/bin/env python3
"""
Netlify Webhook設定スクリプト
NetlifyのAPIを直接使用してWebhook設定を行う

Author: Claude Code  
Date: 2025-08-10
"""

import requests
import json
import subprocess
import sys

def get_netlify_token():
    """NetlifyのアクセストークンをCLIから取得"""
    try:
        # netlify statusを実行してトークンを確認
        result = subprocess.run(['netlify', 'status', '--json'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            # netlify configからトークン情報取得を試行
            config_result = subprocess.run(['netlify', 'api', 'getSite', 
                                          '-d', '{"site_id": "178502f5-7910-4db3-bfd1-ae57d99e9345"}'],
                                        capture_output=True, text=True)
            if config_result.returncode == 0:
                print("✅ Netlify認証確認済み")
                return True
        return False
    except Exception as e:
        print(f"❌ Netlify認証確認エラー: {e}")
        return False

def create_webhook_manual():
    """手動でWebhook設定手順を表示"""
    print("🔧 Netlify Webhook手動設定手順")
    print("=" * 40)
    print("")
    print("1. Netlify管理画面にアクセス:")
    print("   https://app.netlify.com/sites/neon-biscochitos-8dd468/settings/deploys#notifications")
    print("")
    print("2. 'Add notification' → 'Outgoing webhook' を選択")
    print("")
    print("3. 以下の設定を入力:")
    print("   Event to listen for: Deploy failed")
    print("   URL to notify: https://274d45352f6c.ngrok-free.app/netlify-webhook")
    print("")
    print("4. 'Save' をクリックして設定完了")
    print("")
    
def test_webhook():
    """Webhook動作テスト"""
    print("🧪 Netlify Webhook動作テスト実行")
    print("=" * 35)
    
    # テストペイロード
    test_payload = {
        "state": "error",
        "error_message": "Test deploy failure - cannot load such file -- fiddle (LoadError)",
        "name": "himawari-massage.jp", 
        "url": "https://neon-biscochitos-8dd468.netlify.app",
        "admin_url": "https://app.netlify.com/sites/neon-biscochitos-8dd468"
    }
    
    try:
        response = requests.post(
            "https://274d45352f6c.ngrok-free.app/netlify-webhook",
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Webhook テスト成功")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Webhook テスト失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook テストエラー: {e}")
        return False

def main():
    print("🚀 Netlify Webhook設定スクリプト")
    print("=" * 35)
    print("")
    
    # Step 1: 認証確認
    if get_netlify_token():
        print("✅ Netlify CLI認証済み")
    else:
        print("❌ Netlify CLI認証が必要です")
        return False
    
    # Step 2: 手動設定手順表示
    create_webhook_manual()
    
    # Step 3: Webhook動作確認
    print("👆 上記手順でWebhookを設定後、以下でテストしてください:")
    print("   python3 netlify_webhook_setup.py test")
    print("")
    
    # テストモードの場合
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        return test_webhook()
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)