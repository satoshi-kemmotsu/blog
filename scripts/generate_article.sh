#!/bin/bash
# 🚀 記事生成ワンライナーコマンド
# 環境変数自動読み込み→記事生成のシンプル化

# 使用方法: ./scripts/generate_article.sh パーキンソン病 西区 case_study

if [[ $# -ne 3 ]]; then
    echo "❌ 使用方法が間違っています"
    echo "正しい使用方法: ./scripts/generate_article.sh [症状] [地域] [テンプレート]"
    echo "例: ./scripts/generate_article.sh パーキンソン病 西区 case_study"
    exit 1
fi

CONDITION="$1"
AREA="$2" 
TEMPLATE="$3"

echo "🚀 記事生成開始"
echo "症状: $CONDITION"
echo "地域: $AREA"
echo "テンプレート: $TEMPLATE"
echo "=================="

# 環境変数自動読み込み
if [[ -f ".env" ]]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ 環境変数読み込み完了"
else
    echo "⚠️  .env ファイルが見つかりません"
    echo "初回セットアップ実行: ./scripts/quick_setup.sh"
    exit 1
fi

# 記事生成実行
echo ""
echo "📝 記事生成実行中..."
python scripts/seo_blog_system.py "$CONDITION" "$AREA" "$TEMPLATE"

echo ""
echo "🎉 記事生成完了！"
echo "次のステップ: Taskエージェントを使用してJekyll変換を実行してください"