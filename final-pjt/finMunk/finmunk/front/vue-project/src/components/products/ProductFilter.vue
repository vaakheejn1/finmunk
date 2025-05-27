<template>
  <div class="filter-container">
    <div class="filter-header">
      <div class="filter-icon">
        <i class="fas fa-sliders-h"></i>
      </div>
      <div class="filter-title">
        <h3>상품 필터</h3>
        <p>원하는 조건으로 상품을 찾아보세요</p>
      </div>
    </div>

    <div class="filter-grid">
      <!-- 은행 선택 -->
      <div class="filter-group">
        <label class="filter-label">
          <i class="fas fa-university"></i>
          은행 선택
        </label>
        <div class="input-wrapper">
          <select v-model="localFilters.bank" @change="emitUpdate" class="filter-select">
            <option value="">전체 은행</option>
            <option v-for="bank in uniqueBanks" :key="bank" :value="bank">
              {{ bank }}
            </option>
          </select>
          <i class="fas fa-chevron-down select-arrow"></i>
        </div>
      </div>

      <!-- 최소 금리 -->
      <div class="filter-group">
        <label class="filter-label">
          <i class="fas fa-percentage"></i>
          최소 금리
        </label>
        <div class="input-wrapper">
          <input 
            type="number" 
            v-model.number="localFilters.rate" 
            @input="emitUpdate"
            placeholder="예: 2.5" 
            step="0.1"
            min="0"
            max="10"
            class="filter-input"
          />
          <span class="input-suffix">% 이상</span>
        </div>
      </div>

      <!-- 저축기간 -->
      <div class="filter-group">
        <label class="filter-label">
          <i class="fas fa-clock"></i>
          저축기간
        </label>
        <div class="input-wrapper">
          <select v-model="localFilters.term" @change="emitUpdate" class="filter-select">
            <option value="">전체 기간</option>
            <option v-for="term in availableTerms" :key="term" :value="term">
              {{ term }}개월
            </option>
          </select>
          <i class="fas fa-chevron-down select-arrow"></i>
        </div>
      </div>

      <!-- 가입한도 -->
      <div class="filter-group">
        <label class="filter-label">
          <i class="fas fa-coins"></i>
          가입한도
        </label>
        <div class="input-wrapper">
          <select v-model="localFilters.limit" @change="emitUpdate" class="filter-select">
            <option value="">전체</option>
            <option value="있음">한도 있음</option>
            <option value="없음">한도 없음</option>
          </select>
          <i class="fas fa-chevron-down select-arrow"></i>
        </div>
      </div>
    </div>

    <!-- 필터 액션 버튼 -->
    <div class="filter-actions">
      <button @click="applyFilters" class="action-btn primary">
        <i class="fas fa-search"></i>
        필터 적용
      </button>
      <button @click="resetFilters" class="action-btn secondary">
        <i class="fas fa-undo"></i>
        초기화
      </button>
    </div>

    <!-- 활성 필터 표시 -->
    <div v-if="hasActiveFilters" class="active-filters">
      <div class="active-filters-header">
        <i class="fas fa-filter"></i>
        <span>활성 필터</span>
      </div>
      <div class="filter-tags">
        <div v-if="localFilters.bank" class="filter-tag" @click="clearFilter('bank')">
          <span>은행: {{ localFilters.bank }}</span>
          <i class="fas fa-times"></i>
        </div>
        <div v-if="localFilters.rate" class="filter-tag" @click="clearFilter('rate')">
          <span>금리: {{ localFilters.rate }}% 이상</span>
          <i class="fas fa-times"></i>
        </div>
        <div v-if="localFilters.term" class="filter-tag" @click="clearFilter('term')">
          <span>기간: {{ localFilters.term }}개월</span>
          <i class="fas fa-times"></i>
        </div>
        <div v-if="localFilters.limit" class="filter-tag" @click="clearFilter('limit')">
          <span>한도: {{ localFilters.limit }}</span>
          <i class="fas fa-times"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
filters: {
  type: Object,
  required: true
},
uniqueBanks: {
  type: Array,
  default: () => []
}
})

const emit = defineEmits(['apply', 'update:filters'])

// 로컬 필터 상태
const localFilters = ref({ ...props.filters })

// 사용 가능한 저축기간 옵션
const availableTerms = computed(() => {
return [1, 3, 6, 12, 18, 24, 36].sort((a, b) => a - b)
})

// 활성 필터가 있는지 확인
const hasActiveFilters = computed(() => {
return localFilters.value.bank || 
       localFilters.value.rate || 
       localFilters.value.term || 
       localFilters.value.limit
})

// 부모 컴포넌트의 filters가 변경되면 로컬 상태도 업데이트
watch(() => props.filters, (newFilters) => {
localFilters.value = { ...newFilters }
}, { deep: true })

// 로컬 필터가 변경될 때 부모에게 전달
function emitUpdate() {
emit('update:filters', { ...localFilters.value })
}

function applyFilters() {
emitUpdate()
emit('apply')
console.log('🔍 필터 적용됨:', localFilters.value)
}

