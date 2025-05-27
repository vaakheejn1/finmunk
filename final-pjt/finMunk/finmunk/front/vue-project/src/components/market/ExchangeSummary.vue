<template>
    <div class="exchange-grid">
      <div class="exchange-card">
        <div class="exchange-header">
          <div class="currency-info">
            <div class="currency-flag kospi">📈</div>
            <div>
              <div class="currency-label">KOSPI</div>
              <div class="exchange-value">{{ financial.KOSPI ?? '-' }}p</div>
            </div>
          </div>
        </div>
        <div class="change-rate">{{ dateLabel }}</div>
      </div>
  
      <div class="exchange-card">
        <div class="exchange-header">
          <div class="currency-info">
            <div class="currency-flag kosdaq">📉</div>
            <div>
              <div class="currency-label">KOSDAQ</div>
              <div class="exchange-value">{{ financial.KOSDAQ ?? '-' }}p</div>
            </div>
          </div>
        </div>
        <div class="change-rate">{{ dateLabel }}</div>
      </div>
  
      <div class="exchange-card">
        <div class="exchange-header">
          <div class="currency-info">
            <div class="currency-flag rate">📊</div>
            <div>
              <div class="currency-label">기준금리</div>
              <div class="exchange-value">3.5%</div>
            </div>
          </div>
        </div>
        <div class="change-rate">동결 유지</div>
      </div>
  
      <div class="exchange-card">
        <div class="exchange-header">
          <div class="currency-info">
            <div class="currency-flag cpi">📊</div>
            <div>
              <div class="currency-label">소비자물가지수 (CPI)</div>
              <div class="exchange-value">108.4</div>
            </div>
          </div>
        </div>
        <div class="change-rate positive">+0.3p (+0.3%)</div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  const props = defineProps({
    financial: Object,
    dateLabel: String
  })
  </script>
  
  <style scoped>
  .exchange-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
    gap: 20px;
    margin-bottom: 50px;
    width: 100%;
    max-width: 1200px;
  }
  
  .exchange-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    border: 1px solid #f0f0f0;
    transition: all 0.3s ease;
  }
  
  .exchange-card:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
  }
  
  .exchange-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
  }
  
  .currency-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .currency-flag {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    background-color: #F0FFFA;
    border: 2px solid #E5FAF3;
  }
  
  .kospi {
    border-color: #E5F0FF;
    background-color: #F0F7FF;
  }
  
  .kosdaq {
    border-color: #FFE5E5;
    background-color: #FFF5F5;
  }
  
  .rate {
    border-color: #FFF0E5;
    background-color: #FFFAF5;
  }
  
  .cpi {
    border-color: #F0E5FF;
    background-color: #F8F5FF;
  }
  
  .currency-label {
    font-size: 13px;
    color: #888;
    font-weight: 500;
  }
  
  .exchange-value {
    font-size: 26px;
    font-weight: 700;
    color: #222;
  }
  
  .change-rate {
    font-size: 14px;
    margin-top: 5px;
    font-weight: 500;
  }
  
  .positive {
    color: #FF5252;
  }
  </style>