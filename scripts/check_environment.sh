#!/bin/bash
# ひまわり治療院SEOブログシステム環境確認スクリプト
# 使用方法: ./scripts/check_environment.sh

echo "🔍 ひまわり治療院SEOブログシステム環境確認"
echo "=============================================="

# 現在位置確認
echo "📍 現在の作業ディレクトリ:"
pwd
echo ""

# 重要ファイル存在確認
echo "📋 重要ファイル存在確認:"
files=(
    "scripts/seo_blog_system.py"
    "scripts/safe_jekyll_converter.py" 
    "data/netlify_site/_posts/"
    "data/netlify_site/_config.yml"
)

all_ok=true
for file in "${files[@]}"; do
    if [[ -e "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file - 見つかりません！"
        all_ok=false
    fi
done

echo ""

# Git状態確認
echo "📊 Git状態確認:"
git status --porcelain | head -5
if [[ $(git status --porcelain | wc -l) -gt 0 ]]; then
    echo "⚠️  未コミットの変更があります"
else
    echo "✅ クリーンな状態"
fi

echo ""

# 環境変数確認
echo "🔧 環境変数確認:"
env_vars=("COMPANY_NAME" "LICENSE" "CLINIC_PHONE" "MAIN_SITE_URL" "BUSINESS_HOURS")
for var in "${env_vars[@]}"; do
    if [[ -n "${!var}" ]]; then
        echo "✅ $var: ${!var}"
    else
        echo "⚠️  $var: 未設定"
    fi
done

echo ""

# 最終判定
if $all_ok; then
    echo "🎉 環境確認完了！記事生成システムを使用できます"
    echo ""
    echo "📝 記事生成コマンド例:"
    echo "COMPANY_NAME=\"ひまわり治療院\" CLINIC_PHONE=\"080-4769-0101\" python scripts/seo_blog_system.py パーキンソン病 西区 case_study"
else
    echo "🚨 環境に問題があります！上記エラーを解決してください"
    echo ""
    echo "🔧 対処方法:"
    echo "1. 正しいディレクトリに移動: cd /Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT"
    echo "2. 不足ファイルを復旧: git checkout [該当ファイル]"
    echo "3. 再度確認: ./scripts/check_environment.sh"
fi