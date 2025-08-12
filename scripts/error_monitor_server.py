#!/usr/bin/env python3
"""
GitHub/Netlify エラー自動監視システム
Claude Code統合による瞬時対応システム

Author: Claude Code
Date: 2025-08-10
"""

from flask import Flask, request, jsonify
import json
import requests
import hmac
import hashlib
import os
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 設定
GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', 'your-github-secret')
NETLIFY_WEBHOOK_SECRET = os.getenv('NETLIFY_WEBHOOK_SECRET', 'your-netlify-secret')
PROJECT_PATH = '/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/correct_repo'
CLAUDE_API_ENDPOINT = 'http://localhost:8080/claude-code'  # ローカルClaude Code API

class ErrorAnalyzer:
    """エラー解析・修正提案システム"""
    
    def __init__(self):
        self.common_fixes = {
            'csv': 'gem "csv" # Ruby 3.4対応',
            'logger': 'gem "logger" # Ruby 3.4対応', 
            'base64': 'gem "base64" # Ruby 3.4対応',
            'ostruct': 'gem "ostruct" # Ruby 3.4対応',
            'mutex_m': 'gem "mutex_m" # Ruby 3.4対応',
            'fiddle': 'gem "fiddle" # Ruby 3.4対応',
            'drb': 'gem "drb" # Ruby 3.4対応'
        }
    
    def analyze_ruby_gem_error(self, error_log):
        """Ruby gemエラーの自動解析"""
        missing_gems = []
        
        for gem_name, fix_line in self.common_fixes.items():
            if f"cannot load such file -- {gem_name}" in error_log:
                missing_gems.append((gem_name, fix_line))
        
        return missing_gems
    
    def analyze_jekyll_error(self, error_log):
        """Jekyllビルドエラーの解析"""
        issues = []
        
        if "Liquid syntax error" in error_log:
            issues.append("Liquid構文エラー: テンプレート構文を確認")
        
        if "YAML front matter" in error_log:
            issues.append("Front Matter構文エラー: YAML形式を確認")
        
        if "Layout 'post' does not exist" in error_log:
            issues.append("レイアウトファイル不足: _layouts/post.html確認")
        
        return issues

def verify_github_signature(payload_body, signature_header):
    """GitHub Webhook署名検証"""
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode('utf-8'), 
        payload_body, 
        hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

