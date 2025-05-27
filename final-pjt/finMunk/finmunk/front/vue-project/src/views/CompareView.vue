<template>
  <div class="compare-container">
    <!-- 헤더 섹션 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">💰</div>
        <div class="header-text">
          <h1 class="page-title">예적금 상품 비교</h1>
          <p class="page-subtitle">다양한 금융상품을 한눈에 비교해보세요</p>
        </div>
      </div>
      <div class="header-decoration"></div>
    </div>

    <!-- 상품 타입 탭 -->
    <div class="product-type-tabs">
      <button 
        @click="activeTab = 'all'" 
        :class="{ active: activeTab === 'all' }" 
        class="tab-btn"
      >
        <i class="fas fa-chart-bar"></i>
        <span>전체</span>
        <span class="count">{{ products.length }}</span>
      </button>
      <button 
        @click="activeTab = 'deposit'" 
        :class="{ active: activeTab === 'deposit' }" 
        class="tab-btn"
      >
        <i class="fas fa-university"></i>
        <span>예금</span>
        <span class="count">{{ depositProducts.length }}</span>
      </button>
      <button 
        @click="activeTab = 'saving'" 
        :class="{ active: activeTab === 'saving' }" 
        class="tab-btn"
      >
        <i class="fas fa-piggy-bank"></i>
        <span>적금</span>
        <span class="count">{{ savingProducts.length }}</span>
      </button>
    </div>

    <!-- 필터 컴포넌트 -->
    <div class="filter-section">
      <ProductFilter
        v-model:filters="filters"
        :uniqueBanks="uniqueBanks"
        @apply="applyFilter"
      />
    </div>

    <!-- 필터 요약 -->
    <div v-if="hasActiveFilters" class="filter-summary">
      <div class="summary-content">
        <i class="fas fa-filter"></i>
        <span>활성 필터: {{ getFilterSummary() }}</span>
      </div>
      <button @click="clearFilters" class="clear-btn">
        <i class="fas fa-times"></i>
        필터 초기화
      </button>
    </div>

    <!-- 상품 통계 -->
    <div class="product-stats">
      <div class="stats-card">
        <div class="stats-icon">
          <i class="fas fa-chart-pie"></i>
        </div>
        <div class="stats-content">
          <h3>{{ getTabLabel() }}</h3>
          <p>{{ processedProducts.length }}개 상품</p>
        </div>
      </div>
    </div>

    <!-- 상품 목록 -->
    <div class="product-list">
      <ProductCard
        v-for="(item, index) in processedProducts"
        :key="`product-${activeTab}-${index}-${item.id || item.product_name}`"
        :item="item"
        :selected="selectedProduct === item.id"
        @toggle="toggleDetail"
      />
    </div>

    <!-- 결과 없음 -->
    <div v-if="processedProducts.length === 0 && currentTabProducts.length > 0" class="no-results">
      <div class="no-results-icon">😅</div>
      <h3>조건에 맞는 상품이 없습니다</h3>
      <p>다른 조건으로 다시 검색해보세요</p>
      <button @click="clearFilters" class="action-btn">
        <i class="fas fa-refresh"></i>
        필터 초기화
      </button>
    </div>

    <!-- 상품 없음 -->
    <div v-if="currentTabProducts.length === 0 && products.length > 0" class="no-products">
      <div class="no-products-icon">📭</div>
      <h3>{{ getTabLabel() }} 상품이 없습니다</h3>
      <p>다른 상품 유형을 선택해보세요</p>
    </div>

    <!-- 맨 위로 가기 버튼 -->
    <button 
      v-if="showScrollTop"
      @click="scrollToTop"
      class="scroll-top-btn"
    >
      <i class="fas fa-arrow-up"></i>
    </button>
  </div>
  <Chatbot/>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import axios from 'axios'

import ProductFilter from '@/components/products/ProductFilter.vue'
import ProductCard from '@/components/products/ProductCard.vue'
import Chatbot from '@/components/chatbot/Chatbot.vue'

const products = ref([])
const activeTab = ref('all')
const filters = ref({ bank: '', rate: null, term: '', limit: '' })
const selectedProduct = ref(null)
const showScrollTop = ref(false)

function toggleDetail(item) {
selectedProduct.value = selectedProduct.value === item.id ? null : item.id
}

const depositProducts = computed(() =>
products.value.filter(p =>
  p.product_type === 'deposit' || p.product_name?.includes('예금') || p.category === 'deposit'
)
)

const savingProducts = computed(() =>
products.value.filter(p =>
  p.product_type === 'saving' || p.product_name?.includes('적금') || p.category === 'saving'
)
)

const currentTabProducts = computed(() => {
if (activeTab.value === 'deposit') return depositProducts.value
if (activeTab.value === 'saving') return savingProducts.value
return products.value
})

const uniqueBanks = computed(() =>
[...new Set(currentTabProducts.value.map(p => p.bank_name))].sort()
)

const hasActiveFilters = computed(() => {
return filters.value.bank || filters.value.rate !== null || filters.value.term || filters.value.limit
})

