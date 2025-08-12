#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path

# 環境変数からクリニック情報を取得
COMPANY_NAME = os.environ.get('COMPANY_NAME', 'ひまわり治療院')
LICENSE = os.environ.get('LICENSE', '厚生労働省認定・医療保険適用の訪問医療マッサージ専門院')
CLINIC_PHONE = os.environ.get('CLINIC_PHONE', '080-4769-0101')
MAIN_SITE_URL = os.environ.get('MAIN_SITE_URL', 'https://peraichi.com/landing_pages/view/himawari-massage')
BUSINESS_HOURS = os.environ.get('BUSINESS_HOURS', '8:00-21:00（毎日）')

# 大阪の地域リスト
OSAKA_AREAS = [
    '住吉区', '北区', '天王寺区', '浪速区', '中央区', '都島区', 
    '此花区', '旭区', '城東区', '生野区', '鶴見区', '住之江区',
    '大正区', '東成区', '西成区', '港区', '西区', '福島区',
    '淀川区', '東淀川区', '西淀川区', '阿倍野区', '東住吉区', '平野区'
]

# 症状リスト
CONDITIONS = [
    'パーキンソン病', '脳血管障害', '関節拘縮', '筋萎縮', '骨粗鬆症',
    '椎間板ヘルニア', '脊柱管狭窄症', '坐骨神経痛', '変形性関節症',
    '関節リウマチ', '五十肩', '脳梗塞', '脊髄損傷', '頸椎症', '腰椎症'
]

# カテゴリーリスト
CATEGORIES = ['symptom_guide', 'qa', 'case_study', 'prevention']

def generate_article_content(condition, area, category):
    """記事コンテンツを生成"""
    
    today = datetime.now().strftime('%Y年%m月%d日')
    
    if category == 'symptom_guide':
        title = f"{condition}でお悩みの方へ｜{area}の訪問マッサージで症状緩和"
        content = f"""# {title}

## {area}にお住まいの{condition}でお困りの方へ

{area}で{condition}の症状にお悩みの方へ、{COMPANY_NAME}の訪問医療マッサージがお役に立てるかもしれません。

### {condition}の症状について

{condition}は、日常生活に大きな影響を与える症状です。{area}の多くの方が、この症状でお困りです。

- 日常生活での動作が困難になる
- 痛みや不快感が継続する
- 身体機能の低下が見られる

### 訪問マッサージによるサポート

{COMPANY_NAME}では、{area}全域で以下のサービスを提供しています：

1. **個別対応のマッサージ施術**
   - お一人おひとりの症状に合わせた施術
   - 身体機能の維持・改善をサポート

2. **ご自宅での施術**
   - 通院の負担なし
   - リラックスできる環境での施術

3. **保険適用可能**
   - 医療保険適用で経済的負担を軽減
   - 医師の同意書があれば保険適用可能

### {area}での訪問エリア

{area}全域に訪問可能です。ご自宅や施設まで、経験豊富な施術師がお伺いします。

### お問い合わせ

**電話番号**: {CLINIC_PHONE}  
**営業時間**: {BUSINESS_HOURS}

{area}で{condition}の症状にお悩みの方は、お気軽にご相談ください。

---

*最終更新日: {today}*
"""
    
    elif category == 'qa':
        title = f"{condition}のよくある質問｜{area}の訪問マッサージ"
        content = f"""# {title}

## {area}の方から寄せられる{condition}に関するご質問

### Q1. {condition}でも訪問マッサージを受けられますか？

はい、{condition}の方も訪問マッサージを受けていただけます。{area}にお住まいの多くの方にご利用いただいています。

### Q2. 保険は適用されますか？

医師の同意書があれば、医療保険の適用が可能です。{area}の医療機関と連携してサポートいたします。

### Q3. どのような施術を行いますか？

{condition}の症状に応じて、以下の施術を組み合わせます：
- マッサージによる血行促進
- 関節可動域の維持・改善
- 筋力維持のサポート

### Q4. {area}のどこまで訪問可能ですか？

{area}全域に訪問可能です。ご自宅はもちろん、施設への訪問も対応しています。

### Q5. 料金はどのくらいかかりますか？

保険適用の場合、1回あたりの自己負担は数百円程度です。詳細はお問い合わせください。

### お問い合わせ

**{COMPANY_NAME}**  
電話: {CLINIC_PHONE}  
営業時間: {BUSINESS_HOURS}

---

*最終更新日: {today}*
"""
    
    elif category == 'case_study':
        title = f"{condition}の改善事例｜{area}の訪問マッサージ"
        content = f"""# {title}

## {area}での{condition}改善サポート事例

### 事例のご紹介

{area}にお住まいの方で、{condition}の症状でお困りの方への訪問マッサージサポート事例をご紹介します。

### ケース1: 70代の方の例

**状況**: {condition}により日常生活に支障
**サポート内容**: 週2回の訪問マッサージ
**経過**: 3ヶ月で身体機能の維持・改善を実感

### ケース2: 80代の方の例

**状況**: {condition}による身体の不調
**サポート内容**: 週3回の訪問マッサージ
**経過**: 継続的なケアで生活の質が向上

### {area}での訪問マッサージの特徴

- ご自宅での施術で通院負担なし
- 個別対応で最適なケア
- 保険適用で経済的負担を軽減

### ご相談・お問い合わせ

{area}で{condition}にお悩みの方は、ぜひご相談ください。

**電話**: {CLINIC_PHONE}  
**営業時間**: {BUSINESS_HOURS}

---

*最終更新日: {today}*
"""
    
    else:  # prevention
        title = f"{condition}の予防とケア｜{area}の訪問マッサージ"
        content = f"""# {title}

## {area}で{condition}の予防・ケアをサポート

### {condition}の予防について

{condition}は適切なケアで進行を遅らせることが可能です。{area}の皆様の健康維持をサポートします。

### 予防のポイント

1. **定期的な身体のケア**
   - マッサージによる血行促進
   - 関節可動域の維持

2. **早期対応の重要性**
   - 症状が軽いうちからのケア
   - 継続的なサポート

3. **生活習慣の改善**
   - 適度な運動のサポート
   - 身体機能の維持

### {area}での訪問マッサージサービス

{COMPANY_NAME}では、{area}全域で予防ケアをサポートしています。

- 定期的な訪問でケア
- 保険適用可能
- 経験豊富な施術師が対応

### お問い合わせ

**電話**: {CLINIC_PHONE}  
**営業時間**: {BUSINESS_HOURS}

{area}で{condition}の予防・ケアをお考えの方は、お気軽にご相談ください。

---

*最終更新日: {today}*
"""
    
    return title, content