function resetFilters() {
localFilters.value = {
  bank: '',
  rate: null,
  term: '',
  limit: ''
}
emitUpdate()
emit('apply')
console.log('🧹 필터 초기화됨')
}

function clearFilter(filterType) {
localFilters.value[filterType] = filterType === 'rate' ? null : ''
emitUpdate()
emit('apply')
}
</script>

<style scoped>
.filter-container {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 20px;
padding: 24px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
border: 1px solid rgba(255, 255, 255, 0.2);
backdrop-filter: blur(10px);
transition: all 0.3s ease;
animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
from {
  opacity: 0;
  transform: translateY(20px);
}
to {
  opacity: 1;
  transform: translateY(0);
}
}

.filter-container:hover {
transform: translateY(-2px);
box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

/* 필터 헤더 */
.filter-header {
display: flex;
align-items: center;
gap: 16px;
margin-bottom: 24px;
padding-bottom: 16px;
border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.filter-icon {
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

.filter-title h3 {
font-size: 18px;
font-weight: 700;
color: #1f2937;
margin: 0 0 4px 0;
}

.filter-title p {
font-size: 14px;
color: #6b7280;
margin: 0;
}

/* 필터 그리드 */
.filter-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
gap: 20px;
margin-bottom: 24px;
}

.filter-group {
display: flex;
flex-direction: column;
gap: 8px;
}

.filter-label {
display: flex;
align-items: center;
gap: 8px;
font-size: 14px;
font-weight: 600;
color: #374151;
margin-bottom: 4px;
}

.filter-label i {
color: #3b82f6;
width: 16px;
}

/* 입력 요소 스타일 */
.input-wrapper {
position: relative;
display: flex;
align-items: center;
}

.filter-select,
.filter-input {
width: 100%;
padding: 12px 16px;
border: 2px solid rgba(59, 130, 246, 0.1);
border-radius: 12px;
font-size: 14px;
font-weight: 500;
color: #374151;
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
transition: all 0.3s ease;
appearance: none;
}

.filter-select:focus,
.filter-input:focus {
outline: none;
border-color: #3b82f6;
box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
transform: translateY(-1px);
}

.filter-select:hover,
.filter-input:hover {
border-color: rgba(59, 130, 246, 0.3);
}

/* 셀렉트 화살표 */
.select-arrow {
position: absolute;
right: 12px;
color: #6b7280;
pointer-events: none;
font-size: 12px;
}

/* 입력 접미사 */
.input-suffix {
position: absolute;
right: 12px;
font-size: 12px;
color: #6b7280;
font-weight: 500;
pointer-events: none;
}

.filter-input:focus + .input-suffix {
color: #3b82f6;
}

/* 액션 버튼 */
.filter-actions {
display: flex;
gap: 12px;
justify-content: center;
margin-bottom: 20px;
}

.action-btn {
flex: 1;
max-width: 150px;
padding: 12px 20px;
border-radius: 12px;
font-size: 14px;
font-weight: 600;
cursor: pointer;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
gap: 8px;
border: none;
}

.action-btn.primary {
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
color: white;
box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.action-btn.primary:hover {
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

.action-btn.secondary {
background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
color: #374151;
border: 1px solid rgba(0, 0, 0, 0.1);
}

.action-btn.secondary:hover {
background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
transform: translateY(-1px);
}

/* 활성 필터 표시 */
.active-filters {
background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
border-radius: 12px;
padding: 16px;
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

.active-filters-header {
display: flex;
align-items: center;
gap: 8px;
margin-bottom: 12px;
font-size: 14px;
font-weight: 600;
color: #1f2937;
}

.active-filters-header i {
color: #3b82f6;
}

.filter-tags {
display: flex;
flex-wrap: wrap;
gap: 8px;
}

.filter-tag {
display: flex;
align-items: center;
gap: 6px;
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border: 1px solid rgba(59, 130, 246, 0.2);
border-radius: 20px;
padding: 6px 12px;
font-size: 12px;
font-weight: 500;
color: #374151;
cursor: pointer;
transition: all 0.2s ease;
}

.filter-tag:hover {
background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
border-color: #ef4444;
color: #dc2626;
}

.filter-tag i {
font-size: 10px;
opacity: 0.7;
}

.filter-tag:hover i {
opacity: 1;
color: #dc2626;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
.filter-container {
  padding: 20px;
}

.filter-header {
  flex-direction: column;
  text-align: center;
  gap: 12px;
}

.filter-grid {
  grid-template-columns: 1fr;
  gap: 16px;
}

.filter-actions {
  flex-direction: column;
}

.action-btn {
  max-width: none;
}

.filter-tags {
  justify-content: center;
}
}

@media (max-width: 480px) {
.filter-container {
  padding: 16px;
}

.filter-icon {
  width: 40px;
  height: 40px;
  font-size: 18px;
}

.filter-title h3 {
  font-size: 16px;
}

.filter-title p {
  font-size: 13px;
}

.filter-select,
.filter-input {
  padding: 10px 12px;
  font-size: 13px;
}
}
</style>