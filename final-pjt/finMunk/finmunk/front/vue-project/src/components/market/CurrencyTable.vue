<template>
    <section class="currency-table-container">
      <div class="section-header">
        <h2 class="section-title">주요 통화 현황</h2>
        <button class="calculator-btn" @click="$emit('openCalculator')">
          <span>🧮</span>
          환율계산기
        </button>
      </div>
      <table class="currency-table">
        <thead>
          <tr>
            <th>통화</th>
            <th>현재 환율</th>
            <th>전일 대비</th>
            <th>변동률</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(info, code) in rates" :key="code">
            <td>
              <div class="currency-name">
                <div class="currency-icon">{{ code }}</div>
                <span>{{ code }}/KRW{{ code === 'JPY' ? ' (100엔)' : '' }}</span>
              </div>
            </td>
            <td>{{ info.today?.toFixed(2) ?? '-' }}원</td>
            <td :class="rateClass(info.diff)">
              {{ info.diff?.toFixed(2) ?? '-' }}원
              <span v-if="info.diff > 0">(↑)</span>
              <span v-else-if="info.diff < 0">(↓)</span>
            </td>
            <td :class="rateClass(info.rate)">
              {{ info.rate?.toFixed(2) ?? '-' }}%
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </template>
  
  <script setup>
  defineProps(['rates'])
  const rateClass = (val) => val > 0 ? 'positive' : val < 0 ? 'negative' : ''
  </script>
  
  <style scoped>
  .currency-table-container {
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
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .calculator-btn {
    background: #4DD0B1;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .calculator-btn:hover {
    background: #3CBFA0;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(77, 208, 177, 0.3);
  }
  
  .currency-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .currency-table th {
    text-align: left;
    padding: 16px;
    color: #666;
    font-weight: 600;
    font-size: 14px;
    border-bottom: 2px solid #f8f8f8;
  }
  
  .currency-table td {
    padding: 18px 16px;
    border-bottom: 1px solid #fafafa;
  }
  
  .currency-table tbody tr:hover {
    background-color: #fcfcfc;
  }
  
  .currency-name {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .currency-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    background-color: #F0FFFA;
    border: 2px solid #E5FAF3;
  }
  
  .positive { color: #FF5252; }
  .negative { color: #2196F3; }
  </style>