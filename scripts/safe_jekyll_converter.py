#!/usr/bin/env python3
"""
安全なJekyll変換システム
環境変数完全対応・ソース記事忠実変換・ハードコーディングフリー
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional

class SafeJekyllConverter:
    """安全なJekyll変換システム - 環境変数完全対応"""
    
    def __init__(self):
        self.project_root = self._get_project_root()
        self.env_vars = self._load_environment_variables()
        
    def _get_project_root(self) -> Path:
        """プロジェクトルート取得"""
        project_root = os.environ.get('PROJECT_ROOT')
        if project_root:
            return Path(project_root)
        return Path(__file__).parent.parent
    
    def _load_environment_variables(self) -> Dict[str, str]:
        """環境変数読み込み（デフォルト値付き）"""
        return {
            'COMPANY_NAME': os.environ.get('COMPANY_NAME', 'ひまわり治療院'),
            'LICENSE': os.environ.get('LICENSE', '厚生労働省認定・医療保険適用の訪問医療マッサージ専門院'),
            'CLINIC_PHONE': os.environ.get('CLINIC_PHONE', '080-4769-0101'),
            'MAIN_SITE_URL': os.environ.get('MAIN_SITE_URL', 'https://peraichi.com/landing_pages/view/himawari-massage'),
            'BUSINESS_HOURS': os.environ.get('BUSINESS_HOURS', '8:00-21:00（毎日）'),
            'TARGET_CITY': os.environ.get('TARGET_CITY', '大阪市'),
        }
    
    def convert_article_with_task_agent(self, article_path: Path) -> Dict[str, Any]:
        """Taskエージェントを使用した安全な記事変換"""
        
        if not article_path.exists():
            return {"success": False, "error": f"記事が見つかりません: {article_path}"}
        
        # 記事内容を読み込み
        with open(article_path, 'r', encoding='utf-8') as f:
            source_content = f.read()
        
        # 記事分析
        metadata = self._analyze_article(source_content)
        
        # Jekyll出力ディレクトリ設定
        jekyll_posts_dir = self.project_root / "data" / "github_pages" / "_posts"
        jekyll_posts_dir.mkdir(parents=True, exist_ok=True)
        
        # ファイル名生成
        jekyll_filename = self._generate_jekyll_filename(metadata)
        jekyll_path = jekyll_posts_dir / jekyll_filename
        
        print(f"🚀 Taskエージェントを使用してJekyll変換を開始")
        print(f"📁 ソース記事: {article_path.name}")
        print(f"🎯 出力ファイル: {jekyll_filename}")
        print(f"📝 記事タイトル: {metadata['title']}")
        print(f"🏷️  カテゴリ: {metadata['category']}")
        print(f"📍 地域: {metadata.get('area', 'N/A')}")
        print(f"🩺 症状: {metadata.get('condition', 'N/A')}")
        
        # 環境変数値を表示
        print(f"\n🔧 環境変数設定:")
        for key, value in self.env_vars.items():
            print(f"  {key}: {value}")
        
        # Taskエージェント用のプロンプトを生成
        agent_prompt = self._generate_task_agent_prompt(
            article_path, source_content, metadata, jekyll_path
        )
        
        return {
            "success": True,
            "source_path": str(article_path),
            "jekyll_path": str(jekyll_path),
            "jekyll_filename": jekyll_filename,
            "metadata": metadata,
            "task_agent_prompt": agent_prompt,
            "instruction": "以下のプロンプトでTaskエージェントを実行してください"
        }
    
    def _analyze_article(self, content: str) -> Dict[str, Any]:
        """記事内容分析"""
        metadata = {}
        
        # タイトル抽出
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        metadata['title'] = title_match.group(1).strip() if title_match else "タイトル未検出"
        
        # カテゴリ検出
        metadata['category'] = self._detect_category(content)
        
        # 地域・症状抽出
        metadata['area'] = self._extract_area(content)
        metadata['condition'] = self._extract_condition(content)
        
        return metadata
    
    def _detect_category(self, content: str) -> str:
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
            return "symptom_guide"
    
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
    
    def _generate_jekyll_filename(self, metadata: Dict[str, Any]) -> str:
        """Jekyll形式ファイル名生成"""
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        
        # 英語短縮形マッピング
        condition_map = {
            "パーキンソン病": "parkinsons", "脳血管障害": "cerebrovascular",
            "関節拘縮": "contracture", "筋萎縮": "atrophy", "骨粗鬆症": "osteoporosis",
            "椎間板ヘルニア": "hernia", "脊柱管狭窄症": "stenosis", "坐骨神経痛": "sciatica",
            "変形性関節症": "osteoarthritis", "リウマチ": "rheumatism", "五十肩": "frozen-shoulder"
        }
        
        area_map = {
            "住吉区": "sumiyoshi", "北区": "kita", "天王寺区": "tennoji", "浪速区": "naniwa",
            "中央区": "chuo", "都島区": "miyakojima", "此花区": "konohana", "旭区": "asahi",
            "城東区": "joto", "生野区": "ikuno", "鶴見区": "tsurumi", "住之江区": "suminoe",
            "大正区": "taisho", "東成区": "higashinari", "西成区": "nishinari", "港区": "minato",
            "西区": "nishi", "福島区": "fukushima", "淀川区": "yodogawa", "東淀川区": "higashiyodogawa",
            "西淀川区": "nishiyodogawa", "阿倍野区": "abeno", "東住吉区": "higashisumiyoshi", "平野区": "hirano"
        }
        
        category_map = {
            "symptom_guide": "guide", "prevention": "prevention", "qa": "qa",
            "case_study": "case", "competitive_analysis": "analysis", "experience_story": "story"
        }
        
        condition_slug = condition_map.get(metadata.get('condition', ''), 'condition')
        area_slug = area_map.get(metadata.get('area', ''), None)
        category_slug = category_map.get(metadata['category'], 'article')
        
        # 地域名が取得できない場合はエラーログを出力
        if not area_slug:
            print(f"⚠️  警告: 地域名を特定できませんでした: {metadata.get('area', 'なし')}")
            area_slug = 'osaka'  # デフォルト値を設定
        
        return f"{date_prefix}-{condition_slug}-{category_slug}-{area_slug}.md"
    
    def _generate_task_agent_prompt(self, source_path: Path, source_content: str, 
                                  metadata: Dict[str, Any], jekyll_path: Path) -> str:
        """Taskエージェント用プロンプト生成"""
        
        # UTC時刻設定（確実に過去時刻）
        utc_now = datetime.now(timezone.utc)
        safe_utc = utc_now - timedelta(hours=1)  # 1時間前に設定
        date_str = safe_utc.strftime("%Y-%m-%d %H:%M:%S +0000")
        
        return f"""以下のJekyll記事変換を実行してください：

