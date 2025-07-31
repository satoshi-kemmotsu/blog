---
layout: default
title: "症状別一覧 | ひまわり治療院"
description: "ひまわり治療院で対応可能な症状の一覧ページ。各症状に関する詳細記事をご覧いただけます。"
permalink: /symptoms/
---

# 対応症状一覧

ひまわり治療院では、以下の症状に対応した訪問マッサージを行っております。
各症状をクリックすると、関連する記事一覧をご覧いただけます。

<div class="symptoms-grid">
{% for condition in site.conditions %}
  <div class="symptom-card">
    <h3><a href="/symptoms/{{ condition | url_encode }}/">{{ condition }}</a></h3>
    <p>{{ condition }}に関する記事一覧</p>
  </div>
{% endfor %}
</div>

## お問い合わせ

症状でお悩みの方は、お気軽にご相談ください。

- **電話:** {{ site.clinic_info.phone }}
- **営業時間:** {{ site.clinic_info.hours }}
- **対応エリア:** {{ site.clinic_info.area }}

<style>
.symptoms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.symptom-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: box-shadow 0.3s ease;
}

.symptom-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.symptom-card h3 {
  margin: 0 0 10px 0;
}

.symptom-card a {
  text-decoration: none;
  color: #333;
}

.symptom-card a:hover {
  color: #007cba;
}
</style>