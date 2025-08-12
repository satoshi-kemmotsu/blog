# 🚨 デプロイ環境の正確な情報（重要：誤認防止用）

## ⚠️ 重要な訂正事項

### ❌ 誤った認識（過去のClaudeが誤認していた内容）
- **誤**: 本番サイトはGitHub Pagesでホストされている
- **誤**: `https://himawari-massage.jp/` はGitHub Pagesで動いている
- **誤**: GitHubにプッシュすれば自動的に本番に反映される

### ✅ 正しい情報

#### 本番環境
- **ホスティング**: **Netlify**（GitHub Pagesではない！）
- **本番URL**: `https://himawari-massage.jp/`
- **Netlify URL**: `https://neon-biscochitos-8dd468.netlify.app/`
- **管理画面**: `https://app.netlify.com/sites/neon-biscochitos-8dd468`

#### デプロイフロー
1. GitHubの`main`ブランチにプッシュ
2. Netlifyが自動的にビルド開始
3. Jekyllビルドが実行される
4. 成功すれば`https://himawari-massage.jp/`に反映

#### GitHub Pagesについて
- **状態**: 無効化されている（使用していない）
- **理由**: Netlifyの方が高機能で環境変数対応
- `https://satoshi-kemmotsu.github.io/blog/` → `https://himawari-massage.jp/` にリダイレクト設定

## 📍 確認方法

### Netlifyビルド状況の確認
```bash
# Netlifyのビルドログを確認（Web UIから）
# https://app.netlify.com/sites/neon-biscochitos-8dd468/deploys
```

### 記事の反映確認
1. GitHubにプッシュ後、5-10分待つ
2. `https://himawari-massage.jp/` で確認
3. 反映されない場合はNetlifyの管理画面でビルドログを確認

## 🔧 トラブルシューティング

### 記事が反映されない場合
1. Netlifyのビルドが成功しているか確認
2. `_config.yml`の設定を確認
3. 記事のFront Matterが正しいか確認
4. Jekyllのビルドエラーがないか確認

### よくある間違い
- GitHub Pagesの設定を触らない
- `gh-pages`ブランチは使用しない
- GitHub Actionsは記事生成には使わない

## 📝 今後のClaude向けメモ

**必ず覚えること**:
1. **本番 = Netlify**（GitHub Pagesではない）
2. **URL = https://himawari-massage.jp/**（Netlifyカスタムドメイン）
3. **デプロイ = GitHubプッシュ → Netlify自動ビルド**

---

**作成日**: 2025-08-12
**目的**: Claude間での誤認防止
**重要度**: 🚨 最高（デプロイ環境の基本情報）