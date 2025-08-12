#!/bin/bash
# 🚨 緊急バックアップシステム（CLAUDE.md消失事件対応）
# 重要ファイルの多重バックアップ実行

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_ROOT="backups"
LOCAL_BACKUP="$BACKUP_ROOT/local/$DATE"
CLOUD_BACKUP="$BACKUP_ROOT/cloud"

echo "🚨 緊急バックアップシステム開始"
echo "事件発生日: 2025-08-11"
echo "対象: プロジェクト根幹ファイル"
echo "=================================="

# バックアップディレクトリ作成
mkdir -p "$LOCAL_BACKUP"
mkdir -p "$CLOUD_BACKUP"

# 📋 絶対に失ってはいけないファイル
CRITICAL_FILES=(
    "CLAUDE.md"
    "scripts/seo_blog_system.py"
    "scripts/safe_jekyll_converter.py"
    "ERROR_PATTERNS_DATABASE.json"
    "WEBHOOK_SYSTEM_ARCHITECTURE.md"
    ".gitignore"
)

echo "🔄 重要ファイルバックアップ実行:"
for file in "${CRITICAL_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        # ローカルバックアップ
        cp "$file" "$LOCAL_BACKUP/"
        
        # クラウドバックアップ（タイムスタンプ付き）
        basename_file=$(basename "$file")
        cp "$file" "$CLOUD_BACKUP/${basename_file}_${DATE}"
        
        echo "✅ $file → バックアップ完了"
    else
        echo "⚠️  $file - ファイルが見つかりません！"
    fi
done

# Git コミット情報も保存
echo "📊 Git状態スナップショット保存:"
git log --oneline -20 > "$LOCAL_BACKUP/git_history.txt"
git status > "$LOCAL_BACKUP/git_status.txt"
git diff --name-only > "$LOCAL_BACKUP/git_changes.txt"

echo ""
echo "🎯 バックアップ完了!"
echo "📁 ローカル: $LOCAL_BACKUP"
echo "☁️  クラウド: $CLOUD_BACKUP"
echo ""
echo "📋 作成されたファイル:"
ls -la "$LOCAL_BACKUP"

# 古いバックアップ削除（30日以上前）
find "$BACKUP_ROOT/local" -type d -mtime +30 -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "🔥 Remember CLAUDE.md消失事件 2025-08-11 🔥"
echo "このシステムは二度とあの悲劇を繰り返さないためにある"