📁 **変換元記事**: {source_path}
🎯 **出力先**: {jekyll_path}

🔧 **必須環境変数**（これらの値を必ず使用）:
- COMPANY_NAME: "{self.env_vars['COMPANY_NAME']}"
- LICENSE: "{self.env_vars['LICENSE']}"
- CLINIC_PHONE: "{self.env_vars['CLINIC_PHONE']}"
- MAIN_SITE_URL: "{self.env_vars['MAIN_SITE_URL']}"
- BUSINESS_HOURS: "{self.env_vars['BUSINESS_HOURS']}"

📝 **記事メタ情報**:
- タイトル: {metadata['title']}
- カテゴリ: {metadata['category']}
- 地域: {metadata.get('area', 'N/A')}
- 症状: {metadata.get('condition', 'N/A')}
- 出力日時: {date_str}

🚨 **厳格な変換ルール**:
1. ソース記事を読み込み、内容を一切変更・追加・削除しない
2. H1タイトル（# で始まる行）を削除しない
3. 独自の文章・ストーリー・FAQを追加しない
4. ソース記事にない内容は一切作成しない
5. 運営者情報は上記の環境変数値のみを使用

📋 **Jekyll Front Matter**（この形式で作成）:
```yaml
---
layout: "post"
title: "{metadata['title']}"
date: "{date_str}"
categories: [{metadata['category']}]
tags: ['{metadata.get('condition', '')}', '{metadata.get('area', '')}', '訪問マッサージ', '医療保険適用', '大阪市']

condition: "{metadata.get('condition', '')}"
area: "{metadata.get('area', '')}"
description: "記事の適切な要約を作成"
---
```

🔍 **品質チェック要求**:
- 変換後にソース記事との内容一致を確認
- 環境変数値の正確な反映を確認
- H1タイトルの保持を確認
- 不正な内容追加がないか確認

📊 **実行手順**:
1. {source_path} を読み込み、全文を取得
2. 上記のFront Matterを追加
3. ソース記事内容をそのまま続ける（改変厳禁）
4. {jekyll_path} に保存
5. 変換結果を報告

✅ **成功条件**:
- Jekyll形式のファイルが正常に作成される
- ソース記事の内容が完全に保持される
- 環境変数値が正確に反映される
- 不正な内容追加がない

変換を開始してください。"""

def main():
    """メイン実行関数"""
    if len(sys.argv) < 2:
        print("使用方法: python safe_jekyll_converter.py <記事ファイルパス>")
        return
    
    article_path = Path(sys.argv[1])
    converter = SafeJekyllConverter()
    
    result = converter.convert_article_with_task_agent(article_path)
    
    if result["success"]:
        print("\n" + "="*60)
        print("🎯 Taskエージェント実行準備完了")
        print("="*60)
        print(f"📁 変換元: {result['source_path']}")
        print(f"🎯 出力先: {result['jekyll_path']}")
        print(f"📝 ファイル名: {result['jekyll_filename']}")
        print("\n📋 以下のプロンプトでTaskエージェントを実行:")
        print("-"*60)
        print(result['task_agent_prompt'])
        print("-"*60)
    else:
        print(f"❌ エラー: {result['error']}")

if __name__ == "__main__":
    main()