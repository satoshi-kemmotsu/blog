---
layout: home
title: "ひまわり治療院ブログ | 大阪市訪問マッサージ・医療保険適用"
description: "大阪市での訪問マッサージ・在宅医療マッサージの専門情報。脊柱管狭窄症、脳梗塞、パーキンソン病など各種傷病の症状改善事例、予防法、よくある質問を専門家が解説。医療保険適用で安心の在宅ケア。"
---

<!-- ヒーローセクション -->
<div class="hero-section">
  <div class="hero-image">
    <img src="/assets/images/hero-massage.jpg" alt="ひまわり治療院の訪問マッサージ">
  </div>
  
  <div class="hero-content">
    <h1>大阪市訪問マッサージ専門</h1>
    <h2>ひまわり治療院</h2>
    <p>医療保険適用の訪問マッサージで、大阪市内のご自宅にお伺いいたします。脊柱管狭窄症、脳梗塞、パーキンソン病など、様々な症状でお困りの方への専門的なケアをご提供します。</p>
    
    <div class="hero-cta">
      <a href="{{ site.clinic_info.main_site }}" target="_blank" class="cta-button">
        📞 無料体験のお申込み
      </a>
      <div class="contact-info">
        <div class="phone">{{ site.clinic_info.phone }}</div>
        <div class="hours">{{ site.clinic_info.hours }}</div>
      </div>
    </div>
  </div>
</div>

## 専門情報サイト

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
/* シンプルなヒーローセクション */
.hero-section {
  margin: 20px 0;
  background: #f8f9fa;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.hero-image {
  width: 100%;
  height: 250px;
  overflow: hidden;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-content {
  padding: 30px;
  text-align: center;
}

.hero-content h1 {
  color: #DB7093;
  font-size: 1.8rem;
  margin: 0 0 10px 0;
  font-weight: bold;
}

.hero-content h2 {
  color: #FFB6C1;
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.hero-content p {
  color: #555;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 25px;
}

.cta-button {
  display: inline-block;
  background: linear-gradient(45deg, #FFB6C1, #F8BBD9);
  color: white;
  padding: 15px 25px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: bold;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 182, 193, 0.4);
  text-decoration: none;
  background: linear-gradient(45deg, #F8BBD9, #DDA0DD);
}

.contact-info {
  margin-top: 15px;
}

.phone {
  font-size: 1.2rem;
  font-weight: bold;
  color: #DB7093;
  margin-bottom: 5px;
}

.hours {
  font-size: 0.9rem;
  color: #666;
}

/* モバイル対応 */
@media (max-width: 768px) {
  .hero-section {
    margin: 10px 0;
    border-radius: 8px;
  }
  
  .hero-image {
    height: 200px;
  }
  
  .hero-content {
    padding: 20px;
  }
  
  .hero-content h1 {
    font-size: 1.5rem;
  }
  
  .hero-content h2 {
    font-size: 1.3rem;
  }
  
  .hero-content p {
    font-size: 0.95rem;
  }
  
  .cta-button {
    padding: 12px 20px;
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .hero-content {
    padding: 15px;
  }
  
  .hero-content h1 {
    font-size: 1.3rem;
  }
  
  .hero-content h2 {
    font-size: 1.2rem;
  }
  
  .cta-button {
    width: 100%;
    padding: 12px;
  }
}

/* 既存のスタイル */
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
  background: #FFB6C1;
  color: white;
  border-color: #FFB6C1;
  transform: translateY(-2px);
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.view-all-link {
  color: #DB7093;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1em;
}

.view-all-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .conditions-grid, .areas-grid {
    gap: 8px;
  }
  
  .condition-link, .area-link {
    padding: 6px 12px;
    font-size: 0.85em;
  }
}
</style>

## 最新記事

症状別・地域別の専門情報を毎日更新中です。