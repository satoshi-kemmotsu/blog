#!/bin/bash
# 🚨 Git安全装置システム（CLAUDE.md消失事件対応）
# 危険なGit操作を防止する安全装置

echo "🛡️  Git安全装置チェック"
echo "========================"

# 危険なGitコマンドを監視（記事アップ作業では発生しない）
DANGEROUS_COMMANDS=(
    "git reset --hard"
    "git clean -fd" 
    "git checkout ."
    "rm -rf .git"
)

# 通常の記事アップ作業で使用する安全なコマンド（監視対象外）
SAFE_COMMANDS=(
    "git add"
    "git commit"
    "git push"
    "git status"
    "git log"
    "git diff"
)

# 現在実行されようとしているコマンドをチェック
CURRENT_CMD="$*"

echo "🔍 実行予定コマンド: $CURRENT_CMD"

for dangerous_cmd in "${DANGEROUS_COMMANDS[@]}"; do
    if [[ "$CURRENT_CMD" =~ $dangerous_cmd ]]; then
        echo ""
        echo "🚨🚨🚨 危険なコマンドが検出されました！ 🚨🚨🚨"
        echo "コマンド: $dangerous_cmd"
        echo ""
        echo "🔥 2025-08-11 CLAUDE.md消失事件を思い出してください！"
        echo "このコマンドにより550行のCLAUDE.mdと67個のファイル(8350行)が消失しました"
        echo ""
        echo "⚠️  このコマンドを実行すると以下のリスクがあります:"
        echo "- 未コミットの変更が全て失われる可能性"
        echo "- 重要なファイルが完全に削除される可能性" 
        echo "- プロジェクトの根幹が破壊される可能性"
        echo ""
        echo "📋 安全な代替手段:"
        echo "1. git stash push -m \"一時保存\" (安全な退避)"
        echo "2. ./scripts/emergency_backup_system.sh (緊急バックアップ)"
        echo "3. git status (現在の状態確認)"
        echo ""
        read -p "本当に実行しますか？(yes/NO): " confirmation
        
        if [[ "$confirmation" != "yes" ]]; then
            echo "❌ コマンド実行を中止しました"
            echo "🛡️  安全装置によりシステムが保護されました"
            exit 1
        else
            echo "⚠️  ユーザーが実行を強制しました"
            echo "🔄 緊急バックアップを自動実行します..."
            ./scripts/emergency_backup_system.sh
        fi
        break
    fi
done

echo "✅ Git操作の安全性が確認されました"