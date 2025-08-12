#!/usr/bin/env python3
"""
スマートJekyll変換システム
Claude Taskエージェント自動連携でミスゼロを実現
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

class SmartJekyllConverter:
    """エージェント連携Jekyll変換システム"""
    
    def __init__(self):
        self.project_root = self._get_project_root()
        self.config = self._load_config()
        
    def _get_project_root(self) -> Path:
        """プロジェクトルート取得"""
        project_root = os.environ.get('PROJECT_ROOT')
        if project_root:
            return Path(project_root)
        return Path(__file__).parent.parent
    
    def _load_config(self) -> Dict[str, Any]:
        """設定ファイル読み込み"""
        config_path = self.project_root / "config" / "blog_config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """デフォルト設定"""
        return {
            "paths": {
                "articles_dir": str(self.project_root / "blog_articles"),
                "jekyll_posts": str(self.project_root / "data" / "github_pages" / "_posts")
            },
            "jekyll": {
                "layout": "post",
                "timezone_offset": "+0000"
            }
        }
    
    def analyze_article(self, article_path: Path) -> Dict[str, Any]:
        """記事を分析してメタデータ抽出"""
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # タイトル抽出
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else article_path.stem
        
        # カテゴリ推定
        category = self._detect_category(content, article_path.name)
        
        # 地域・症状抽出
        area = self._extract_area(content)
        condition = self._extract_condition(content)
        
        return {
            "title": title,
            "category": category,
            "area": area,
            "condition": condition,
            "content": content
        }
    
    def _detect_category(self, content: str, filename: str) -> str:
        """カテゴリ自動検出"""
        if "症状解説" in content or "でお悩みの方へ" in content:
            return "symptom_guide"
        elif "セルフケア" in content or "予防" in content:
            return "prevention"
        elif "よくある質問" in content or "FAQ" in content:
            return "qa"
        elif "ケア事例" in content or "事例" in content:
            return "case_study"
        elif "競合分析" in content or "選び方" in content:
            return "competitive_analysis"
        elif "体験談" in content or "あなたへ" in content:
            return "experience_story"
        else:
            return "symptom_guide"  # デフォルト
    
    def _extract_area(self, content: str) -> Optional[str]:
        """地域名抽出"""
        osaka_areas = [
            "住吉区", "北区", "天王寺区", "浪速区", "中央区", "都島区", "此花区", 
            "旭区", "城東区", "生野区", "鶴見区", "住之江区", "大正区", "東成区",
            "西成区", "港区", "西区", "福島区", "淀川区", "東淀川区", "西淀川区",
            "阿倍野区", "東住吉区", "平野区"
        ]
        
        for area in osaka_areas:
            if area in content:
                return area
        return None
    
    def _extract_condition(self, content: str) -> Optional[str]:
        """症状名抽出"""
        conditions = [
            "パーキンソン病", "脳血管障害", "関節拘縮", "筋萎縮", "骨粗鬆症",
            "椎間板ヘルニア", "脊柱管狭窄症", "坐骨神経痛", "変形性関節症",
            "リウマチ", "五十肩", "頸椎症", "腰痛症", "脊髄損傷", "廃用症候群",
            "その他"
        ]
        
        for condition in conditions:
            if condition in content:
                return condition
        return None
    
    def generate_jekyll_front_matter(self, metadata: Dict[str, Any], date_str: str = None) -> str:
        """Jekyll Front Matter生成"""
        if date_str is None:
            # UTC時刻で確実に過去時刻に設定
            now_utc = datetime.now(timezone.utc)
            # 1時間前に設定して確実に過去時刻にする
            date_utc = now_utc.replace(hour=now_utc.hour-1) if now_utc.hour > 0 else now_utc.replace(hour=23, day=now_utc.day-1)
            date_str = date_utc.strftime("%Y-%m-%d %H:%M:%S +0000")
        
        category_map = {
            "symptom_guide": "症状解説",
            "prevention": "セルフケア", 
            "qa": "よくある質問",
            "case_study": "ケア事例",
            "competitive_analysis": "競合分析",
            "experience_story": "体験談"
        }
        
        front_matter = f"""---