def save_article(title, content, condition, area, category):
    """記事を保存"""
    # 日付フォルダ作成
    date_str = datetime.now().strftime('%Y-%m-%d')
    save_dir = Path(f'/Users/skem/Himawari/blog_articles/{date_str}')
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # ファイル名生成
    filename = f"{condition}_{area}_{category}_{date_str}.md"
    filepath = save_dir / filename
    
    # 記事保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def main():
    """メイン処理"""
    if len(sys.argv) == 4:
        condition = sys.argv[1]
        area = sys.argv[2]
        category = sys.argv[3]
    else:
        # ランダムに選択
        condition = '関節拘縮'
        area = '旭区'
        category = 'symptom_guide'
    
    print(f"\n{'='*60}")
    print(f"記事生成開始")
    print(f"{'='*60}")
    print(f"症状: {condition}")
    print(f"地域: {area}")
    print(f"カテゴリ: {category}")
    
    # 記事生成
    title, content = generate_article_content(condition, area, category)
    
    # 記事保存
    filepath = save_article(title, content, condition, area, category)
    
    print(f"\n✅ 記事生成完了")
    print(f"📄 タイトル: {title}")
    print(f"📁 保存先: {filepath}")
    print(f"📊 文字数: {len(content)} 文字")
    
    # Jekyll用ファイルも生成
    jekyll_dir = Path('/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/_posts')
    jekyll_filename = f"{datetime.now().strftime('%Y-%m-%d')}-{condition}-{area}-{category}.md"
    jekyll_path = jekyll_dir / jekyll_filename
    
    # Front Matter追加
    jekyll_content = f"""---
layout: post
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d')}
categories: {category.replace('_', '-')}
area: {area}
condition: {condition}
---

{content}
"""
    
    with open(jekyll_path, 'w', encoding='utf-8') as f:
        f.write(jekyll_content)
    
    print(f"📝 Jekyll記事: {jekyll_path}")
    print(f"\n{'='*60}")
    print(f"記事生成・保存完了！")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()