const filteredProducts = computed(() => {
return currentTabProducts.value.filter(product => {
  if (filters.value.bank && product.bank_name !== filters.value.bank) return false

  if (filters.value.rate !== null && filters.value.rate > 0) {
    const rate = product.interest_rate2 || product.interest_rate || 0
    if (rate < filters.value.rate) return false
  }

  if (filters.value.term) {
    const term = parseInt(filters.value.term)
    if (parseInt(product.save_term) !== term) return false
  }

  if (filters.value.limit === '있음') {
    if (!product.max_limit || product.max_limit === '' || product.max_limit === '한도없음') return false
  } else if (filters.value.limit === '없음') {
    if (product.max_limit && product.max_limit !== '' && product.max_limit !== '한도없음') return false
  }

  return true
})
})

function getJoinRestrictionText(code) {
switch (String(code)) {
  case '1': return '가입 제한 없음'
  case '3': return '청년 가입가능 (만 19세~34세)'
  default: return '정보 없음'
}
}

const processedProducts = computed(() => {
return filteredProducts.value.map(product => ({
  ...product,
  join_restriction_text: getJoinRestrictionText(product.join_restriction || product.join_deny)
}))
})

function applyFilter() {
console.log('🔍 필터 적용:', filters.value)
}

function clearFilters() {
filters.value = { bank: '', rate: null, term: '', limit: '' }
}

function getFilterSummary() {
const active = []
if (filters.value.bank) active.push(`은행: ${filters.value.bank}`)
if (filters.value.rate) active.push(`금리: ${filters.value.rate}% 이상`)
if (filters.value.term) active.push(`기간: ${filters.value.term}개월`)
if (filters.value.limit) active.push(`한도: ${filters.value.limit}`)
return active.join(', ')
}

function getTabLabel() {
return activeTab.value === 'deposit' ? '예금' : activeTab.value === 'saving' ? '적금' : '전체'
}

function scrollToTop() {
window.scrollTo({
  top: 0,
  behavior: 'smooth'
})
}

function handleScroll() {
showScrollTop.value = window.scrollY > 300
}

watch(activeTab, () => {
selectedProduct.value = null
})

watch(filters, () => {
console.log('필터 변경됨:', filters.value)
}, { deep: true })