layout: "{self.config['jekyll']['layout']}"
title: "{metadata['title']}"
date: "{date_str}"
categories: [{metadata['category']}]
tags: ['{metadata.get('condition', '')}', '{metadata.get('area', '')}', '訪問マッサージ', '医療保険適用', '大阪市']

"""
        
        if metadata.get('area'):
            front_matter += f"area: \"{metadata['area']}\"\n"
        if metadata.get('condition'):
            front_matter += f"condition: \"{metadata['condition']}\"\n"
        
        front_matter += "---\n\n"
        return front_matter
    
    def generate_jekyll_filename(self, metadata: Dict[str, Any], original_path: Path) -> str:
        """Jekyll形式ファイル名生成"""
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        
        # 英語ファイル名生成
        category_short = {
            "symptom_guide": "guide",
            "prevention": "prevention", 
            "qa": "qa",
            "case_study": "case",
            "competitive_analysis": "analysis",
            "experience_story": "story"
        }.get(metadata['category'], 'article')
        
        condition_short = self._to_english_short(metadata.get('condition', ''))
        area_short = self._to_english_short(metadata.get('area', ''))
        
        filename = f"{date_prefix}-{condition_short}-{category_short}-{area_short}.md"
        return filename
    
    def _to_english_short(self, japanese_text: str) -> str:
        """日本語を英語短縮形に変換"""
        mapping = {
            "パーキンソン病": "parkinsons",
            "脳血管障害": "cerebrovascular",
            "関節拘縮": "contracture",
            "筋萎縮": "atrophy",
            "骨粗鬆症": "osteoporosis",
            "椎間板ヘルニア": "hernia",
            "脊柱管狭窄症": "stenosis",
            "坐骨神経痛": "sciatica",
            "変形性関節症": "osteoarthritis",
            "リウマチ": "rheumatism",
            "五十肩": "frozen-shoulder",
            "頸椎症": "cervical",
            "腰痛症": "back-pain",
            "脊髄損傷": "spinal-injury",
            "廃用症候群": "disuse-syndrome",
            "住吉区": "sumiyoshi",
            "北区": "kita",
            "天王寺区": "tennoji",
            "浪速区": "naniwa",
            "中央区": "chuo",
            "都島区": "miyakojima",
            "此花区": "konohana",
            "旭区": "asahi",
            "城東区": "joto",
            "生野区": "ikuno",
            "鶴見区": "tsurumi",
            "住之江区": "suminoe",
            "大正区": "taisho",
            "東成区": "higashinari",
            "西成区": "nishinari",
            "港区": "minato",
            "西区": "nishi",
            "福島区": "fukushima",
            "淀川区": "yodogawa",
            "東淀川区": "higashiyodogawa",
            "西淀川区": "nishiyodogawa",
            "阿倍野区": "abeno",
            "東住吉区": "higashisumiyoshi",
            "平野区": "hirano"
        }
        return mapping.get(japanese_text, japanese_text.lower().replace(" ", "-"))
    
    def trigger_agent_conversion(self, articles_dir: str, target_date: str = None) -> Dict[str, Any]:
        """Taskエージェントを使用してJekyll変換実行"""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        
        source_dir = Path(articles_dir) / target_date
        if not source_dir.exists():
            return {"status": "error", "message": f"記事ディレクトリが見つかりません: {source_dir}"}
        
        articles = list(source_dir.glob("*.md"))
        if not articles:
            return {"status": "error", "message": f"対象記事が見つかりません: {source_dir}"}
        
        print(f"🚀 Taskエージェントを起動してJekyll変換を実行します")
        print(f"📁 対象: {len(articles)}記事 in {source_dir}")
        print(f"🎯 変換先: {self.config['paths']['jekyll_posts']}")
        
        # エージェントタスクプロンプトを生成
        task_prompt = self._generate_agent_task_prompt(source_dir, articles)
        
        return {
            "status": "ready_for_agent",
            "articles_count": len(articles),
            "source_dir": str(source_dir),
            "target_dir": self.config['paths']['jekyll_posts'],
            "task_prompt": task_prompt,
            "instruction": "以下のプロンプトでTaskエージェントを起動してください"
        }
    
    def _generate_agent_task_prompt(self, source_dir: Path, articles: List[Path]) -> str:
        """エージェントタスク用プロンプト生成（環境変数とソース記事忠実変換対応）"""
        articles_list = "\n".join([f"- {article.name}" for article in articles])
        
        # 環境変数の現在値を取得
        env_vars = {
            'COMPANY_NAME': os.environ.get('COMPANY_NAME', 'ひまわり治療院'),
            'LICENSE': os.environ.get('LICENSE', '厚生労働省認定・医療保険適用の訪問医療マッサージ専門院'),
            'CLINIC_PHONE': os.environ.get('CLINIC_PHONE', '080-4769-0101'),
            'MAIN_SITE_URL': os.environ.get('MAIN_SITE_URL', 'https://peraichi.com/landing_pages/view/himawari-massage'),
            'BUSINESS_HOURS': os.environ.get('BUSINESS_HOURS', '8:00-21:00（毎日）')
        }
        
        return f"""以下のタスクを実行してください：