@app.route('/health')
def health_check():
    """ヘルスチェック"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    """GitHub Webhookエンドポイント"""
    try:
        signature = request.headers.get('X-Hub-Signature-256')
        payload_body = request.get_data()
        
        # 署名検証（セキュリティ）
        if not verify_github_signature(payload_body, signature):
            logger.warning("GitHub Webhook署名検証失敗")
            return jsonify({"error": "Invalid signature"}), 401
        
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')
        
        logger.info(f"GitHub Event: {event_type}")
        
        # Workflow run失敗の監視
        if event_type == 'workflow_run' and payload['action'] == 'completed':
            if payload['workflow_run']['conclusion'] == 'failure':
                handle_github_build_failure(payload)
        
        # Push時のビルド失敗監視
        elif event_type == 'push':
            # Push後のCI/CD状況を監視
            monitor_push_build_status(payload)
        
        return jsonify({"status": "processed"}), 200
        
    except Exception as e:
        logger.error(f"GitHub Webhookエラー: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/netlify-webhook', methods=['POST'])
def netlify_webhook():
    """Netlify Webhookエンドポイント"""
    try:
        payload = request.json
        
        logger.info(f"Netlify Event: {payload.get('state', 'unknown')}")
        
        # ビルド失敗時の処理
        if payload.get('state') == 'error':
            handle_netlify_build_failure(payload)
        
        # ビルド成功時の処理
        elif payload.get('state') == 'ready':
            logger.info(f"🎉 Netlify Deploy成功: {payload.get('url')}")
        
        return jsonify({"status": "processed"}), 200
        
    except Exception as e:
        logger.error(f"Netlify Webhookエラー: {str(e)}")
        return jsonify({"error": str(e)}), 500

def handle_github_build_failure(payload):
    """GitHub ビルド失敗処理"""
    workflow_name = payload['workflow_run']['name']
    repository = payload['repository']['full_name']
    run_id = payload['workflow_run']['id']
    
    logger.error(f"🚨 GitHub Build Failed: {workflow_name} in {repository}")
    
    # ログ取得してエラー解析
    try:
        # GitHub CLI経由でログ取得
        log_result = subprocess.run([
            'gh', 'run', 'view', str(run_id), '--repo', repository, '--log'
        ], capture_output=True, text=True)
        
        if log_result.returncode == 0:
            analyze_and_fix_github_error(log_result.stdout, repository)
        
    except Exception as e:
        logger.error(f"GitHub ログ取得エラー: {str(e)}")

def handle_netlify_build_failure(payload):
    """Netlify ビルド失敗処理"""
    site_name = payload.get('name', 'unknown')
    deploy_url = payload.get('admin_url', 'N/A')
    error_message = payload.get('error_message', 'No error message provided')
    
    logger.error(f"🚨 Netlify Build Failed: {site_name}")
    logger.error(f"Error: {error_message}")
    logger.error(f"Admin URL: {deploy_url}")
    
    # エラー詳細解析
    analyze_and_fix_netlify_error(error_message, payload)

def monitor_push_build_status(payload):
    """Push後のビルド状況監視"""
    repository = payload['repository']['full_name']
    commit_sha = payload['after']
    
    logger.info(f"Push監視開始: {repository} @ {commit_sha[:7]}")
    
    # 30秒後にビルド状況確認（非同期推奨）
    # 実装では celery やバックグラウンドタスクを使用

def analyze_and_fix_github_error(error_log, repository):
    """GitHub エラーの解析・修正実行"""
    analyzer = ErrorAnalyzer()
    
    # Ruby gem エラー解析
    missing_gems = analyzer.analyze_ruby_gem_error(error_log)
    jekyll_issues = analyzer.analyze_jekyll_error(error_log)
    
    if missing_gems:
        auto_fix_ruby_gems(missing_gems, repository)
    
    if jekyll_issues:
        for issue in jekyll_issues:
            logger.warning(f"Jekyll Issue: {issue}")

def analyze_and_fix_netlify_error(error_message, payload):
    """Netlify エラーの解析・修正実行"""
    analyzer = ErrorAnalyzer()
    
    # Ruby gem エラー解析
    missing_gems = analyzer.analyze_ruby_gem_error(error_message)
    
    if missing_gems:
        # 自動修正実行
        auto_fix_ruby_gems(missing_gems, "satoshi-kemmotsu/blog")
        
        logger.info(f"🔧 自動修正完了: {len(missing_gems)}個のgem追加")
        
        # Slack/メール通知（オプション）
        send_notification(f"Netlify Build Error自動修正: {missing_gems}")

def auto_fix_ruby_gems(missing_gems, repository):
    """Ruby gemの自動修正実行"""
    try:
        gemfile_path = Path(PROJECT_PATH) / 'Gemfile'
        
        if not gemfile_path.exists():
            logger.error("Gemfile not found")
            return
        
        # Gemfile読み込み
        with open(gemfile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 欠損gem追加
        gem_section = "# Ruby 3.4対応の必須gem（デフォルトから除外されたgem群）\n"
        
        for gem_name, fix_line in missing_gems:
            if f'gem "{gem_name}"' not in content:
                gem_section += f'{fix_line}\n'
                logger.info(f"Adding gem: {gem_name}")
        
        # Gemfileに追記
        if "# Ruby 3.4対応の必須gem" not in content:
            # Jekyll本体の後に挿入
            content = content.replace(
                'gem "jekyll", "~> 4.3.0"',
                f'gem "jekyll", "~> 4.3.0"\n\n{gem_section}'
            )
        else:
            # 既存セクションに追加
            content = content.replace(
                "# Ruby 3.4対応の必須gem（デフォルトから除外されたgem群）",
                gem_section.rstrip()
            )
        
        # ファイル保存
        with open(gemfile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Git commit & push
        commit_and_push_fix(missing_gems)
        
    except Exception as e:
        logger.error(f"自動修正エラー: {str(e)}")

def commit_and_push_fix(missing_gems):
    """修正をコミット・プッシュ"""
    try:
        os.chdir(PROJECT_PATH)
        
        # Git add
        subprocess.run(['git', 'add', 'Gemfile'], check=True)
        
        # Commit message生成
        gem_names = [gem[0] for gem in missing_gems]
        commit_msg = f"""自動修正: Ruby 3.4 gem追加 ({', '.join(gem_names)})

🤖 Error Monitor自動修正:
- Netlifyビルドエラー検出
- 不足gem自動追加: {gem_names}
- Ruby 3.4対応完了

Generated by Error Monitor System
Co-Authored-By: Claude <noreply@anthropic.com>"""
        
        # Git commit
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Git push
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        logger.info("🚀 自動修正コミット・プッシュ完了")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Git操作エラー: {str(e)}")

def send_notification(message):
    """通知送信（Slack/メール等）"""
    logger.info(f"📢 Notification: {message}")
    
    # TODO: Slack Webhook実装
    # TODO: メール通知実装

if __name__ == '__main__':
    logger.info("🚀 Error Monitor Server起動")
    logger.info(f"監視対象: {PROJECT_PATH}")
    
    # 開発環境での起動（ポート8080でAirPlay競合回避）
    app.run(host='0.0.0.0', port=8080, debug=True)