onMounted(() => {
axios.get(`${import.meta.env.VITE_API_URL}/products/all-products/`, {
  headers: {
    Authorization: `Token ${localStorage.getItem('token')}`
  }
})
.then(res => {
  products.value = res.data
})
.catch(err => {
  console.error('❌ 데이터 로딩 실패:', err)
})

window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.compare-container {
max-width: 1200px;
margin: 0 auto;
padding: 20px;
min-height: 100vh;
background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
}

/* 헤더 섹션 */
.page-header {
text-align: center;
margin-bottom: 48px;
position: relative;
padding: 40px 0;
animation: fadeInDown 0.8s ease-out;
}

.header-content {
display: flex;
align-items: center;
justify-content: center;
gap: 20px;
margin-bottom: 20px;
}

.header-icon {
font-size: 48px;
animation: bounce 2s infinite;
}

@keyframes bounce {
0%, 20%, 50%, 80%, 100% {
  transform: translateY(0);
}
40% {
  transform: translateY(-10px);
}
60% {
  transform: translateY(-5px);
}
}

.header-text {
text-align: left;
}

.page-title {
font-size: 36px;
font-weight: 800;
background: linear-gradient(135deg, #1e40af 0%, #10b981 50%, #059669 100%);
background-clip: text;
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
margin: 0 0 8px 0;
letter-spacing: -0.025em;
}

.page-subtitle {
font-size: 16px;
color: #6b7280;
margin: 0;
font-weight: 500;
}

.header-decoration {
width: 100px;
height: 4px;
background: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
margin: 0 auto;
border-radius: 2px;
animation: scaleIn 1s ease-out 0.5s both;
}

@keyframes fadeInDown {
from {
  opacity: 0;
  transform: translateY(-30px);
}
to {
  opacity: 1;
  transform: translateY(0);
}
}

@keyframes scaleIn {
from {
  transform: scaleX(0);
}
to {
  transform: scaleX(1);
}
}

/* 상품 타입 탭 */
.product-type-tabs {
display: flex;
gap: 16px;
margin-bottom: 32px;
padding: 0 4px;
}

.tab-btn {
flex: 1;
padding: 16px 24px;
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border: 2px solid rgba(59, 130, 246, 0.1);
border-radius: 16px;
color: #6b7280;
font-weight: 600;
font-size: 16px;
cursor: pointer;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
gap: 8px;
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
backdrop-filter: blur(10px);
}

.tab-btn:hover {
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
border-color: rgba(59, 130, 246, 0.3);
}

.tab-btn.active {
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
color: white;
border-color: #3b82f6;
box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.tab-btn i {
font-size: 18px;
}

.count {
background: rgba(255, 255, 255, 0.2);
padding: 2px 8px;
border-radius: 12px;
font-size: 12px;
font-weight: 700;
}

.tab-btn.active .count {
background: rgba(255, 255, 255, 0.3);
}

/* 필터 섹션 */
.filter-section {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 20px;
padding: 24px;
margin-bottom: 24px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
border: 1px solid rgba(255, 255, 255, 0.2);
backdrop-filter: blur(10px);
}

/* 필터 요약 */
.filter-summary {
background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
padding: 16px 20px;
border-radius: 12px;
margin-bottom: 24px;
display: flex;
justify-content: space-between;
align-items: center;
border: 1px solid rgba(59, 130, 246, 0.1);
animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
from {
  opacity: 0;
  transform: translateY(-10px);
}
to {
  opacity: 1;
  transform: translateY(0);
}
}

.summary-content {
display: flex;
align-items: center;
gap: 8px;
color: #1f2937;
font-weight: 500;
}

.summary-content i {
color: #3b82f6;
}

.clear-btn {
background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
color: white;
border: none;
padding: 8px 16px;
border-radius: 8px;
cursor: pointer;
font-size: 14px;
font-weight: 600;
display: flex;
align-items: center;
gap: 6px;
transition: all 0.3s ease;
box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.clear-btn:hover {
transform: translateY(-1px);
box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

/* 상품 통계 */
.product-stats {
margin-bottom: 32px;
}

.stats-card {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 16px;
padding: 20px;
display: flex;
align-items: center;
gap: 16px;
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
border: 1px solid rgba(255, 255, 255, 0.2);
backdrop-filter: blur(10px);
transition: all 0.3s ease;
}

.stats-card:hover {
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stats-icon {
width: 48px;
height: 48px;
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
border-radius: 12px;
display: flex;
align-items: center;
justify-content: center;
font-size: 20px;
color: white;
box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.stats-content h3 {
font-size: 18px;
font-weight: 700;
color: #1f2937;
margin: 0 0 4px 0;
}

.stats-content p {
font-size: 14px;
color: #6b7280;
margin: 0;
font-weight: 500;
}

/* 상품 목록 */
.product-list {
display: grid;
grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
gap: 24px;
margin-bottom: 48px;
}

/* 결과 없음 / 상품 없음 */
.no-results, .no-products {
text-align: center;
padding: 80px 20px;
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 20px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
border: 1px solid rgba(255, 255, 255, 0.2);
backdrop-filter: blur(10px);
animation: fadeIn 0.6s ease-out;
}

.no-results-icon, .no-products-icon {
font-size: 64px;
margin-bottom: 20px;
}

.no-results h3, .no-products h3 {
font-size: 24px;
font-weight: 700;
color: #374151;
margin: 0 0 8px 0;
}

.no-results p, .no-products p {
font-size: 16px;
color: #6b7280;
margin: 0 0 24px 0;
}

.action-btn {
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
color: white;
border: none;
padding: 12px 24px;
border-radius: 12px;
font-size: 16px;
font-weight: 600;
cursor: pointer;
transition: all 0.3s ease;
display: inline-flex;
align-items: center;
gap: 8px;
box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.action-btn:hover {
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

/* 맨 위로 가기 버튼 */
.scroll-top-btn {
position: fixed;
bottom: 30px;
right: 30px;
width: 56px;
height: 56px;
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
color: white;
border: none;
border-radius: 50%;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
font-size: 20px;
box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
transition: all 0.3s ease;
z-index: 100;
animation: fadeInUp 0.3s ease-out;
}

.scroll-top-btn:hover {
transform: translateY(-4px) scale(1.1);
box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
}

@keyframes fadeIn {
from {
  opacity: 0;
}
to {
  opacity: 1;
}
}

@keyframes fadeInUp {
from {
  opacity: 0;
  transform: translateY(30px);
}
to {
  opacity: 1;
  transform: translateY(0);
}
}

/* 반응형 디자인 */
@media (max-width: 768px) {
.compare-container {
  padding: 16px;
}

.page-header {
  padding: 20px 0;
  margin-bottom: 32px;
}

.header-content {
  flex-direction: column;
  gap: 16px;
}

.header-text {
  text-align: center;
}

.page-title {
  font-size: 28px;
}

.product-type-tabs {
  flex-direction: column;
  gap: 12px;
}

.tab-btn {
  padding: 12px 16px;
  font-size: 14px;
}

.filter-section {
  padding: 20px;
}

.filter-summary {
  flex-direction: column;
  gap: 12px;
  align-items: stretch;
}

.product-list {
  grid-template-columns: 1fr;
  gap: 16px;
}

.scroll-top-btn {
  bottom: 20px;
  right: 20px;
  width: 48px;
  height: 48px;
  font-size: 18px;
}
}

@media (max-width: 480px) {
.stats-card {
  padding: 16px;
}

.stats-icon {
  width: 40px;
  height: 40px;
  font-size: 18px;
}

.no-results, .no-products {
  padding: 60px 20px;
}
}
</style>