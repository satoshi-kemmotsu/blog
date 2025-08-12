#!/usr/bin/env python3
"""
Jekyll記事変換エージェント
生成された記事を自動でJekyll形式に変換するシステム

作成日: 2025-08-07
作成者: Claude Code
"""

import os
import re
import # GAFA_PLATINUM: データ形式（RFC 8259準拠）
 json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
import logging

class JekyllArticleConverter:
    def __init__(self):
        # 設定ファイルからパス取得
        import sys
        # 動的パス解決
        import os
        project_root = os.environ.get('PROJECT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sys.path.append(project_root)
        from config.config_loader import config
        
        self.base_dir = Path(config.config['paths']['project_root'])
        self.source_dir = Path(config.config['paths']['blog_articles_dir'])
        self.output_dir = Path(config.config['paths']['github_pages_dir'])
        self.backup_dir = self.base_dir / "data/jekyll_converter_backup"
        
        # カテゴリマッピング（英語 → 日本語）
        self.category_map = {
            'symptom_guide': '症状解説',
            'prevention': 'セルフケア', 
            'qa': 'よくある質問',
            'case_study': 'ケア事例'
        }
        
        # 症状名マッピング（日本語 → 英語スラッグ）
        self.condition_map = {
            '脊髄損傷': 'spinal-injury',
            'パーキンソン病': 'parkinsons',
            '脊柱管狭窄症': 'spinal-stenosis',
            '脳血管障害': 'cerebrovascular',
            '関節拘縮': 'joint-contracture',
            '変形性関節症': 'osteoarthritis',
            '筋萎縮': 'muscle-atrophy',
            '骨粗鬆症': 'osteoporosis',
            'リウマチ': 'rheumatism',
            '五十肩': 'frozen-shoulder',
            '椎間板ヘルニア': 'herniated-disc',
            '坐骨神経痛': 'sciatica',
            '膝関節症': 'knee-joint',
            '腰椎症': 'lumbar',
            '頸椎症': 'cervical',
            '脳梗塞': 'cerebral-infarction'
        }
        
        # 地域名マッピング（日本語 → 英語スラッグ）
        self.area_map = {
            '北区': 'kita',
            '都島区': 'miyakojima', 
            '福島区': 'fukushima',
            '此花区': 'konohana',
            '中央区': 'chuo',
            '西区': 'nishi',
            '港区': 'minato',
            '大正区': 'taisho',
            '天王寺区': 'tennoji',
            '浪速区': 'naniwa',
            '西淀川区': 'nishiyodogawa',
            '東淀川区': 'higashiyodogawa',
            '東成区': 'higashinari',
            '生野区': 'ikuno',
            '旭区': 'asahi',
            '城東区': 'joto',
            '阿倍野区': 'abeno',
            '住吉区': 'sumiyoshi',
            '東住吉区': 'higashisumiyoshi',
            '西成区': 'nishinari',
            '淀川区': 'yodogawa',
            '鶴見区': 'tsurumi',
            '住之江区': 'suminoe',
            '平野区': 'hirano'
        }
        
        # カテゴリスラッグマッピング
        self.category_slug_map = {
            'symptom_guide': 'guide',
            'prevention': 'prevention',
            'qa': 'qa',
            'case_study': 'case'
        }
        
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # ディレクトリ作成
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_article_info(self, content):
        """記事からタイトル、カテゴリ、地域、症状を抽出"""
        info = {
            'title': '',
            'category': 'symptom_guide',  # デフォルト
            'area': '',
            'condition': '',
            'tags': []
        }
        
        # タイトル抽出（最初のh1から）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            info['title'] = title_match.group(1).strip()
            
        # メタ情報抽出
        tag_match = re.search(r'\*\*タグ:\*\*\s*(.+)', content)
        if tag_match:
            tags = [tag.strip() for tag in tag_match.group(1).split(',')]
            info['tags'] = tags
            
            # 症状名と地域名を抽出
            for tag in tags:
                if tag in self.condition_map:
                    info['condition'] = tag
                if tag in self.area_map:
                    info['area'] = tag
                    
        # カテゴリ抽出
        category_match = re.search(r'\*\*カテゴリ:\*\*\s*(.+)', content)
        if category_match:
            info['category'] = category_match.group(1).strip()
            
        return info
        
    def generate_filename(self, info):
        """Jekyll用のファイル名を生成"""
        # UTC時刻で1時間前の日時を取得（確実に過去にする）
        # 設定ファイルからタイムゾーンオフセット取得
        timezone_offset = config.config.get('jekyll_settings', {}).get('timezone_offset_hours', 1)
        utc_time = datetime.now(timezone.utc) - timedelta(hours=timezone_offset)
        date_str = utc_time.strftime('%Y-%m-%d')
        
        # スラッグ生成
        condition_slug = self.condition_map.get(info['condition'], 'condition')
        area_slug = self.area_map.get(info['area'], 'area')
        category_slug = self.category_slug_map.get(info['category'], 'article')
        
        filename = f"{date_str}-{condition_slug}-{category_slug}-{area_slug}.md"
        return filename
        
    def generate_front_matter(self, info):
        """Jekyll Front Matterを生成"""
        # UTC時刻で1時間前の日時を取得
        # 設定ファイルからタイムゾーンオフセット取得
        timezone_offset = config.config.get('jekyll_settings', {}).get('timezone_offset_hours', 1)
        utc_time = datetime.now(timezone.utc) - timedelta(hours=timezone_offset)
        date_str = utc_time.strftime('%Y-%m-%d %H:%M:%S +0000')
        
        # カテゴリは英語のまま使用（Jekyll内部処理用）
        english_category = info['category']
        
        # タグリストを作成（日本語のまま）
        tags = []
        if info['condition']:
            tags.append(info['condition'])
        if info['area']:
            tags.append(info['area'])
        tags.extend(['訪問マッサージ', '医療保険', '大阪市', '在宅医療'])
        
        front_matter = f"""---
layout: post
title: "{info['title']}"
date: {date_str}
categories: [{english_category}]
tags: {tags}
area: "{info['area']}"
condition: "{info['condition']}"
---

"""
        return front_matter
        
    def clean_article_content(self, content):
        """記事コンテンツをクリーンアップ"""
        # メタ情報行を削除
        lines = content.split('\n')
        cleaned_lines = []
        skip_meta = False
        
        for line in lines:
            # メタ情報をスキップ
            if line.startswith('**タグ:**') or line.startswith('**カテゴリ:**') or line.startswith('**作成日:**'):
                skip_meta = True
                continue
            if skip_meta and line.strip() == '---':
                skip_meta = False
                continue
            if skip_meta:
                continue
                
            cleaned_lines.append(line)
            
        return '\n'.join(cleaned_lines)
        
    def backup_existing_file(self, filename):
        """既存ファイルのバックアップを作成"""
        source_path = self.output_dir / filename
        if source_path.exists():
            backup_path = self.backup_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            shutil.copy2(source_path, backup_path)
            self.logger.info(f"既存ファイルをバックアップ: {backup_path}")
            return backup_path
        return None
        
    def convert_article(self, source_path, overwrite=False):
        """単一記事をJekyll形式に変換"""
        try:
            source_path = Path(source_path)
            if not source_path.exists():
                raise FileNotFoundError(f"ソースファイルが見つかりません: {source_path}")
                
            # 記事内容を読み込み
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 記事情報を抽出
            info = self.extract_article_info(content)
            if not info['title']:
                raise ValueError(f"タイトルが抽出できませんでした: {source_path}")
                
            # ファイル名とパスを生成
            filename = self.generate_filename(info)
            output_path = self.output_dir / filename
            
            # 既存ファイルチェック
            if output_path.exists() and not overwrite:
                backup_path = self.backup_existing_file(filename)
                self.logger.warning(f"既存ファイルを上書きします: {output_path}")
                
            # Front Matterを生成
            front_matter = self.generate_front_matter(info)
            
            # 記事コンテンツをクリーンアップ
            cleaned_content = self.clean_article_content(content)
            
            # Jekyll記事を作成
            jekyll_content = front_matter + cleaned_content
            
            # ファイルを保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(jekyll_content)
                
            result = {
                'success': True,
                'source_path': str(source_path),
                'output_path': str(output_path),
                'filename': filename,
                'title': info['title'],
                'category': info['category'],
                'area': info['area'],
                'condition': info['condition']
            }
            
            self.logger.info(f"変換完了: {filename}")
            return result
            
        except Exception as e:
            self.logger.error(f"変換エラー: {source_path} - {str(e)}")
            return {
                'success': False,
                'source_path': str(source_path),
                'error': str(e)
            }
            
    def batch_convert(self, date_filter=None, overwrite=False):
        """複数記事の一括変換"""
        results = []
        
        # 対象日付のディレクトリを取得
        if date_filter:
            target_dirs = [self.source_dir / date_filter]
        else:
            target_dirs = [d for d in self.source_dir.iterdir() if d.is_dir()]
            
        for date_dir in sorted(target_dirs):
            if not date_dir.is_dir():
                continue
                
            self.logger.info(f"処理中のディレクトリ: {date_dir}")
            
            # ディレクトリ内のMarkdownファイルを処理
            for md_file in date_dir.glob('*.md'):
                result = self.convert_article(md_file, overwrite=overwrite)
                results.append(result)
                
        return results
        
    def print_summary(self, results):
        """変換結果のサマリーを表示"""
        success_count = len([r for r in results if r['success']])
        error_count = len([r for r in results if not r['success']])
        
        print("\n" + "="*60)
        print("Jekyll記事変換エージェント - 処理結果")
        print("="*60)
        print(f"総処理数: {len(results)}件")
        print(f"成功: {success_count}件")
        print(f"エラー: {error_count}件")
        
        if success_count > 0:
            print("\n✅ 変換成功:")
            for result in results:
                if result['success']:
                    print(f"  📄 {result['filename']}")
                    print(f"     タイトル: {result['title']}")
                    print(f"     カテゴリ: {result['category']} | 地域: {result['area']} | 症状: {result['condition']}")
                    
        if error_count > 0:
            print("\n❌ 変換エラー:")
            for result in results:
                if not result['success']:
                    print(f"  📄 {Path(result['source_path']).name}")
                    print(f"     エラー: {result['error']}")
                    
        print("\n📁 出力先:", self.output_dir)
        print("📁 バックアップ先:", self.backup_dir)
        print("="*60)

def main():
    """メイン処理"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Jekyll記事変換エージェント')
    parser.add_argument('--file', '-f', help='変換する単一ファイルのパス')
    parser.add_argument('--date', '-d', help='処理する日付 (YYYY-MM-DD)')
    parser.add_argument('--overwrite', '-o', action='store_true', help='既存ファイルを上書き')
    parser.add_argument('--all', '-a', action='store_true', help='すべての記事を一括変換')
    
    args = parser.parse_args()
    
    converter = JekyllArticleConverter()
    
    if args.file:
        # 単一ファイル変換
        result = converter.convert_article(args.file, overwrite=args.overwrite)
        converter.print_summary([result])
        
    elif args.date or args.all:
        # 一括変換
        date_filter = args.date if not args.all else None
        results = converter.batch_convert(date_filter=date_filter, overwrite=args.overwrite)
        converter.print_summary(results)
        
    else:
        # 最新日付の記事を変換（デフォルト動作）
        today = datetime.now().strftime('%Y-%m-%d')
        results = converter.batch_convert(date_filter=today, overwrite=args.overwrite)
        if not results:
            # 今日の記事がない場合は昨日の記事を変換
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            results = converter.batch_convert(date_filter=yesterday, overwrite=args.overwrite)
            
        converter.print_summary(results)

if __name__ == '__main__':
    main()