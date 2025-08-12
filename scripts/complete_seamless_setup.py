#!/usr/bin/env python3
"""
完全シームレス化セットアップスクリプト
GitHub/Netlify Webhook自動設定 + 疎通テスト

Author: Claude Code
Date: 2025-08-10
"""

import requests
import json
import time
import sys
import os
import subprocess
from pathlib import Path

# 設定
GITHUB_TOKEN = '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'
GITHUB_REPO = 'satoshi-kemmotsu/blog'
WEBHOOK_SECRET = 'himawari-webhook-secret-2025'

# ログディレクトリ
LOG_DIR = Path('/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/logs')
LOG_DIR.mkdir(exist_ok=True)

def get_ngrok_url():
    """ngrok公開URL取得"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if response.status_code == 200:
            tunnels = response.json().get('tunnels', [])
            for tunnel in tunnels:
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
        return None
    except:
        return None

def setup_github_webhook(webhook_url):
    """GitHub Webhook自動設定"""
    
    webhook_config = {
        "name": "web",
        "active": True,
        "events": [
            "push",
            "workflow_run",
            "workflow_job",
            "deployment_status"
        ],
        "config": {
            "url": f"{webhook_url}/github-webhook",
            "content_type": "json",
            "secret": WEBHOOK_SECRET,
            "insecure_ssl": "0"
        }
    }
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # 既存Webhook削除（重複回避）
    try:
        existing_hooks = requests.get(
            f'https://api.github.com/repos/{GITHUB_REPO}/hooks',
            headers=headers
        ).json()
        
        for hook in existing_hooks:
            if 'github-webhook' in hook.get('config', {}).get('url', ''):
                print(f"🗑️  既存Webhook削除中: {hook['id']}")
                requests.delete(
                    f'https://api.github.com/repos/{GITHUB_REPO}/hooks/{hook["id"]}',
                    headers=headers
                )
    except:
        pass
    
    # 新規Webhook作成
    try:
        response = requests.post(
            f'https://api.github.com/repos/{GITHUB_REPO}/hooks',
            headers=headers,
            json=webhook_config
        )
        
        if response.status_code == 201:
            hook_data = response.json()
            print("✅ GitHub Webhook設定完了")
            print(f"   ID: {hook_data['id']}")
            print(f"   URL: {webhook_config['config']['url']}")
            print(f"   Events: {len(webhook_config['events'])}個")
            return True
        else:
            print(f"❌ GitHub Webhook設定失敗: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ GitHub Webhook設定エラー: {str(e)}")
        return False

def test_webhook_connectivity(webhook_url):
    """Webhook疎通テスト"""
    
    # ヘルスチェック
    try:
        response = requests.get(f"{webhook_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Webhook サーバー疎通確認")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Time: {health_data.get('timestamp')}")
            return True
        else:
            print(f"❌ ヘルスチェック失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 疎通テストエラー: {str(e)}")
        return False

def test_github_webhook(webhook_url):
    """GitHub Webhook機能テスト"""
    
    # テストペイロード
    test_payload = {
        "action": "completed",
        "workflow_run": {
            "id": 99999,
            "name": "Test Workflow",
            "conclusion": "failure",
            "html_url": f"https://github.com/{GITHUB_REPO}/actions/runs/99999"
        },
        "repository": {
            "full_name": GITHUB_REPO,
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
            f"{webhook_url}/github-webhook",
            json=test_payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ GitHub Webhook機能テスト成功")
            return True
        else:
            print(f"❌ GitHub Webhook機能テスト失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ GitHub Webhookテストエラー: {str(e)}")
        return False

def test_error_auto_fix():
    """エラー自動修正機能テスト"""
    
    print("🧪 エラー自動修正機能テスト...")
    
    # Ruby gem不足エラーシミュレーション
    test_error = """
    bundler: failed to load command: jekyll
    cannot load such file -- ostruct (LoadError)
    cannot load such file -- fiddle (LoadError)
    Build failed due to a user error
    """
    
    # テスト用Netlify Webhook
    netlify_payload = {
        "state": "error",
        "error_message": test_error,
        "name": "himawari-massage.jp",
        "url": "https://neon-biscochitos-8dd468.netlify.app"
    }
    
    # 監視サーバーから直接エラー解析テスト
    sys.path.append('/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/scripts')
    
    try:
        from error_monitor_server import ErrorAnalyzer
        
        analyzer = ErrorAnalyzer()
        missing_gems = analyzer.analyze_ruby_gem_error(test_error)
        
        if missing_gems:
            print(f"✅ エラー解析成功: {len(missing_gems)}個のgem不足検出")
            for gem, fix in missing_gems:
                print(f"   - {gem}: {fix}")
            return True
        else:
            print("❌ エラー解析失敗")
            return False
            
    except Exception as e:
        print(f"❌ エラー解析テストエラー: {str(e)}")
        return False

def save_configuration(webhook_url):
    """設定情報の保存"""
    
    config = {
        "webhook_url": webhook_url,
        "github_repo": GITHUB_REPO,
        "setup_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active"
    }
    
    config_file = LOG_DIR / 'seamless_config.json'
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 設定保存完了: {config_file}")
        return True
    except Exception as e:
        print(f"❌ 設定保存エラー: {str(e)}")
        return False

def main():
    """完全シームレス化セットアップ実行"""
    
    print("🚀 完全シームレス化セットアップ開始")
    print("=" * 50)
    
    # Step 1: ngrok URL確認
    print("\n1. ngrok外部公開URL取得中...")
    webhook_url = get_ngrok_url()
    
    if not webhook_url:
        print("❌ ngrok URL取得失敗")
        print("   ngrokが起動していることを確認してください")
        print("   起動コマンド: ngrok http 8080")
        return False
    
    print(f"✅ Webhook URL: {webhook_url}")
    
    # Step 2: 疎通テスト
    print("\n2. 基本疎通テスト中...")
    if not test_webhook_connectivity(webhook_url):
        print("❌ 基本疎通テスト失敗")
        return False
    
    # Step 3: GitHub Webhook設定
    print("\n3. GitHub Webhook設定中...")
    if not setup_github_webhook(webhook_url):
        print("❌ GitHub Webhook設定失敗")
        return False
    
    # Step 4: 機能テスト
    print("\n4. Webhook機能テスト中...")
    github_test = test_github_webhook(webhook_url)
    error_test = test_error_auto_fix()
    
    # Step 5: 設定保存
    print("\n5. 設定保存中...")
    save_configuration(webhook_url)
    
    # 結果表示
    print("\n" + "=" * 50)
    print("🎯 シームレス化セットアップ結果")
    print(f"   ✅ ngrok外部公開: {webhook_url}")
    print(f"   ✅ GitHub Webhook: 設定完了")
    print(f"   {'✅' if github_test else '❌'} Webhook機能テスト")
    print(f"   {'✅' if error_test else '❌'} エラー自動修正")
    
    if github_test and error_test:
        print("\n🎉 完全シームレス化成功！")
        print("\n📋 これで以下が自動実行されます:")
        print("   • GitHub/Netlifyエラー自動検出")
        print("   • Ruby gem不足の自動修正")
        print("   • 自動コミット・プッシュ・再ビルド")
        print("   • 24時間365日の無人稼働")
        print("\n🔧 システム監視:")
        print(f"   ヘルスチェック: {webhook_url}/health")
        print("   ログ確認: tail -f /Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/logs/error_monitor.log")
        
        return True
    else:
        print("\n⚠️  一部機能に問題があります。手動確認が必要です。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)