📁 **対象記事ディレクトリ**: {source_dir}
📝 **変換対象記事** ({len(articles)}件):
{articles_list}

🔧 **必須環境変数**（これらの値を必ず使用すること）:
- COMPANY_NAME: "{env_vars['COMPANY_NAME']}"
- LICENSE: "{env_vars['LICENSE']}"
- CLINIC_PHONE: "{env_vars['CLINIC_PHONE']}"
- MAIN_SITE_URL: "{env_vars['MAIN_SITE_URL']}"
- BUSINESS_HOURS: "{env_vars['BUSINESS_HOURS']}"

🎯 **実行タスク**:
1. 各記事を完全に読み込み（全文を取得）
2. 記事内容を一切改変せず、そのまま保持
3. H1タイトルを削除しない（記事の構造を完全保持）
4. Jekyll Front Matter生成（UTC時刻使用必須）
5. 英語ファイル名への変換
6. {self.config['paths']['jekyll_posts']} に保存

🚨 **厳格な制限事項**:
- ソース記事の内容を一文字も変更・追加・削除してはならない
- 独自の文章やストーリーを追加することを完全に禁止
- FAQ形式の質問を勝手に追加することを禁止
- 「大阪城公園にお参りしたい」等の創作ストーリーを追加することを禁止
- ソース記事にない情報は一切追加しない

⚠️ **重要な注意点**:
- 日付は必ずUTC形式で現在時刻より過去に設定
- カテゴリは [symptom_guide], [prevention], [qa], [case_study] のいずれか
- ファイル名は英語のみ（日本語禁止）
- area/conditionメタデータを必ず追加
- Front Matterの形式を厳密に守る
- 運営者情報は必ず上記の環境変数値を使用

🔍 **品質チェック**:
- 変換後記事にソース記事にない内容が含まれていないか確認
- 環境変数値が正確に反映されているか確認
- H1タイトルが保持されているか確認

🚀 **実行後**:
- 変換完了した記事数を報告
- エラーがあれば詳細を報告
- 成功時は各記事のタイトルとファイル名を一覧表示
- ソース記事との内容一致確認結果を報告"""

def main():
    """メイン実行関数"""
    converter = SmartJekyllConverter()
    
    if len(sys.argv) < 2:
        print("使用方法: python smart_jekyll_converter.py <記事ディレクトリ> [日付]")
        print("例: python smart_jekyll_converter.py /path/to/blog_articles 2025-08-08")
        return
    
    articles_dir = sys.argv[1]
    target_date = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = converter.trigger_agent_conversion(articles_dir, target_date)
    
    if result["status"] == "error":
        print(f"❌ エラー: {result['message']}")
        return
    
    print("\n" + "="*60)
    print("🎯 TASK エージェント起動準備完了")
    print("="*60)
    print(f"📊 変換対象: {result['articles_count']}記事")
    print(f"📁 ソース: {result['source_dir']}")
    print(f"🎯 出力先: {result['target_dir']}")
    print("\n📋 以下のプロンプトでTaskエージェントを起動してください:")
    print("-"*60)
    print(result['task_prompt'])
    print("-"*60)

if __name__ == "__main__":
    main()