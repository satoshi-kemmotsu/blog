---
layout: home
title: "ひまわり治療院ブログ | 大阪市訪問マッサージ・医療保険適用"
description: "大阪市での訪問マッサージ・在宅医療マッサージの専門情報。脊柱管狭窄症、脳梗塞、パーキンソン病など各種傷病の症状改善事例、予防法、よくある質問を専門家が解説。医療保険適用で安心の在宅ケア。"
---

# 大阪市訪問マッサージ専門ブログ

## ひまわり治療院の専門情報サイト

医療保険適用の訪問マッサージで、大阪市内のご自宅にお伺いいたします。
脊柱管狭窄症、脳梗塞、パーキンソン病など、様々な症状でお困りの方への
専門的な情報をお届けします。

### 🏥 対応可能な症状

<div class="conditions-grid">
{% for condition in site.conditions %}
  <a href="/symptoms/{{ condition | url_encode }}/" class="condition-link">{{ condition }}</a>
{% endfor %}
</div>

<p style="text-align: center; margin-top: 15px;">
  <a href="/symptoms/" class="view-all-link">→ 症状別記事一覧を見る</a>
</p>

### 📍 対応エリア

<div class="areas-grid">
{% for area in site.areas %}
  <a href="/areas/{{ area | url_encode }}/" class="area-link">大阪市{{ area }}</a>
{% endfor %}
</div>

<p style="text-align: center; margin-top: 15px;">
  <a href="/areas/" class="view-all-link">→ 地域別記事一覧を見る</a>
</p>

### 📞 お問い合わせ

- **電話:** {{ site.clinic_info.phone }}
- **住所:** {{ site.clinic_info.address }}
- **営業時間:** {{ site.clinic_info.hours }}
- **営業日:** {{ site.clinic_info.days }}
- **対応エリア:** {{ site.clinic_info.area }}

### 🌐 詳細情報

[{{ site.clinic_info.name }}の詳細はこちら]({{ site.clinic_info.main_site }}){:target="_blank"}

---

<style>
.conditions-grid, .areas-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 15px 0;
  justify-content: center;
}

.condition-link, .area-link {
  display: inline-block;
  padding: 8px 16px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 25px;
  text-decoration: none;
  color: #495057;
  font-size: 0.9em;
  transition: all 0.3s ease;
}

.condition-link:hover, .area-link:hover {
  background: #007cba;
  color: white;
  border-color: #007cba;
  transform: translateY(-2px);
}

.view-all-link {
  color: #007cba;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1em;
}

.view-all-link:hover {
  text-decoration: underline;
}
</style>

## 最新記事

症状別・地域別の専門情報を毎日更新中です。