---
layout: default
title: "記事一覧 | ひまわり治療院ブログ"
description: "大阪市での訪問マッサージ・在宅医療マッサージの専門記事一覧。症状別・地域別の情報を日付順にご覧いただけます。"
permalink: /archive/
---

# 記事一覧

大阪市での訪問マッサージ・在宅医療マッサージの専門記事を日付順にご覧いただけます。

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

## 📅 日付別記事一覧

<div class="archive-list">
{% for post in site.posts %}
  <article class="archive-item">
    <div class="archive-meta">
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y年%m月%d日" }}</time>
      {% if post.categories[0] %}
        {% case post.categories[0] %}
          {% when 'symptom_guide' %}
            <span class="category">症状解説</span>
          {% when 'case_study' %}
            <span class="category">ケア事例</span>
          {% when 'qa' %}
            <span class="category">よくある質問</span>
          {% when 'prevention' %}
            <span class="category">セルフケア</span>
          {% else %}
            <span class="category">{{ post.categories[0] }}</span>
        {% endcase %}
      {% endif %}
    </div>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    {% if post.description %}
      <p class="excerpt">{{ post.description | strip_html | truncate: 150 }}</p>
    {% else %}
      <p class="excerpt">{{ post.content | strip_html | truncate: 150 }}</p>
    {% endif %}
    {% if post.tags %}
      <div class="tags">
        {% for tag in post.tags limit:5 %}
          <span class="tag">{{ tag }}</span>
        {% endfor %}
      </div>
    {% endif %}
  </article>
{% endfor %}
</div>

{% endif %}

---

## 📍 カテゴリ別記事

<div class="category-links">
  <a href="/symptoms/" class="category-button">症状別記事</a>
  <a href="/areas/" class="category-button">地域別記事</a>
  <a href="/" class="category-button">トップページ</a>
</div>

<style>
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

.category-links {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin: 30px 0;
  flex-wrap: wrap;
}

.category-button {
  display: inline-block;
  background: linear-gradient(45deg, #FFB6C1, #F8BBD9);
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.category-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 182, 193, 0.4);
  text-decoration: none;
  background: linear-gradient(45deg, #F8BBD9, #DDA0DD);
}

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
  
  .category-links {
    flex-direction: column;
    align-items: center;
  }
  
  .category-button {
    width: 200px;
    text-align: center;
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
}
</style>