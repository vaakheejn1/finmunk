<template>
  <section class="metal-section">
    <h2 class="section-title">
  <img src="@/assets/clock.png" alt="시계 아이콘" class="title-icon" />
      실시간 금/은 시세
    </h2>

    
    <div class="price-container">
      <div class="metal-card gold">
        <div class="metal-icon">
          <img src="@/assets/gold.png" alt="금 로고" class="metal-img" />
        </div>
        <div class="metal-info">
          <h3 class="metal-name">금 (Gold)</h3>
          <div class="price-row">
            <span class="price-label">국제 시세:</span>
            <span class="price-value">{{ goldPrice.internationalPrice }} USD</span>
          </div>
          <div class="price-row">
            <span class="price-label">국내 시세:</span>
            <span class="price-value">{{ formatNumber(goldPrice.domesticPrice * 3.75) }} 원</span>
          </div>
        </div>
      </div>

      <div class="metal-card silver">
        <div class="metal-icon">
          <img src="@/assets/silver.png" alt="은 로고" class="metal-img" />
        </div>
        <div class="metal-info">
          <h3 class="metal-name">은 (Silver)</h3>
          <div class="price-row">
            <span class="price-label">국제 시세:</span>
            <span class="price-value">{{ silverPrice.internationalPrice }} USD</span>
          </div>
          <div class="price-row">
            <span class="price-label">국내 시세:</span>
            <span class="price-value">{{ formatNumber(silverPrice.domesticPrice * 3.75) }} 원</span>
          </div>
        </div>
      </div>
    </div>

      
      <div class="chart-container">
        <!-- 날짜 필터 섹션 -->
        <div class="date-filter-section">
          <div class="period-buttons">
            <button 
              v-for="period in periodOptions"
              :key="period.value"
              :class="['period-btn', { active: selectedPeriod === period.value }]" 
              @click="selectPeriod(period.value)"
            >
              {{ period.label }}
            </button>
          </div>
          
          <div class="custom-date-filter">
            <div class="date-inputs">
              <div class="date-input-group">
                <label>📅 시작일</label>
                <input 
                  type="date" 
                  v-model="customStartDate" 
                  min="2023-01-01"
                  :max="customEndDate || todayString"
                  @change="applyCustomDateFilter"
                />
              </div>
              <div class="date-input-group">
                <label>📅 종료일</label>
                <input 
                  type="date" 
                  v-model="customEndDate" 
                  min="2023-01-01"
                  :min="customStartDate"
                  :max="todayString"
                  @change="applyCustomDateFilter"
                />
              </div>
              <button class="apply-btn" @click="applyCustomDateFilter">
                적용
              </button>
            </div>
          </div>
        </div>
  
        <!-- 차트 정보 -->
        <div class="chart-info">
          <p class="data-period">
            📊 데이터 기간: {{ formatDate(currentStartDate) }} ~ {{ formatDate(currentEndDate) }} 
            ({{ filteredDataCount }}개 데이터)
          </p>
        </div>
  
        <!-- 차트 탭 -->
        <div class="chart-tabs">
          <button 
            :class="['tab-button', {active: activeTab === 'both-usd'}]" 
            @click="activeTab = 'both-usd'"
          >
            금 & 은 
          </button>
          
          <button 
            :class="['tab-button', {active: activeTab === 'gold'}]" 
            @click="activeTab = 'gold'"
          >
            금 (Gold)
          </button>
          <button 
            :class="['tab-button', {active: activeTab === 'silver'}]" 
            @click="activeTab = 'silver'"
          >
            은 (Silver)
          </button>
        </div>
  
        <h3 class="chart-title">📊 
          <span v-if="activeTab === 'both-usd'">금/은 시세 추이 </span>
          <span v-else-if="activeTab === 'gold'">금 시세 추이 </span>
          <span v-else>은 시세 추이 </span>
        </h3>


        
        <div class="chart-wrapper">
          <canvas v-show="activeTab === 'both-usd'" id="bothUsdChart" ref="bothUsdChart"></canvas>
          <canvas v-show="activeTab === 'gold'" id="goldChart" ref="goldChart"></canvas>
          <canvas v-show="activeTab === 'silver'" id="silverChart" ref="silverChart"></canvas>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { onMounted, ref, computed, watch } from 'vue'
  import axios from 'axios'
  import Chart from 'chart.js/auto'
  
  const goldPrice = ref({bid: 0, ask: 0})
  const silverPrice = ref({bid: 0, ask: 0})
  const goldChartData = ref([])
  const silverChartData = ref([])
  const exchangeRate = ref(1395)
  const activeTab = ref('both-usd')
  
  // 날짜 필터 관련
  const selectedPeriod = ref('6M')
  const customStartDate = ref('')
  const customEndDate = ref('')
  const currentStartDate = ref('')
  const currentEndDate = ref('')
  
  // 기간 옵션
  const periodOptions = [
    { label: '1개월', value: '1M' },
    { label: '3개월', value: '3M' },
    { label: '6개월', value: '6M' },
    { label: '1년', value: '1Y' },
    { label: '2년', value: '2Y' },
    { label: '전체', value: 'ALL' }
  ]
  
  const formatNumber = (value) => {
    if (!value || isNaN(value)) return "정보 없음"
    return new Intl.NumberFormat('ko-KR').format(Math.round(value))
  }

  // 오늘 날짜 문자열
  const todayString = computed(() => {
    return new Date().toISOString().split('T')[0]
  })
  
  // 필터링된 데이터 개수
  const filteredDataCount = computed(() => {
    return getFilteredData(goldChartData.value).length
  })
  
  // 차트 참조
  const bothUsdChart = ref(null)
  const goldChart = ref(null)
  const silverChart = ref(null)
  
  // 차트 인스턴스
  const chartInstances = ref({
    'both-usd': null,
    'gold': null,
    'silver': null
  })
  
  // 날짜 포맷팅
  const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleDateString('ko-KR')
  }
  
  
  // 기간별 시작 날짜 계산
  const calculateStartDate = (period) => {
    const today = new Date()
    const startDate = new Date(today)
    
    switch(period) {
      case '1M':
        startDate.setMonth(today.getMonth() - 1)
        break
      case '3M':
        startDate.setMonth(today.getMonth() - 3)
        break
      case '6M':
        startDate.setMonth(today.getMonth() - 6)
        break
      case '1Y':
        startDate.setFullYear(today.getFullYear() - 1)
        break
      case '2Y':
        startDate.setFullYear(today.getFullYear() - 2)
        break
      case 'ALL':
        return null // 전체 데이터
    }
    
    return startDate.toISOString().split('T')[0]
  }
  
  // 기간 선택
  const selectPeriod = (period) => {
    selectedPeriod.value = period
    
    if (period === 'ALL') {
      currentStartDate.value = ''
      currentEndDate.value = ''
    } else {
      currentStartDate.value = calculateStartDate(period)
      currentEndDate.value = todayString.value
    }
    
    updateCharts()
  }
  
  // 커스텀 날짜 필터 적용
  const applyCustomDateFilter = () => {
    if (customStartDate.value && customEndDate.value) {
      selectedPeriod.value = '' // 기간 버튼 비활성화
      currentStartDate.value = customStartDate.value
      currentEndDate.value = customEndDate.value
      updateCharts()
    }
  }
  
  // 날짜 범위로 데이터 필터링
  const getFilteredData = (dataArr) => {
    if (!dataArr || dataArr.length === 0) return []
    
    // 전체 데이터인 경우
    if (!currentStartDate.value && !currentEndDate.value) {
      return dataArr
    }
    
    return dataArr.filter(item => {
      const itemDate = new Date(item.date)
      const start = currentStartDate.value ? new Date(currentStartDate.value) : new Date('1900-01-01')
      const end = currentEndDate.value ? new Date(currentEndDate.value) : new Date()
      
      return itemDate >= start && itemDate <= end
    })
  }
  
  // 차트 데이터 추출 (필터링 적용)
  const extractChartData = (dataArr) => {
    const filteredData = getFilteredData(dataArr)
    
    const labels = filteredData.map(item => {
      const date = new Date(item.date)
      return date.toLocaleDateString('ko-KR', { 
        year: 'numeric',
        month: 'short', 
        day: 'numeric'
      })
    })
  
    const prices = filteredData.map(item => item.internationalPrice || 0)
    const krwPrices = filteredData.map(item => {
      const price = item.internationalPrice || 0
      return price * exchangeRate.value
    })
    
    return { labels, prices, krwPrices }
  }
  
  // 공통 차트 옵션
  const getCommonChartOptions = (yAxisOptions = {}) => ({
    responsive: true,
    maintainAspectRatio: false,
    animation: { 
      duration: 800,
      easing: 'easeInOutQuart'
    },
    plugins: {
      legend: {
        position: 'top',
        labels: { 
          boxWidth: 20, 
          padding: 20, 
          font: { size: 14, weight: '600' }, 
          usePointStyle: true,
          generateLabels: function(chart) {
            const original = Chart.defaults.plugins.legend.labels.generateLabels(chart);
            original.forEach(label => {
              label.pointStyle = 'circle';
            });
            return original;
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        titleColor: '#333',
        bodyColor: '#666',
        borderColor: '#e0e0e0',
        borderWidth: 1,
        cornerRadius: 8,
        titleFont: { weight: 'bold', size: 15 },
        bodyFont: { size: 14 },
        padding: 12,
        displayColors: true,
        boxWidth: 12,
        boxHeight: 12
      }
    },
    scales: {
      x: { 
        grid: { 
          color: 'rgba(0, 0, 0, 0.08)',
          lineWidth: 1
        },
        title: { 
          display: true, 
          text: '날짜', 
          font: { size: 14, weight: 'bold' },
          color: '#555'
        },
        ticks: {
          maxTicksLimit: 10,
          font: { size: 12 }
        }
      },
      ...yAxisOptions
    },
    elements: { 
      point: { 
        radius: 3, 
        hoverRadius: 6,
        borderWidth: 2,
        hoverBorderWidth: 3
      },
      line: {
        borderWidth: 3,
        tension: 0.4
      }
    },
    interaction: { 
      mode: 'nearest', 
      intersect: false,
      includeInvisible: false
    }
  })
  
  // USD 금/은 함께 차트
  const createBothUsdChart = (gold, silver) => {
    if (chartInstances.value['both-usd']) {
      chartInstances.value['both-usd'].destroy();
    }
    
    if (!bothUsdChart.value) return;
    
    const ctx = bothUsdChart.value.getContext('2d');
    chartInstances.value['both-usd'] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: gold.labels,
        datasets: [
          {
            label: '금 (Gold)',
            data: gold.prices,
            borderColor: '#FFD700',
            backgroundColor: 'rgba(255, 215, 0, 0.15)',
            pointBackgroundColor: '#FFD700',
            pointBorderColor: '#FFB000',
            fill: true,
            yAxisID: 'y-gold'
          },
          {
            label: '은 (Silver)',
            data: silver.prices,
            borderColor: '#C0C0C0',
            backgroundColor: 'rgba(192, 192, 192, 0.15)',
            pointBackgroundColor: '#C0C0C0',
            pointBorderColor: '#A0A0A0',
            fill: true,
            yAxisID: 'y-silver'
          }
        ]
      },
      options: {
        ...getCommonChartOptions({
          'y-gold': { 
            position: 'left',
            grid: { color: 'rgba(0, 0, 0, 0.08)' },
            title: { display: true, text: '금 (USD)', font: { size: 14, weight: 'bold' }, color: '#B8860B' },
            ticks: { color: '#B8860B', font: { size: 12 } }
          },
          'y-silver': {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: '은 (USD)', font: { size: 14, weight: 'bold' }, color: '#808080' },
            ticks: { color: '#808080', font: { size: 12 } }
          }
        }),
        plugins: {
          ...getCommonChartOptions().plugins,
          tooltip: {
            ...getCommonChartOptions().plugins.tooltip,
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: $${context.raw.toFixed(2)}`;
              }
            }
          }
        }
      }
    })
  }

  
  // 금 전용 차트
  const createGoldChart = (gold) => {
    if (chartInstances.value.gold) {
      chartInstances.value.gold.destroy();
    }
    
    if (!goldChart.value) return;
    
    const ctx = goldChart.value.getContext('2d');
    chartInstances.value.gold = new Chart(ctx, {
      type: 'line',
      data: {
        labels: gold.labels,
        datasets: [
          {
            label: '금 (Gold)',
            data: gold.prices,
            borderColor: '#FFD700',
            backgroundColor: 'rgba(255, 215, 0, 0.2)',
            pointBackgroundColor: '#FFD700',
            pointBorderColor: '#FFB000',
            fill: true
          }
        ]
      },
      options: {
        ...getCommonChartOptions({
          y: { 
            grid: { color: 'rgba(0, 0, 0, 0.08)' },
            title: { display: true, text: '금 (USD)', font: { size: 14, weight: 'bold' }, color: '#B8860B' },
            ticks: { color: '#B8860B', font: { size: 12 } }
          }
        }),
        plugins: {
          ...getCommonChartOptions().plugins,
          tooltip: {
            ...getCommonChartOptions().plugins.tooltip,
            callbacks: {
              label: function(context) {
                return `금: $${context.raw.toFixed(2)}`;
              }
            }
          }
        }
      }
    })
  }
  
  // 은 전용 차트
  const createSilverChart = (silver) => {
    if (chartInstances.value.silver) {
      chartInstances.value.silver.destroy();
    }
    
    if (!silverChart.value) return;
    
    const ctx = silverChart.value.getContext('2d');
    chartInstances.value.silver = new Chart(ctx, {
      type: 'line',
      data: {
        labels: silver.labels,
        datasets: [
          {
            label: '은 (Silver)',
            data: silver.prices,
            borderColor: '#C0C0C0',
            backgroundColor: 'rgba(192, 192, 192, 0.2)',
            pointBackgroundColor: '#C0C0C0',
            pointBorderColor: '#A0A0A0',
            fill: true
          }
        ]
      },
      options: {
        ...getCommonChartOptions({
          y: { 
            grid: { color: 'rgba(0, 0, 0, 0.08)' },
            title: { display: true, text: '은 (USD)', font: { size: 14, weight: 'bold' }, color: '#808080' },
            ticks: { color: '#808080', font: { size: 12 } }
          }
        }),
        plugins: {
          ...getCommonChartOptions().plugins,
          tooltip: {
            ...getCommonChartOptions().plugins.tooltip,
            callbacks: {
              label: function(context) {
                return `은: $${context.raw.toFixed(2)}`;
              }
            }
          }
        }
      }
    })
  }
  
  // 차트 업데이트
const updateCharts = () => {
  const gold = extractChartData(goldChartData.value)
  const silver = extractChartData(silverChartData.value)

  if (activeTab.value === 'both-usd') {
    createBothUsdChart(gold, silver)
  } else if (activeTab.value === 'gold') {
    createGoldChart(gold)
  } else if (activeTab.value === 'silver') {
    createSilverChart(silver)
  }
}
  
  // 탭 변경시 차트 업데이트
  watch(activeTab, () => {
    setTimeout(updateCharts, 100)
  })
  
  // 데이터 로드
  onMounted(async () => {
    try {
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/market/summary/`)
      
      if (res.data.gold_price) {
        goldPrice.value = {
          internationalPrice: res.data.gold_price.international,
          domesticPrice: res.data.gold_price.domestic
        }
      }
      if (res.data.silver_price) {
        silverPrice.value = {
          internationalPrice: res.data.silver_price.international,
          domesticPrice: res.data.silver_price.domestic
        }
      }

      if (res.data.gold_chart) {
        goldChartData.value = res.data.gold_chart;
      }
      
      if (res.data.silver_chart) {
        silverChartData.value = res.data.silver_chart;
      }
      
      if (res.data.rates && res.data.rates.USD && res.data.rates.USD.today) {
        exchangeRate.value = res.data.rates.USD.today;
      }
  
      // 기본 6개월 기간으로 설정
      selectPeriod('6M')
  
    } catch (error) {
      console.error('금/은 시세 데이터를 불러오는 중 오류가 발생했습니다:', error);
    }
  })
  </script>
  
  <style scoped>
  .metal-section {
    background: linear-gradient(135deg, #fff 0%, #f8fffe 100%);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 50px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    border: 1px solid #f0f0f0;
    width: 100%;
  }
  
  .section-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 28px;
    color: #222;
    text-align: center;
  }
  
  .price-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
  }
  
  .metal-card {
    display: flex;
    align-items: center;
    gap: 20px;
    background: linear-gradient(145deg, #ffffff 0%, #f9f9f9 100%);
    border-radius: 20px;
    padding: 28px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid #f0f0f0;
    position: relative;
    overflow: hidden;
  }
  
  .metal-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #FFD700, #FFA500);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .metal-card.silver::before {
    background: linear-gradient(90deg, #C0C0C0, #A8A8A8);
  }
  
  .metal-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
  }
  
  .metal-card:hover::before {
    opacity: 1;
  }
  
  .metal-icon {
    font-size: 42px;
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border-radius: 50%;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  }
  
  .metal-card:hover .metal-icon {
    transform: rotate(10deg) scale(1.1);
  }
  
  .metal-info {
    flex: 1;
  }
  
  .metal-name {
    font-size: 20px;
    font-weight: 700;
    color: #333;
    margin-bottom: 12px;
  }
  
  .price-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 15px;
    padding: 4px 0;
  }
  
  .price-label {
    color: #666;
    font-weight: 500;
  }
  
  .price-value {
    font-weight: 700;
    color: #222;
  }
  
  .chart-container {
    background: linear-gradient(145deg, #ffffff 0%, #f9f9f9 100%);
    border-radius: 20px;
    padding: 28px;
    border: 1px solid #f0f0f0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  }
  
  .date-filter-section {
    margin-bottom: 24px;
    padding: 20px;
    background: linear-gradient(145deg, #f8f9fa, #ffffff);
    border-radius: 16px;
    border: 1px solid #e9ecef;
  }
  
  .period-buttons {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .period-btn {
    padding: 10px 18px;
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    border: 2px solid #e9ecef;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    color: #555;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
  }
  
  .period-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
    transition: left 0.5s;
  }
  
  .period-btn:hover::before {
    left: 100%;
  }
  
  .period-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    border-color: #4DD0B1;
  }
  
  .period-btn.active {
    background: linear-gradient(145deg, #4DD0B1, #45c7a8);
    color: white;
    border-color: #4DD0B1;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(77, 208, 177, 0.4);
  }
  
  .custom-date-filter {
    border-top: 1px solid #e9ecef;
    padding-top: 16px;
  }
  
  .date-inputs {
    display: flex;
    gap: 16px;
    align-items: end;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .date-input-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  
  .date-input-group label {
    font-size: 13px;
    font-weight: 600;
    color: #555;
  }
  
  .date-input-group input {
    padding: 10px 14px;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    font-size: 14px;
    transition: all 0.3s ease;
    background: white;
    min-width: 140px;
  }
  
  .date-input-group input:focus {
    outline: none;
    border-color: #4DD0B1;
    box-shadow: 0 0 0 3px rgba(77, 208, 177, 0.1);
  }
  
  .apply-btn {
    padding: 10px 20px;
    background: linear-gradient(145deg, #4DD0B1, #45c7a8);
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    min-height: 42px;
  }
  
  .apply-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(77, 208, 177, 0.3);
  }
  
  .chart-info {
    text-align: center;
    margin-bottom: 20px;
    padding: 12px 20px;
    background: linear-gradient(145deg, #f8f9fa, #ffffff);
    border-radius: 12px;
    border: 1px solid #e9ecef;
  }
  
  .data-period {
    font-size: 14px;
    color: #666;
    font-weight: 500;
    margin: 0;
  }
  
  .chart-tabs {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;
  }
  
  .tab-button {
    padding: 12px 20px;
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
    border: 2px solid #e9ecef;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    color: #555;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
  }
  
  .tab-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
    transition: left 0.5s;
  }
  
  .tab-button:hover::before {
    left: 100%;
  }
  
  .tab-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    border-color: #4DD0B1;
  }
  
  .tab-button.active {
    background: linear-gradient(145deg, #4DD0B1, #45c7a8);
    color: white;
    border-color: #4DD0B1;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(77, 208, 177, 0.4);
  }
  
  .chart-title {
    font-size: 20px;
    font-weight: 700;
    color: #333;
    margin-bottom: 24px;
    text-align: center;
  }
  
  .chart-wrapper {
    height: 450px;
    position: relative;
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
  }
  
  canvas {
    width: 100% !important;
    height: 100% !important;
    position: absolute;
    top: 20px;
    left: 20px;
    right: 20px;
    bottom: 20px;
  }
  
  @media (max-width: 768px) {
    .metal-section {
      padding: 20px;
    }
    
    .price-container {
      grid-template-columns: 1fr;
      gap: 16px;
    }
    
    .metal-card {
      padding: 20px;
    }
    
    .chart-wrapper {
      height: 350px;
      padding: 15px;
    }
    
    .chart-tabs, .period-buttons {
      flex-wrap: wrap;
      gap: 8px;
    }
    
    .tab-button, .period-btn {
      flex: 1;
      min-width: 80px;
      text-align: center;
      padding: 10px 12px;
      font-size: 13px;
    }
    
    .date-inputs {
      flex-direction: column;
      align-items: center;
    }
    
    .date-input-group {
      width: 100%;
      max-width: 200px;
    }
    
    .date-input-group input {
      width: 100%;
    }
    
    .apply-btn {
      width: 100%;
      max-width: 200px;
    }
    
    .section-title {
      font-size: 20px;
    }
    
    .chart-title {
      font-size: 18px;
    }
    
    canvas {
      top: 15px;
      left: 15px;
      right: 15px;
      bottom: 15px;
    }
  }
  
  @media (max-width: 480px) {
    .metal-card {
      flex-direction: column;
      text-align: center;
      gap: 16px;
    }
    
    .metal-icon {
      width: 60px;
      height: 60px;
      font-size: 32px;
    }
    
    .chart-wrapper {
      height: 300px;
      padding: 10px;
    }
    
    canvas {
      top: 10px;
      left: 10px;
      right: 10px;
      bottom: 10px;
    }
    
    .date-filter-section {
      padding: 16px;
    }
    
    .chart-container {
      padding: 20px;
    }
  }
  </style>