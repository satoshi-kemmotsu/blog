---
layout: home
title: "ひまわり治療院ブログ | 大阪市訪問マッサージ・医療保険適用"
description: "大阪市での訪問マッサージ・在宅医療マッサージの専門情報。脊柱管狭窄症、脳梗塞、パーキンソン病など各種傷病の症状改善事例、予防法、よくある質問を専門家が解説。医療保険適用で安心の在宅ケア。"
---

<!-- ヒーローセクション -->
<section class="hero">
  <div class="hero-image">
    <img src="/assets/images/hero-massage.jpg" alt="ひまわり治療院の訪問マッサージ - 専門スタッフによる在宅リハビリテーション">
  </div>
  <div class="hero-content">
    <h1 class="hero-title">大阪市訪問マッサージ専門</h1>
    <h2 class="hero-subtitle">ひまわり治療院</h2>
    <p class="hero-description">
      医療保険適用の訪問マッサージで、大阪市内のご自宅にお伺いいたします。<br>
      脊柱管狭窄症、脳梗塞、パーキンソン病など、様々な症状でお困りの方への<br>
      専門的なケアをご提供します。
    </p>
    <div class="hero-cta">
      <a href="{{ site.clinic_info.main_site }}" target="_blank" class="cta-button-primary">
        📞 無料体験のお申込み
      </a>
      <div class="hero-contact">
        <span class="phone-number">{{ site.clinic_info.phone }}</span>
        <span class="hours">{{ site.clinic_info.hours }}</span>
      </div>
    </div>
  </div>
</section>

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
/* ページ全体の上部余白をリセット */
body {
  margin-top: 0 !important;
  padding-top: 0 !important;
}

.page-content {
  margin-top: 0 !important;
  padding-top: 0 !important;
}

/* ヒーローセクション */
.hero {
  position: relative;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 15px;
  overflow: hidden;
  margin: -20px -15px 40px -15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.hero-image {
  width: 100%;
  height: 400px;
  overflow: hidden;
  position: relative;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.8);
}

.hero-content {
  position: absolute;
  top: 50%;
  left: 50px;
  transform: translateY(-50%);
  color: white;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
  max-width: 600px;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 0 10px 0;
  color: #fff;
}

.hero-subtitle {
  font-size: 2rem;
  color: #ffeb3b;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.hero-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 30px;
  color: #f8f9fa;
}

.hero-cta {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.cta-button-primary {
  display: inline-block;
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
  padding: 15px 30px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(255,107,107,0.4);
  align-self: flex-start;
}

.cta-button-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255,107,107,0.6);
  background: linear-gradient(45deg, #ee5a24, #ff6b6b);
}

.hero-contact {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.phone-number {
  font-size: 1.3rem;
  font-weight: bold;
  color: #ffeb3b;
}

.hours {
  font-size: 1rem;
  color: #f8f9fa;
}

/* タブレット対応 */
@media (max-width: 1024px) {
  .hero-content {
    left: 30px;
    max-width: 500px;
  }
  
  .hero-title {
    font-size: 2.2rem;
  }
  
  .hero-subtitle {
    font-size: 1.8rem;
  }
}

/* モバイル対応 */
@media (max-width: 768px) {
  .hero {
    margin: -20px -10px 30px -10px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    position: relative;
    background: none;
  }
  
  .hero-image {
    height: 200px;
    position: relative;
  }
  
  .hero-content {
    position: relative;
    top: auto;
    left: auto;
    transform: none;
    padding: 20px;
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: white;
    text-shadow: none;
    max-width: none;
  }
  
  .hero-title {
    font-size: 1.6rem;
    margin-bottom: 8px;
  }
  
  .hero-subtitle {
    font-size: 1.3rem;
    margin-bottom: 15px;
  }
  
  .hero-description {
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 20px;
  }
  
  .hero-cta {
    align-items: center;
  }
  
  .cta-button-primary {
    align-self: center;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .hero {
    margin: -10px -10px 20px -10px;
    border-radius: 5px;
  }
  
  .hero-image {
    height: 180px;
  }
  
  .hero-content {
    padding: 15px;
  }
  
  .hero-title {
    font-size: 1.4rem;
    margin-bottom: 6px;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
    margin-bottom: 12px;
  }
  
  .hero-description {
    font-size: 0.9rem;
    margin-bottom: 15px;
    br {
      display: none;
    }
  }
  
  .cta-button-primary {
    padding: 12px 20px;
    font-size: 1rem;
    width: 100%;
    text-align: center;
  }
  
  .hero-contact {
    text-align: center;
    margin-top: 10px;
  }
  
  .phone-number {
    font-size: 1.1rem;
  }
  
  .hours {
    font-size: 0.9rem;
  }
  
  /* モバイル時のコンテンツグリッドも調整 */
  .conditions-grid, .areas-grid {
    gap: 8px;
  }
  
  .condition-link, .area-link {
    padding: 6px 12px;
    font-size: 0.85em;
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