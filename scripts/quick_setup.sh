#!/bin/bash
# 🚀 クイックセットアップスクリプト
# 新しいClaude セッション開始時の1回実行で完了

echo "🚀 ひまわり治療院SEOブログシステム クイックセットアップ"
echo "=================================================="

# Step 1: .env ファイル存在確認・作成
if [[ ! -f ".env" ]]; then
    echo "📝 .env ファイルを作成中..."
    cp .env.example .env
    echo "⚠️  .env ファイルに実際の値を設定してください"
    echo "   主要項目: GITHUB_TOKEN, NETLIFY_AUTH_TOKEN"
else
    echo "✅ .env ファイル存在確認"
fi

# Step 2: 環境変数読み込み
if [[ -f ".env" ]]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ 環境変数読み込み完了"
fi

# Step 3: 環境確認実行
echo ""
echo "🔍 システム環境確認実行..."
./scripts/check_environment.sh

# Step 4: 緊急バックアップ実行
echo ""
echo "🛡️  緊急バックアップ実行..."
./scripts/emergency_backup_system.sh > /dev/null

echo ""
echo "🎉 セットアップ完了！"
echo ""
echo "📝 記事生成コマンド例:"
echo "python scripts/seo_blog_system.py パーキンソン病 西区 case_study"
echo ""
echo "⚠️  重要: Git危険操作前には安全装置が動作します"
echo "正常な作業では影響ありません"