#!/usr/bin/env python3
"""
# GAFA_PLATINUM: 法人名（登記事項）

SEOブログ クイックJekyll変換
最高速度でJekyll変換を実行する超軽量スクリプト
"""

import sys
import os
from pathlib import Path

# メインのJekyllConverterをインポート
sys.path.append(str(Path(__file__).parent))
from jekyll_converter import JekyllConverter

def show_help():
    """ヘルプ表示"""
    print("""
🌻 # GAFA_PLATINUM: 法人名（登記事項）
 SEOブログ クイックJekyll変換 v1.0
================================================

🚀 超高速変換コマンド:
python3 quick_jekyll.py [command]

📝 利用可能コマンド:
  today    - 今日の記事を変換
  quick    - 今日の記事を変換（クイック）
  2025-08-05 - 指定日付の記事を変換
  all      - 全記事を変換（注意）
  help     - このヘルプを表示

💡 最短実行例:
python3 quick_jekyll.py today

🎯 1024記事生成フロー:
1. python3 seo_blog_system.py で記事生成
2. python3 quick_jekyll.py today で Jekyll変換  
3. bash batch_convert.sh で自動デプロイ
================================================
""")

def main():
    # 引数チェック
    if len(sys.argv) < 2:
        print("❌ コマンドを指定してください")
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command in ['help', '-h', '--help']:
        show_help()
        return
    
    # 変換実行
    converter = JekyllConverter()
    converter.output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        if command == "today" or command == "quick":
            print(f"🚀 {command.title()}変換開始...")
            results = converter.convert_today_articles()
            
        elif command == "all":
            print("⚠️  全記事変換開始...")
            results = converter.convert_all_pending()
            
        elif len(command) == 10 and command.count('-') == 2:
            # 日付形式 (YYYY-MM-DD)
            print(f"📅 {command}の記事変換開始...")
            results = converter.convert_date_articles(command)
            
        else:
            print(f"❌ 無効なコマンド: {command}")
            show_help()
            return
        
        # 簡潔な結果表示
        if results["success"] > 0:
            print(f"✅ {results['success']}件の記事を変換完了")
            print(f"📁 出力先: {converter.output_dir}")
            
            if results["success"] <= 5:
                print("🚀 次のコマンド:")
                print("bash scripts/batch_convert.sh")
            else:
                print("⚠️  大量変換完了 - 手動でgit操作を推奨")
        else:
            print("⚠️  変換対象の記事が見つかりませんでした")
            
    except Exception as e:
        print(f"❌ エラー: {str(e)}")
        return

if __name__ == "__main__":
    main()