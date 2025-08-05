---
layout: default
title: "記事一覧 | ひまわり治療院ブログ"
description: "大阪市での訪問マッサージ・在宅医療マッサージの専門記事一覧。症状解説、ケア事例、セルフケア、よくある質問をカテゴリ別にご覧いただけます。"
permalink: /archive/
---

# 記事一覧

大阪市での訪問マッサージ・在宅医療マッサージの専門記事をカテゴリ別にご覧いただけます。

<div class="archive-header">
  <p>📝 総記事数: <strong>{{ site.posts.size }}件</strong></p>
  <p>🔄 最終更新: <strong>{% if site.posts.first %}{{ site.posts.first.date | date: "%Y年%m月%d日" }}{% else %}記事準備中{% endif %}</strong></p>
</div>

{% if site.posts.size == 0 %}
<div class="no-articles">
  <p>🌻 記事準備中です。まもなく更新予定です！</p>
  <p><a href="/">← トップページに戻る</a></p>
</div>
{% else %}

<!-- カテゴリ別タブナビゲーション -->
<div class="category-tabs">
  <input type="radio" id="tab-all" name="category-tab" checked>
  <label for="tab-all" class="tab-label">📋 すべて ({{ site.posts.size }})</label>
  
  <input type="radio" id="tab-symptom" name="category-tab">
  <label for="tab-symptom" class="tab-label">🩺 症状解説 ({% assign symptom_posts = site.posts | where: 'categories', 'symptom_guide' %}{{ symptom_posts.size }})</label>
  
  <input type="radio" id="tab-case" name="category-tab">
  <label for="tab-case" class="tab-label">📊 ケア事例 ({% assign case_posts = site.posts | where: 'categories', 'case_study' %}{{ case_posts.size }})</label>
  
  <input type="radio" id="tab-prevention" name="category-tab">
  <label for="tab-prevention" class="tab-label">💪 セルフケア ({% assign prevention_posts = site.posts | where: 'categories', 'prevention' %}{{ prevention_posts.size }})</label>
  
  <input type="radio" id="tab-qa" name="category-tab">
  <label for="tab-qa" class="tab-label">❓ よくある質問 ({% assign qa_posts = site.posts | where: 'categories', 'qa' %}{{ qa_posts.size }})</label>

  <!-- すべての記事 -->
  <div class="tab-content" id="content-all">
    <h2>📅 すべての記事 (最新20件)</h2>
    <div class="archive-list">
      {% for post in site.posts limit:20 %}
        {% include archive-item.html %}
      {% endfor %}
    </div>
    {% if site.posts.size > 20 %}
      <div class="pagination-info">
        <p>📄 表示: 最新20件 / 全{{ site.posts.size }}件</p>
      </div>
    {% endif %}
  </div>

  <!-- 症状解説 -->
  <div class="tab-content" id="content-symptom">
    <h2>🩺 症状解説記事</h2>
    <div class="archive-list">
      {% assign symptom_posts = site.posts | where: 'categories', 'symptom_guide' %}
      {% for post in symptom_posts limit:15 %}
        {% include archive-item.html %}
      {% endfor %}
    </div>
    {% if symptom_posts.size > 15 %}
      <div class="pagination-info">
        <p>📄 表示: 最新15件 / 全{{ symptom_posts.size }}件</p>
      </div>
    {% endif %}
  </div>

  <!-- ケア事例 -->
  <div class="tab-content" id="content-case">
    <h2>📊 ケア事例記事</h2>
    <div class="archive-list">
      {% assign case_posts = site.posts | where: 'categories', 'case_study' %}
      {% for post in case_posts limit:15 %}
        {% include archive-item.html %}
      {% endfor %}
    </div>
    {% if case_posts.size > 15 %}
      <div class="pagination-info">
        <p>📄 表示: 最新15件 / 全{{ case_posts.size }}件</p>
      </div>
    {% endif %}
  </div>

  <!-- セルフケア -->
  <div class="tab-content" id="content-prevention">
    <h2>💪 セルフケア記事</h2>
    <div class="archive-list">
      {% assign prevention_posts = site.posts | where: 'categories', 'prevention' %}
      {% for post in prevention_posts limit:15 %}
        {% include archive-item.html %}
      {% endfor %}
    </div>
    {% if prevention_posts.size > 15 %}
      <div class="pagination-info">
        <p>📄 表示: 最新15件 / 全{{ prevention_posts.size }}件</p>
      </div>
    {% endif %}
  </div>

  <!-- よくある質問 -->
  <div class="tab-content" id="content-qa">
    <h2>❓ よくある質問記事</h2>
    <div class="archive-list">
      {% assign qa_posts = site.posts | where: 'categories', 'qa' %}
      {% for post in qa_posts limit:15 %}
        {% include archive-item.html %}
      {% endfor %}
    </div>
    {% if qa_posts.size > 15 %}
      <div class="pagination-info">
        <p>📄 表示: 最新15件 / 全{{ qa_posts.size }}件</p>
      </div>
    {% endif %}
  </div>
</div>

{% endif %}

---

