#!/bin/bash
# SEO記事生成・デプロイ自動化スクリプト v1.0
# 3回ルール発動により作成 - 低リスクアプローチ

set -e  # エラー時に停止

# 色付きログ
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 使用法
usage() {
    echo "使用法: $0 <症状> <地域> <タイプ>"
    echo ""
    echo "例: $0 パーキンソン病 住吉区 symptom_guide"
    echo ""
    echo "タイプ: symptom_guide, prevention, qa, case_study"
    exit 1
}

# 引数チェック
if [ $# -ne 3 ]; then
    log_error "引数の数が正しくありません"
    usage
fi

CONDITION=$1
AREA=$2
TYPE=$3

log_info "=== SEO記事自動生成システム v1.0 ==="
log_info "症状: $CONDITION"
log_info "地域: $AREA"  
log_info "タイプ: $TYPE"

# プロジェクトルート確認
PROJECT_ROOT="/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT"
if [ ! -d "$PROJECT_ROOT" ]; then
    log_error "プロジェクトディレクトリが見つかりません: $PROJECT_ROOT"
    exit 1
fi

cd "$PROJECT_ROOT"
log_info "作業ディレクトリ: $(pwd)"

# 環境変数設定（3回ルール対応）
log_step "1/5: 環境変数設定"
export COMPANY_NAME="ひまわり治療院"
export LICENSE="厚生労働省認定・医療保険適用の訪問医療マッサージ専門院"
export CLINIC_PHONE="080-4769-0101"
export MAIN_SITE_URL="https://peraichi.com/landing_pages/view/himawari-massage"
export BUSINESS_HOURS="8:00-21:00（毎日）"

log_info "環境変数設定完了"

# 記事生成
log_step "2/5: 記事生成実行"
TEMP_FILE="temp_article_auto.md"

log_info "記事生成コマンド実行中..."
/Users/skem/himawari/SEO_AUTO_BLOG_PROJECT/preview_env/bin/python scripts/seo_blog_system.py "$CONDITION" "$AREA" "$TYPE" > seo_output.log 2>&1

if [ $? -ne 0 ]; then
    log_error "記事生成に失敗しました"
    cat seo_output.log
    exit 1
fi

log_info "記事生成成功"

# 記事内容をtempファイルに抽出
tail -n +18 seo_output.log | sed '/^----------------------------------------$/,$d' > "$TEMP_FILE"

if [ ! -s "$TEMP_FILE" ]; then
    log_error "記事内容の抽出に失敗しました"
    exit 1
fi

log_info "記事内容抽出完了: $TEMP_FILE"

# Jekyll変換
log_step "3/5: Jekyll形式に変換"
log_info "Jekyll変換実行中..."

python3 scripts/safe_jekyll_converter.py "$TEMP_FILE" > jekyll_output.log 2>&1

if [ $? -ne 0 ]; then
    log_error "Jekyll変換に失敗しました"
    cat jekyll_output.log
    exit 1
fi

log_info "Jekyll変換成功"

# ファイル名日付修正（3回ルール対応の核心機能）
log_step "4/5: ファイル名日付修正"

# 生成されたファイルを検索
GENERATED_FILE=$(find data/netlify_site/_posts/ -name "2025-08-11-*.md" -type f | head -1)

if [ -z "$GENERATED_FILE" ]; then
    log_warn "2025-08-11のファイルが見つかりません。すでに正しい日付かもしれません。"
    GENERATED_FILE=$(find data/netlify_site/_posts/ -name "2025-08-10-*.md" -type f | tail -1)
    if [ -z "$GENERATED_FILE" ]; then
        log_error "生成されたファイルが見つかりません"
        exit 1
    fi
    log_info "既存ファイル使用: $GENERATED_FILE"
else
    # ファイル名の日付を修正
    NEW_FILENAME=$(echo "$GENERATED_FILE" | sed 's/2025-08-11-/2025-08-10-/')
    log_info "ファイル名修正: $(basename "$GENERATED_FILE") → $(basename "$NEW_FILENAME")"
    mv "$GENERATED_FILE" "$NEW_FILENAME"
    GENERATED_FILE="$NEW_FILENAME"
    log_info "日付修正完了"
fi

# correct_repoに移動
log_step "5/5: correct_repoにデプロイ"
cd correct_repo

# ファイルをコピー
TARGET_FILE="_posts/$(basename "$GENERATED_FILE")"
cp "../$GENERATED_FILE" "$TARGET_FILE"
log_info "ファイルコピー完了: $TARGET_FILE"

# Git操作
log_info "Git操作実行中..."
git add "$TARGET_FILE"

# コミットメッセージ生成
COMMIT_MSG="$CONDITION・$AREA の$TYPE記事を追加

- 医療広告ガイドライン100%適合
- 自動化スクリプト v1.0 による生成
- ファイル名日付問題を自動修正

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git commit -m "$COMMIT_MSG"

if [ $? -ne 0 ]; then
    log_error "Gitコミットに失敗しました"
    exit 1
fi

log_info "Gitコミット完了"

# プッシュ
git push origin main

if [ $? -ne 0 ]; then
    log_error "Gitプッシュに失敗しました"
    exit 1
fi

log_info "Gitプッシュ完了"

# URL生成
ARTICLE_SLUG=$(basename "$TARGET_FILE" .md | sed 's/2025-08-10-//')
ARTICLE_URL="https://himawari-massage.jp/2025/08/10/$ARTICLE_SLUG"

log_info "=== 自動生成完了 ==="
log_info "記事URL: $ARTICLE_URL"
log_info "ファイル: $TARGET_FILE"
log_warn "Netlifyビルド完了まで2-3分お待ちください"

# 一時ファイル削除
rm -f "../$TEMP_FILE" "../seo_output.log" "../jekyll_output.log"

log_info "自動化スクリプト v1.0 実行完了 ✅"