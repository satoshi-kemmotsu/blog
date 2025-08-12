#!/usr/bin/env python3
"""
エラー監視システムのテストスクリプト
Webhook・自動修正機能のテスト

Author: Claude Code
Date: 2025-08-10
"""

import requests
import json
import time
import sys

def test_github_webhook():
    """GitHub Webhookテスト"""
    
    # テスト用GitHub Webhook payload
    test_payload = {
        "action": "completed",
        "workflow_run": {
            "id": 12345,
            "name": "Build and Deploy",
            "conclusion": "failure",
            "html_url": "https://github.com/satoshi-kemmotsu/blog/actions/runs/12345"
        },
        "repository": {
            "full_name": "satoshi-kemmotsu/blog",
            "name": "blog"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "workflow_run",
        "X-Hub-Signature-256": "sha256=test-signature"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/github-webhook",
            json=test_payload,
            headers=headers
        )
        
        print(f"GitHub Webhook Test: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"GitHub Webhook Test Error: {str(e)}")
        return False

def test_netlify_webhook():
    """Netlify Webhookテスト"""
    
    # Ruby gem不足エラーのテストペイロード
    test_payload = {
        "id": "test-deploy-12345",
        "state": "error", 
        "name": "himawari-massage.jp",
        "url": "https://neon-biscochitos-8dd468.netlify.app",
        "admin_url": "https://app.netlify.com/sites/neon-biscochitos-8dd468/deploys/test-deploy-12345",
        "error_message": """
        bundler: failed to load command: jekyll (/opt/build/cache/bundle/ruby/3.4.0/bin/jekyll)
        /opt/buildhome/.local/share/mise/installs/ruby/3.4.5/lib/ruby/3.4.0/bundled_gems.rb:82:in 'Kernel.require': cannot load such file -- ostruct (LoadError)
        Build failed due to a user error: Build script returned non-zero exit code: 2
        """,
        "created_at": "2025-08-10T11:30:00.000Z"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/netlify-webhook", 
            json=test_payload,
            headers=headers
        )
        
        print(f"Netlify Webhook Test: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Netlify Webhook Test Error: {str(e)}")
        return False

def test_health_check():
    """ヘルスチェックテスト"""
    
    try:
        response = requests.get("http://localhost:5000/health")
        
        print(f"Health Check: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Timestamp: {data.get('timestamp')}")
            return True
        
        return False
        
    except Exception as e:
        print(f"Health Check Error: {str(e)}")
        return False

def test_auto_fix_simulation():
    """自動修正シミュレーション"""
    
    print("🧪 自動修正機能テスト...")
    
    # Ruby gem不足エラーをシミュレーション
    test_error_log = """
    bundler: failed to load command: jekyll
    cannot load such file -- ostruct (LoadError)
    cannot load such file -- fiddle (LoadError)
    Build failed due to a user error
    """
    
    # エラー解析器テスト
    from error_monitor_server import ErrorAnalyzer
    
    analyzer = ErrorAnalyzer()
    missing_gems = analyzer.analyze_ruby_gem_error(test_error_log)
    
    print(f"検出されたgem不足: {missing_gems}")
    
    if missing_gems:
        print("✅ エラー解析成功")
        return True
    else:
        print("❌ エラー解析失敗")
        return False

def main():
    """テスト実行メイン"""
    
    print("🧪 GitHub/Netlify エラー監視システム テスト開始")
    print("=" * 60)
    
    # サーバー起動確認
    print("\n1. ヘルスチェック...")
    health_ok = test_health_check()
    
    if not health_ok:
        print("❌ サーバーが起動していません")
        print("先に start_error_monitor.sh を実行してください")
        sys.exit(1)
    
    # テスト実行
    tests = [
        ("GitHub Webhook", test_github_webhook),
        ("Netlify Webhook", test_netlify_webhook), 
        ("自動修正シミュレーション", test_auto_fix_simulation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n2. {test_name} テスト...")
        
        try:
            if test_func():
                print(f"✅ {test_name} テスト成功")
                passed += 1
            else:
                print(f"❌ {test_name} テスト失敗")
        except Exception as e:
            print(f"❌ {test_name} テストエラー: {str(e)}")
    
    # 結果表示
    print("\n" + "=" * 60)
    print(f"🎯 テスト結果: {passed}/{total} 成功")
    
    if passed == total:
        print("🎉 全テスト成功！エラー監視システムが正常稼働しています。")
        print("\n📋 実運用での確認:")
        print("   1. GitHub/Netlifyで実際にビルドエラーを発生させる")
        print("   2. Webhook通知が届くか確認")
        print("   3. 自動修正・コミット・デプロイを確認")
    else:
        print("⚠️  一部テスト失敗。システム設定を再確認してください。")
    
    print("\n📊 システム監視ログ:")
    print("   tail -f /Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/logs/error_monitor.log")

if __name__ == '__main__':
    main()