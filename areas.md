---
layout: default
title: "対応地域一覧 | ひまわり治療院"
description: "ひまわり治療院の対応地域一覧ページ。大阪市内各区での訪問マッサージ記事をご覧いただけます。"
permalink: /areas/
---

# 対応地域一覧

ひまわり治療院では、大阪市内全域で訪問マッサージを行っております。
各地域をクリックすると、その地域に関する記事一覧をご覧いただけます。

<div class="areas-grid">
{% for area in site.areas %}
  <div class="area-card">
    <h3><a href="/areas/{{ area | url_encode }}/">大阪市{{ area }}</a></h3>
    <p>{{ area }}での訪問マッサージ記事一覧</p>
  </div>
{% endfor %}
</div>

## お問い合わせ

お住まいの地域での訪問マッサージをご希望の方は、お気軽にご相談ください。

- **電話:** {{ site.data.business.phone }}
- **営業時間:** {{ site.data.business.business_hours }}
- **対応エリア:** {{ site.data.business.service_area }}

<style>
.areas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 20px 0;
}

.area-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  transition: box-shadow 0.3s ease;
}

.area-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.area-card h3 {
  margin: 0 0 10px 0;
  font-size: 1.1em;
}

.area-card a {
  text-decoration: none;
  color: #333;
}

.area-card a:hover {
  color: #007cba;
}
</style>