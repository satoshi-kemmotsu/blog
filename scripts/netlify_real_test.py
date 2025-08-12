#!/usr/bin/env python3
"""
Netlify実際のビルドエラーシミュレーションテスト
実際のNetlifyエラーと同じ形式でWebhookを送信

Author: Claude Code
Date: 2025-08-10
"""

import requests
import json
import time

def test_real_netlify_error():
    """実際のNetlifyビルドエラーをシミュレート"""
    
    # 実際のNetlifyエラーメッセージ形式
    netlify_payload = {
        "id": "68981d4c680cc700089ac08b",
        "site_id": "178502f5-7910-4db3-bfd1-ae57d99e9345",
        "build_id": "68981d4c680cc700089ac08b",
        "state": "error",
        "name": "neon-biscochitos-8dd468",
        "url": "https://himawari-massage.jp",
        "ssl_url": "https://himawari-massage.jp",
        "admin_url": "https://app.netlify.com/sites/neon-biscochitos-8dd468",
        "deploy_url": "https://68981d4c680cc700089ac08b--neon-biscochitos-8dd468.netlify.app",
        "created_at": "2025-08-10T04:17:16.790Z",
        "updated_at": "2025-08-10T04:17:58.000Z",
        "error_message": """
Build script returned non-zero exit code: 2
bundler: failed to load command: jekyll (/opt/build/repo/vendor/bundle/ruby/3.4.0/bin/jekyll)
/opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/spec_set.rb:159:in `materialize': Could not find this_gem_does_not_exist-0.0.0 in any of the sources (Bundler::GemNotFound)
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/spec_set.rb:75:in `materialize'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/definition.rb:477:in `materialize'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/definition.rb:198:in `specs'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/definition.rb:246:in `specs_for'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/runtime.rb:18:in `setup'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler.rb:161:in `setup'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/setup.rb:20:in `block in <top (required)>'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/ui/shell.rb:136:in `with_level'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/ui/shell.rb:88:in `silence'
	from /opt/buildhome/.rvm/gems/ruby-3.4.0/gems/bundler-2.3.18/lib/bundler/setup.rb:20:in `<top (required)>'
	from <internal:/opt/buildhome/.rvm/rubies/ruby-3.4.0/lib/ruby/3.4.0/rubygems/core_ext/kernel_require.rb>:159:in `require'
	from <internal:/opt/buildhome/.rvm/rubies/ruby-3.4.0/lib/ruby/3.4.0/rubygems/core_ext/kernel_require.rb>:159:in `rescue in require'
	from <internal:/opt/buildhome/.rvm/rubies/ruby-3.4.0/lib/ruby/3.4.0/rubygems/core_ext/kernel_require.rb>:39:in `require'
""",
        "deploy_time": 42,
        "committer": "satoshi-kemmotsu",
        "branch": "main",
        "context": "production",
        "published_at": None
    }
    
    webhook_url = "https://274d45352f6c.ngrok-free.app/netlify-webhook"
    
    print("🧪 実際のNetlifyビルドエラーのシミュレーション")
    print("=" * 50)
    print(f"📡 Webhook URL: {webhook_url}")
    print("🔥 エラー内容: this_gem_does_not_exist が見つからない")
    print("")
    
    try:
        response = requests.post(webhook_url, json=netlify_payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Webhook送信成功！")
            print(f"📝 Response: {response.json()}")
            print("")
            print("⏳ 3秒待機して結果確認...")
            time.sleep(3)
            
            # Git確認
            import subprocess
            result = subprocess.run(
                ['git', 'log', '--oneline', '-1'],
                cwd='/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/correct_repo',
                capture_output=True,
                text=True
            )
            print(f"\n📋 最新コミット: {result.stdout.strip()}")
            
            # Gemfile確認
            result = subprocess.run(
                ['grep', '-E', 'this_gem_does_not_exist|mutex_m|drb', 
                 '/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/correct_repo/Gemfile'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"📦 Gemfileに追加されたgem:\n{result.stdout}")
            else:
                print("ℹ️  該当するgemは見つかりませんでした")
                
            return True
        else:
            print(f"❌ Webhook送信失敗: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

if __name__ == '__main__':
    test_real_netlify_error()