## 📍 地域別記事検索

<div class="area-filter">
  <h3>🗾 大阪市24区別記事</h3>
  <div class="area-grid">
    {% assign areas = "中央区,北区,西区,港区,大正区,天王寺区,浪速区,西成区,阿倍野区,住吉区,東住吉区,住之江区,平野区,生野区,東成区,旭区,城東区,鶴見区,淀川区,西淀川区,東淀川区,福島区,此花区,都島区" | split: "," %}
    {% for area in areas %}
      {% assign area_posts = site.posts | where_exp: "post", "post.tags contains area" %}
      {% if area_posts.size > 0 %}
        <a href="#area-{{ area }}" class="area-tag active" data-area="{{ area }}">{{ area }} ({{ area_posts.size }})</a>
      {% else %}
        <span class="area-tag inactive">{{ area }} (0)</span>
      {% endif %}
    {% endfor %}
  </div>
</div>

<style>
/* 既存のスタイルを保持 */
.archive-header {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
  border-left: 4px solid #FFB6C1;
}

.archive-header p {
  margin: 5px 0;
  font-size: 1.1rem;
}

.archive-list {
  margin: 30px 0;
}

.archive-item {
  background: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.archive-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
  border-color: #FFB6C1;
}

.archive-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.archive-meta time {
  color: #666;
  font-weight: bold;
}

.category {
  background: #FFB6C1;
  color: white;
  padding: 3px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
}

.archive-item h3 {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
  line-height: 1.4;
}

.archive-item h3 a {
  color: #333;
  text-decoration: none;
  transition: color 0.3s ease;
}

.archive-item h3 a:hover {
  color: #DB7093;
}

.excerpt {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 10px 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 15px;
}

.tag {
  background: #e9ecef;
  color: #495057;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  transition: all 0.3s ease;
}

.tag:hover {
  background: #FFB6C1;
  color: white;
}

.no-articles {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  margin: 30px 0;
}

.no-articles p {
  margin: 10px 0;
  color: #856404;
  font-weight: bold;
}

/* 新しいカテゴリタブスタイル */
.category-tabs {
  margin: 30px 0;
}

.category-tabs input[type="radio"] {
  display: none;
}

.tab-label {
  display: inline-block;
  background: #f8f9fa;
  color: #666;
  padding: 12px 20px;
  margin: 0 5px 10px 0;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  font-size: 0.9rem;
  border: 2px solid #dee2e6;
}

.tab-label:hover {
  background: #FFB6C1;
  color: white;
  border-color: #FFB6C1;
  transform: translateY(-2px);
}

.category-tabs input[type="radio"]:checked + .tab-label {
  background: linear-gradient(45deg, #FFB6C1, #F8BBD9);
  color: white;
  border-color: #FFB6C1;
  box-shadow: 0 4px 12px rgba(255, 182, 193, 0.3);
}

.tab-content {
  display: none;
  margin-top: 30px;
}

.category-tabs input[type="radio"]:checked ~ .tab-content {
  display: none;
}

.category-tabs input[type="radio"]#tab-all:checked ~ #content-all,
.category-tabs input[type="radio"]#tab-symptom:checked ~ #content-symptom,
.category-tabs input[type="radio"]#tab-case:checked ~ #content-case,
.category-tabs input[type="radio"]#tab-prevention:checked ~ #content-prevention,
.category-tabs input[type="radio"]#tab-qa:checked ~ #content-qa {
  display: block;
}

.pagination-info {
  background: #e9ecef;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  margin: 20px 0;
  border-left: 4px solid #6c757d;
}

.pagination-info p {
  margin: 0;
  color: #495057;
  font-weight: bold;
}

/* 地域フィルタースタイル */
.area-filter {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 25px;
  margin: 30px 0;
  border-left: 4px solid #28a745;
}

.area-filter h3 {
  margin: 0 0 20px 0;
  color: #333;
  text-align: center;
}

.area-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px;
  margin-top: 15px;
}

.area-tag {
  display: inline-block;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
  text-align: center;
  transition: all 0.3s ease;
  text-decoration: none;
}

.area-tag.active {
  background: #28a745;
  color: white;
  cursor: pointer;
}

.area-tag.active:hover {
  background: #218838;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.area-tag.inactive {
  background: #e9ecef;
  color: #6c757d;
  cursor: default;
}

/* レスポンシブ対応 */
@media (max-width: 768px) {
  .archive-item {
    padding: 15px;
  }
  
  .archive-item h3 {
    font-size: 1.1rem;
  }
  
  .archive-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .tab-label {
    display: block;
    margin: 5px 0;
    text-align: center;
  }
  
  .area-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 8px;
  }
  
  .area-tag {
    font-size: 0.8rem;
    padding: 6px 10px;
  }
}

@media (max-width: 480px) {
  .archive-header {
    padding: 15px;
  }
  
  .archive-item {
    padding: 12px;
  }
  
  .archive-item h3 {
    font-size: 1rem;
  }
  
  .tab-label {
    font-size: 0.8rem;
    padding: 10px 15px;
  }
  
  .area-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>