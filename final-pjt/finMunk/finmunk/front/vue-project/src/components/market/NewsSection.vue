<template>
    <section class="news-section">
      <h2 class="section-title">📰 오늘의 금융 뉴스</h2>
      <div class="news-grid">
        <div class="news-card" v-for="article in news" :key="article.title">
          <p class="news-date">{{ article.date }}</p>
          <h3 class="news-title">{{ article.title }}</h3>
          <p class="news-content">{{ article.content.slice(0, 100) }}...</p>
          <a :href="article.link" target="_blank" class="news-link">더 읽기 →</a>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  defineProps(['news'])
  </script>
  
  <style scoped>
  .news-section {
    background: white;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 50px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    border: 1px solid #f0f0f0;
    width: 100%;
  }
  
  .section-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 24px;
    color: #222;
  }
  
  .news-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
  }
  
  .news-card {
    background: #fcfcfc;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    border: 1px solid #f0f0f0;
    transition: all 0.3s;
  }
  
  .news-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transform: translateY(-2px);
  }
  
  .news-date {
    color: #888;
    font-size: 13px;
    margin-bottom: 10px;
    font-weight: 500;
  }
  
  .news-title {
    font-weight: 700;
    margin-bottom: 14px;
    color: #222;
    line-height: 1.5;
    font-size: 18px;
  }
  
  .news-content {
    color: #666;
    font-size: 14px;
    line-height: 1.7;
    margin-bottom: 16px;
  }
  
  .news-link {
    color: #4DD0B1;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    display: inline-block;
  }
  
  .news-link:hover {
    text-decoration: underline;
  }
  
  @media (max-width: 768px) {
    .news-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>