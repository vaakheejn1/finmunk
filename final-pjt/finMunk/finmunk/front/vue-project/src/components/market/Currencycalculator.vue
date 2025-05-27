<template>
    <div v-if="isOpen" class="calculator-overlay" @click.self="closeCalculator">
      <div class="calculator-modal">
        <div class="calculator-header">
          <h2>🧮 환율계산기</h2>
          <button class="close-btn" @click="closeCalculator">✕</button>
        </div>
        
        <div class="calculator-body">
          <div class="exchange-info">
            <div class="info-item">
              <span class="label">USD/KRW</span>
              <span class="rate">{{ rates.USD || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="label">JPY/KRW</span>
              <span class="rate">{{ rates.JPY || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="label">EUR/KRW</span>
              <span class="rate">{{ rates.EUR || '-' }}</span>
            </div>
          </div>
  
          <div class="calculator-section">
            <div class="input-group">
              <label>금액</label>
              <input 
                type="number" 
                v-model="amount" 
                placeholder="금액을 입력하세요"
                @input="calculate"
                class="amount-input"
              >
            </div>
  
            <div class="currency-selectors">
              <div class="selector-group">
                <label>From</label>
                <select v-model="fromCurrency" @change="calculate" class="currency-select">
                  <option value="KRW">🇰🇷 한국 원 (KRW)</option>
                  <option value="USD">🇺🇸 미국 달러 (USD)</option>
                  <option value="JPY">🇯🇵 일본 엔 (JPY)</option>
                  <option value="EUR">🇪🇺 유로 (EUR)</option>
                  <option value="GBP">🇬🇧 영국 파운드 (GBP)</option>
                  <option value="CNY">🇨🇳 중국 위안 (CNY)</option>
                  <option value="AUD">🇦🇺 호주 달러 (AUD)</option>
                  <option value="CAD">🇨🇦 캐나다 달러 (CAD)</option>
                  <option value="CHF">🇨🇭 스위스 프랑 (CHF)</option>
                  <option value="HKD">🇭🇰 홍콩 달러 (HKD)</option>
                </select>
              </div>
  
              <div class="swap-btn" @click="swapCurrencies">
                🔄
              </div>
  
              <div class="selector-group">
                <label>To</label>
                <select v-model="toCurrency" @change="calculate" class="currency-select">
                  <option value="KRW">🇰🇷 한국 원 (KRW)</option>
                  <option value="USD">🇺🇸 미국 달러 (USD)</option>
                  <option value="JPY">🇯🇵 일본 엔 (JPY)</option>
                  <option value="EUR">🇪🇺 유로 (EUR)</option>
                  <option value="GBP">🇬🇧 영국 파운드 (GBP)</option>
                  <option value="CNY">🇨🇳 중국 위안 (CNY)</option>
                  <option value="AUD">🇦🇺 호주 달러 (AUD)</option>
                  <option value="CAD">🇨🇦 캐나다 달러 (CAD)</option>
                  <option value="CHF">🇨🇭 스위스 프랑 (CHF)</option>
                  <option value="HKD">🇭🇰 홍콩 달러 (HKD)</option>
                </select>
              </div>
            </div>
  
            <div class="result-section" v-if="result !== null">
              <div class="result-card">
                <div class="result-amount">{{ formatResult(result) }}</div>
                <div class="result-label">{{ getCurrencyName(toCurrency) }}</div>
              </div>
              <div class="rate-info">
                1 {{ fromCurrency }} = {{ getCurrentRate() }} {{ toCurrency }}
              </div>
            </div>
  
            <div class="quick-amounts">
              <span class="quick-label">빠른 금액:</span>
              <button 
                v-for="quickAmount in quickAmounts" 
                :key="quickAmount"
                @click="setQuickAmount(quickAmount)"
                class="quick-btn"
              >
                {{ formatNumber(quickAmount) }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  
  const props = defineProps({
    isOpen: Boolean,
    rates: Object
  })
  
  const emit = defineEmits(['close'])
  
  const amount = ref('')
  const fromCurrency = ref('KRW')
  const toCurrency = ref('USD')
  const result = ref(null)
  
  const quickAmounts = [10000, 50000, 100000, 500000, 1000000]
  
  const currencyNames = {
    KRW: '한국 원',
    USD: '미국 달러',
    JPY: '일본 엔',
    EUR: '유로',
    GBP: '영국 파운드',
    CNY: '중국 위안',
    AUD: '호주 달러',
    CAD: '캐나다 달러',
    CHF: '스위스 프랑',
    HKD: '홍콩 달러'
  }
  
  function closeCalculator() {
    emit('close')
  }
  
  function calculate() {
    if (!amount.value || amount.value <= 0) {
      result.value = null
      return
    }
  
    const fromRate = getRate(fromCurrency.value)
    const toRate = getRate(toCurrency.value)
    
    if (!fromRate || !toRate) {
      result.value = null
      return
    }
  
    // KRW를 기준으로 계산
    let krwAmount
    if (fromCurrency.value === 'KRW') {
      krwAmount = parseFloat(amount.value)
    } else {
      krwAmount = parseFloat(amount.value) * fromRate
    }
  
    if (toCurrency.value === 'KRW') {
      result.value = krwAmount
    } else {
      result.value = krwAmount / toRate
    }
  }
  
  function getRate(currency) {
    if (currency === 'KRW') return 1
    return parseFloat(props.rates[currency]) || null
  }
  
  function getCurrentRate() {
    const fromRate = getRate(fromCurrency.value)
    const toRate = getRate(toCurrency.value)
    
    if (!fromRate || !toRate) return '-'
    
    let rate
    if (fromCurrency.value === 'KRW') {
      rate = 1 / toRate
    } else if (toCurrency.value === 'KRW') {
      rate = fromRate
    } else {
      rate = fromRate / toRate
    }
    
    return formatNumber(rate, 4)
  }
  
  function swapCurrencies() {
    const temp = fromCurrency.value
    fromCurrency.value = toCurrency.value
    toCurrency.value = temp
    calculate()
  }
  
  function setQuickAmount(quickAmount) {
    amount.value = quickAmount
    calculate()
  }
  
  function formatResult(value) {
    return formatNumber(value, 2)
  }
  
  function formatNumber(value, decimals = 0) {
    if (value === null || value === undefined) return '-'
    return new Intl.NumberFormat('ko-KR', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value)
  }
  
  function getCurrencyName(currency) {
    return currencyNames[currency] || currency
  }
  
  // amount 변경 시 자동 계산
  watch([amount, fromCurrency, toCurrency], calculate)
  
  // 모달이 열릴 때 초기화
  watch(() => props.isOpen, (isOpen) => {
    if (isOpen) {
      amount.value = ''
      result.value = null
    }
  })
  </script>
  
  <style scoped>
.calculator-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  overflow-y: auto;
}
  
  .calculator-modal {
    background: white;
    border-radius: 20px;
    width: 100%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  }
  
  .calculator-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .calculator-header h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 700;
    color: #333;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #999;
    padding: 0;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }
  
  .close-btn:hover {
    background-color: #f5f5f5;
    color: #666;
  }
  
  .calculator-body {
    padding: 24px;
  }
  
  .exchange-info {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    padding: 16px;
    background-color: #f8fffe;
    border-radius: 12px;
    border: 1px solid #e5faf3;
  }
  
  .info-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
  }
  
  .label {
    font-size: 12px;
    color: #888;
    margin-bottom: 4px;
  }
  
  .rate {
    font-size: 14px;
    font-weight: 600;
    color: #4DD0B1;
  }
  
  .calculator-section {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  
  .input-group label,
  .selector-group label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }
  
  .amount-input {
    width: 100%;
    padding: 16px;
    border: 2px solid #e8e8e8;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 600;
    text-align: center;
    transition: border-color 0.2s;
  }
  
  .amount-input:focus {
    outline: none;
    border-color: #4DD0B1;
  }
  
  .currency-selectors {
    display: flex;
    align-items: end;
    gap: 16px;
  }
  
  .selector-group {
    flex: 1;
  }
  
  .currency-select {
    width: 100%;
    padding: 12px;
    border: 2px solid #e8e8e8;
    border-radius: 12px;
    font-size: 14px;
    background-color: white;
    cursor: pointer;
    transition: border-color 0.2s;
  }
  
  .currency-select:focus {
    outline: none;
    border-color: #4DD0B1;
  }
  
  .swap-btn {
    background-color: #4DD0B1;
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.2s;
    margin-bottom: 2px;
  }
  
  .swap-btn:hover {
    background-color: #3CBFA0;
    transform: rotate(180deg);
  }
  
  .result-section {
    text-align: center;
    padding: 24px;
    background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
    border-radius: 16px;
    color: white;
  }
  
  .result-card {
    margin-bottom: 12px;
  }
  
  .result-amount {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 4px;
  }
  
  .result-label {
    font-size: 16px;
    opacity: 0.9;
  }
  
  .rate-info {
    font-size: 14px;
    opacity: 0.8;
  }
  
  .quick-amounts {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  
  .quick-label {
    font-size: 14px;
    color: #666;
    margin-right: 8px;
  }
  
  .quick-btn {
    padding: 8px 16px;
    border: 1px solid #e8e8e8;
    border-radius: 20px;
    background: white;
    color: #666;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .quick-btn:hover {
    border-color: #4DD0B1;
    color: #4DD0B1;
    background-color: #f8fffe;
  }
  
  @media (max-width: 600px) {
    .calculator-modal {
      margin: 10px;
      max-width: none;
    }
    
    .exchange-info {
      flex-direction: column;
      gap: 12px;
    }
    
    .currency-selectors {
      flex-direction: column;
      gap: 16px;
    }
    
    .swap-btn {
      align-self: center;
      transform: rotate(90deg);
    }
    
    .swap-btn:hover {
      transform: rotate(270deg);
    }
    
    .quick-amounts {
      justify-content: center;
    }
    
    .result-amount {
      font-size: 28px;
    }
  }
  </style>