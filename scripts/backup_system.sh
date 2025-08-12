#!/bin/bash
# 重要ファイル自動バックアップスクリプト
# 使用方法: ./scripts/backup_system.sh

DATE=$(date +%Y%m%d_%H%M)
BACKUP_DIR="scripts/backup"

echo "🔄 重要ファイルバックアップ開始"
echo "==============================="

# バックアップディレクトリ作成
mkdir -p "$BACKUP_DIR"

# 重要スクリプトファイル
files=(
    "scripts/seo_blog_system.py"
    "scripts/safe_jekyll_converter.py"
    "scripts/unified_deploy_system.py"
)

echo "📋 バックアップ対象ファイル:"
for file in "${files[@]}"; do
    if [[ -f "$file" ]]; then
        basename_file=$(basename "$file" .py)
        backup_name="${BACKUP_DIR}/${basename_file}_${DATE}.py"
        cp "$file" "$backup_name"
        echo "✅ $file → $backup_name"
    else
        echo "⚠️  $file - 見つかりません"
    fi
done

# 設定ファイル（存在する場合）
if [[ -f "data/netlify_site/_config.yml" ]]; then
    cp "data/netlify_site/_config.yml" "${BACKUP_DIR}/config_${DATE}.yml"
    echo "✅ _config.yml → config_${DATE}.yml"
fi

echo ""
echo "🎉 バックアップ完了"
echo "📁 バックアップ場所: $BACKUP_DIR"
echo ""

# バックアップファイル一覧表示
echo "📋 作成されたバックアップ:"
ls -la "$BACKUP_DIR" | tail -5