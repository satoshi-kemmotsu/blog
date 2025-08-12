#!/usr/bin/env python3
"""
Ruby 3.4 gem不足エラーのNetlifyシミュレーション
mutex_m gem不足をシミュレート

Author: Claude Code
Date: 2025-08-10
"""

import requests
import json
import time

def test_mutex_m_error():
    """mutex_m gem不足エラーをシミュレート"""
    
    # mutex_m gem不足エラー
    netlify_payload = {
        "id": "test-mutex-error-001",
        "site_id": "178502f5-7910-4db3-bfd1-ae57d99e9345",
        "state": "error",
        "name": "neon-biscochitos-8dd468",
        "url": "https://himawari-massage.jp",
        "admin_url": "https://app.netlify.com/sites/neon-biscochitos-8dd468",
        "error_message": """
Build script returned non-zero exit code: 2
bundler: failed to load command: jekyll
cannot load such file -- mutex_m (LoadError)
	from /opt/buildhome/.rvm/rubies/ruby-3.4.0/lib/ruby/3.4.0/rubygems/core_ext/kernel_require.rb:159:in `require'
	from /opt/buildhome/.rvm/rubies/ruby-3.4.0/lib/ruby/3.4.0/rubygems/core_ext/kernel_require.rb:159:in `rescue in require'
""",
        "deploy_time": 15,
        "branch": "main",
        "context": "production"
    }
    
    webhook_url = "https://274d45352f6c.ngrok-free.app/netlify-webhook"
    
    print("🧪 Ruby 3.4 mutex_m gem不足エラーテスト")
    print("=" * 40)
    print(f"📡 Webhook URL: {webhook_url}")
    print("🔥 エラー: cannot load such file -- mutex_m")
    print("")
    
    try:
        response = requests.post(webhook_url, json=netlify_payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Webhook送信成功！")
            print(f"📝 Response: {response.json()}")
            print("")
            print("⏳ 5秒待機して自動修正結果確認...")
            time.sleep(5)
            
            # Git確認
            import subprocess
            result = subprocess.run(
                ['git', 'log', '--oneline', '-3'],
                cwd='/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/correct_repo',
                capture_output=True,
                text=True
            )
            print(f"\n📋 最新コミット履歴:\n{result.stdout}")
            
            # Gemfile確認
            result = subprocess.run(
                ['grep', 'mutex_m', 
                 '/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/correct_repo/Gemfile'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ mutex_m gemが自動追加されました:\n{result.stdout}")
            else:
                print("❌ mutex_m gemが追加されていません")
                
            return True
        else:
            print(f"❌ Webhook送信失敗: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

if __name__ == '__main__':
    test_mutex_m_error()