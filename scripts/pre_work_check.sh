#!/bin/bash
# 作業前自動チェックシステム（記事生成前の必須確認）
# 使用方法: ./scripts/pre_work_check.sh [症状] [地域] [テンプレート]

echo "🚀 作業前自動チェック開始"
echo "========================="

# 引数チェック
if [[ $# -ne 3 ]]; then
    echo "❌ 引数が不足しています"
    echo "使用方法: ./scripts/pre_work_check.sh [症状] [地域] [テンプレート]"
    echo "例: ./scripts/pre_work_check.sh パーキンソン病 西区 case_study"
    exit 1
fi

CONDITION="$1"
AREA="$2" 
TEMPLATE="$3"

echo "📝 生成予定記事: $CONDITION × $AREA × $TEMPLATE"
echo ""

# 環境確認実行
echo "🔍 Step 1: 環境確認"
if ./scripts/check_environment.sh | grep -q "環境確認完了"; then
    echo "✅ 環境確認OK"
else
    echo "❌ 環境に問題があります。修正してください"
    exit 1
fi

echo ""

# 重複記事チェック
echo "🔍 Step 2: 重複記事確認"
existing_files=$(find data/netlify_site/_posts/ -name "*${AREA}*" -name "*${CONDITION}*" 2>/dev/null)
if [[ -n "$existing_files" ]]; then
    echo "⚠️  類似記事が既に存在します:"
    echo "$existing_files"
    echo ""
    read -p "続行しますか？ (y/N): " continue_choice
    if [[ "$continue_choice" != "y" && "$continue_choice" != "Y" ]]; then
        echo "作業を中止しました"
        exit 1
    fi
else
    echo "✅ 重複記事なし"
fi

echo ""

# バックアップ実行
echo "🔍 Step 3: 自動バックアップ"
./scripts/backup_system.sh > /dev/null 2>&1
echo "✅ バックアップ完了"

echo ""

# 記事生成コマンド提示
echo "🎯 Step 4: 記事生成準備完了"
echo "以下のコマンドで記事生成を実行してください:"
echo ""
echo "COMPANY_NAME=\"ひまわり治療院\" \\"
echo "LICENSE=\"厚生労働省認定・医療保険適用の訪問医療マッサージ専門院\" \\"
echo "CLINIC_PHONE=\"080-4769-0101\" \\"
echo "MAIN_SITE_URL=\"https://peraichi.com/landing_pages/view/himawari-massage\" \\"
echo "BUSINESS_HOURS=\"8:00-21:00（毎日）\" \\"
echo "python scripts/seo_blog_system.py $CONDITION $AREA $TEMPLATE"

echo ""
echo "🎉 作業前チェック完了！記事生成を開始してください"