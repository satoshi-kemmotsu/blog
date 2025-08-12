#!/bin/bash
"""
GitHub/Netlify エラー自動監視システム起動スクリプト
本番運用レベルの自動監視システム

Author: Claude Code
Date: 2025-08-10
"""

set -e

echo "🚀 GitHub/Netlify エラー自動監視システム起動"

# 設定確認
PROJECT_DIR="/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

# 必要な環境変数設定
export GITHUB_TOKEN="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"
export GITHUB_WEBHOOK_SECRET="himawari-github-webhook-secret-2025"
export NETLIFY_WEBHOOK_SECRET="himawari-netlify-webhook-secret-2025"
export WEBHOOK_SERVER_URL="http://localhost:5000"

# 依存関係インストール
echo "📦 Python依存関係インストール中..."
pip3 install flask requests hmac hashlib pathlib

# ngrok確認（外部公開用）
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok available for public URL"
else
    echo "⚠️  ngrok not found - Webhookは localhost:5000 で起動"
    echo "   外部からのWebhook通知を受信するには ngrok が必要です"
fi

# ログディレクトリ作成
mkdir -p "$PROJECT_DIR/logs"

# プロセス確認・停止
if pgrep -f "error_monitor_server.py" > /dev/null; then
    echo "🛑 既存監視プロセス停止中..."
    pkill -f "error_monitor_server.py"
    sleep 2
fi

# バックグラウンド起動
echo "🎯 エラー監視サーバー起動中..."
cd "$SCRIPTS_DIR"

# nohup で永続化実行
nohup python3 error_monitor_server.py > "$PROJECT_DIR/logs/error_monitor.log" 2>&1 &
MONITOR_PID=$!

echo "✅ エラー監視システム起動完了"
echo "   PID: $MONITOR_PID" 
echo "   Log: $PROJECT_DIR/logs/error_monitor.log"
echo "   Health Check: http://localhost:5000/health"

# ngrok起動（オプション）
if command -v ngrok &> /dev/null; then
    echo "🌐 ngrok による外部公開開始..."
    nohup ngrok http 5000 > "$PROJECT_DIR/logs/ngrok.log" 2>&1 &
    NGROK_PID=$!
    
    sleep 3
    
    # ngrok URL取得
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*')
    
    if [ ! -z "$NGROK_URL" ]; then
        echo "🎉 Webhook公開URL: $NGROK_URL"
        echo "   GitHub Webhook: $NGROK_URL/github-webhook"  
        echo "   Netlify Webhook: $NGROK_URL/netlify-webhook"
        
        # Webhook設定実行
        echo "🔧 Webhook自動設定実行中..."
        python3 setup_webhooks.py "$NGROK_URL"
        
    else
        echo "❌ ngrok URL取得失敗"
    fi
fi

# 状態確認
sleep 2
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ システム正常稼働中"
else
    echo "❌ システム起動確認失敗"
    exit 1
fi

echo ""
echo "📋 監視システム情報:"
echo "   - GitHub Repository: satoshi-kemmotsu/blog"
echo "   - Netlify Site: neon-biscochitos-8dd468" 
echo "   - 監視対象: ビルドエラー・デプロイ失敗"
echo "   - 自動修正: Ruby gem不足、Jekyll構文エラー等"
echo ""
echo "🎯 使用方法:"
echo "   1. GitHub/Netlifyでビルドエラー発生"
echo "   2. Webhook経由で自動通知"
echo "   3. エラー解析・修正を自動実行"
echo "   4. 修正コミット・デプロイまで完全自動化"
echo ""
echo "📊 システム停止: pkill -f error_monitor_server.py"

# PID記録
echo "$MONITOR_PID" > "$PROJECT_DIR/logs/monitor.pid"
if [ ! -z "$NGROK_PID" ]; then
    echo "$NGROK_PID" > "$PROJECT_DIR/logs/ngrok.pid"
fi

echo "🚀 GitHub/Netlify エラー自動監視システム稼働開始！"