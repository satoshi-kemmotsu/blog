#!/bin/bash
"""
ngrok認証設定スクリプト
完全シームレス化のためのngrok設定

Author: Claude Code
Date: 2025-08-10
"""

echo "🔐 ngrok認証設定ガイド"
echo "======================"
echo ""
echo "📋 手順:"
echo "1. https://dashboard.ngrok.com/signup でアカウント作成"
echo "2. https://dashboard.ngrok.com/get-started/your-authtoken で認証トークン確認"
echo "3. 下記コマンドで認証トークンを設定:"
echo ""
echo "   ngrok config add-authtoken YOUR_TOKEN_HERE"
echo ""
echo "💡 認証トークンを取得したら以下を実行してください:"
echo ""

# ユーザー入力待機
read -p "認証トークンを入力してください: " NGROK_TOKEN

if [ ! -z "$NGROK_TOKEN" ]; then
    echo "🔧 ngrok認証設定中..."
    ngrok config add-authtoken "$NGROK_TOKEN"
    
    if [ $? -eq 0 ]; then
        echo "✅ ngrok認証設定完了！"
        echo ""
        echo "🚀 テスト起動中..."
        
        # バックグラウンドでngrok起動
        nohup ngrok http 8080 > /Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/logs/ngrok.log 2>&1 &
        NGROK_PID=$!
        
        echo "ngrok PID: $NGROK_PID"
        echo "$NGROK_PID" > /Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/logs/ngrok.pid
        
        sleep 5
        
        # ngrok URL取得
        NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4 | head -1)
        
        if [ ! -z "$NGROK_URL" ]; then
            echo "🎉 ngrok起動成功！"
            echo "📡 公開URL: $NGROK_URL"
            echo "🔗 Webhook URL: $NGROK_URL/github-webhook"
            echo "🔗 Netlify URL: $NGROK_URL/netlify-webhook"
            echo "❤️ ヘルスチェック: $NGROK_URL/health"
            echo ""
            echo "✅ 外部公開完了！次はWebhook設定です。"
            
            # URL保存
            echo "$NGROK_URL" > /Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/logs/ngrok_url.txt
            
        else
            echo "❌ ngrok URL取得失敗。手動確認が必要です。"
            echo "   確認URL: http://localhost:4040"
        fi
        
    else
        echo "❌ ngrok認証設定失敗"
    fi
else
    echo "❌ 認証トークンが入力されませんでした"
fi

echo ""
echo "📊 ngrok管理コマンド:"
echo "   起動確認: curl http://localhost:4040/api/tunnels"
echo "   停止: pkill ngrok"
echo "   ログ確認: tail -f /Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/logs/ngrok.log"