<template>
  <div class="product-card">
    <div class="card-header">
      <div class="header-content">
        <h4 class="product-title">{{ item.product_name }}</h4>
        <span class="bank-badge">{{ item.bank_name }}</span>
      </div>
      <div class="card-rank">
        <i class="fas fa-star"></i>
      </div>
    </div>
    
    <div class="card-content">
      <div class="product-info">
        <div class="info-row">
          <div class="info-item">
            <div class="info-icon">
              <i class="fas fa-percentage"></i>
            </div>
            <div class="info-details">
              <span class="label">금리</span>
              <span class="value highlight">{{ displayRate }}%</span>
            </div>
          </div>
          
          <div class="info-item">
            <div class="info-icon">
              <i class="fas fa-clock"></i>
            </div>
            <div class="info-details">
              <span class="label">기간</span>
              <span class="value">{{ item.save_term }}개월</span>
            </div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-item full-width">
            <div class="info-icon">
              <i class="fas fa-coins"></i>
            </div>
            <div class="info-details">
              <span class="label">가입한도</span>
              <span class="value">{{ displayLimit }}</span>
            </div>
          </div>
        </div>
        
        <div class="info-row">
          <div class="info-item full-width">
            <div class="info-icon">
              <i class="fas fa-user-check"></i>
            </div>
            <div class="info-details">
              <span class="label">가입제한</span>
              <span class="value">{{ item.join_restriction_text || '정보 없음' }}</span>
            </div>
          </div>
        </div>
      </div>

      <button @click="openModal" class="detail-btn">
        <i class="fas fa-info-circle"></i>
        상세정보 보기
      </button>
    </div>
  </div>

  <!-- 상세정보 모달 -->
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <div class="modal-title">
          <h3>{{ item.product_name }}</h3>
          <span class="modal-bank">{{ item.bank_name }}</span>
        </div>
        <button class="close-btn" @click="closeModal">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="modal-body">
        <!-- 핵심 정보 카드 -->
        <div class="highlight-card">
          <div class="highlight-item">
            <div class="highlight-icon rate">
              <i class="fas fa-percentage"></i>
            </div>
            <div class="highlight-content">
              <span class="highlight-label">최고금리</span>
              <span class="highlight-value">{{ displayRate }}%</span>
            </div>
          </div>
          <div class="highlight-item">
            <div class="highlight-icon term">
              <i class="fas fa-calendar-alt"></i>
            </div>
            <div class="highlight-content">
              <span class="highlight-label">저축기간</span>
              <span class="highlight-value">{{ item.save_term }}개월</span>
            </div>
          </div>
          <div class="highlight-item">
            <div class="highlight-icon limit">
              <i class="fas fa-wallet"></i>
            </div>
            <div class="highlight-content">
              <span class="highlight-label">가입한도</span>
              <span class="highlight-value">{{ displayLimit }}</span>
            </div>
          </div>
        </div>

        <div class="detail-sections">
          <!-- 가입 정보 섹션 -->
          <div class="detail-section">
            <div class="section-header">
              <i class="fas fa-info-circle"></i>
              <h5>가입 정보</h5>
            </div>
            <div class="section-content">
              <div class="detail-item">
                <span class="detail-label">가입 방법</span>
                <span class="detail-value">{{ item.join_way || '영업점, 인터넷뱅킹, 모바일앱' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">가입 제한</span>
                <span class="detail-value">{{ item.join_restriction_text || '제한 없음' }}</span>
              </div>
              <div class="detail-item" v-if="item.maturity_type">
                <span class="detail-label">만기 안내</span>
                <span class="detail-value">{{ item.maturity_type }}</span>
              </div>
            </div>
          </div>
          
          <!-- 금리 정보 섹션 -->
          <div class="detail-section">
            <div class="section-header">
              <i class="fas fa-chart-line"></i>
              <h5>금리 정보</h5>
            </div>
            <div class="section-content">
              <div class="rate-comparison">
                <div class="rate-item">
                  <div class="rate-box basic">
                    <span class="rate-label">기본금리</span>
                    <span class="rate-value">{{ item.interest_rate }}%</span>
                  </div>
                </div>
                <div class="rate-item" v-if="item.interest_rate2">
                  <div class="rate-box premium">
                    <span class="rate-label">최고금리</span>
                    <span class="rate-value">{{ item.interest_rate2 }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 우대 혜택 섹션 -->
          <div class="detail-section">
            <div class="section-header">
              <i class="fas fa-gift"></i>
              <h5>우대 혜택</h5>
            </div>
            <div class="section-content">
              <div class="benefit-list">
                <div class="benefit-item">
                  <i class="fas fa-check-circle"></i>
                  <span>인터넷뱅킹 가입 시 <strong>+0.1%</strong> 우대금리</span>
                </div>
                <div class="benefit-item">
                  <i class="fas fa-check-circle"></i>
                  <span>자동이체 등록 시 <strong>+0.1%</strong> 추가 혜택</span>
                </div>
                <div class="benefit-item">
                  <i class="fas fa-check-circle"></i>
                  <span>급여이체 고객 <strong>+0.1%</strong> 우대</span>
                </div>
                <div class="benefit-item">
                  <i class="fas fa-check-circle"></i>
                  <span>청년 고객 <strong>추가 우대</strong> 가능</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 주의사항 섹션 -->
          <div class="detail-section">
            <div class="section-header">
              <i class="fas fa-exclamation-triangle"></i>
              <h5>주의사항</h5>
            </div>
            <div class="section-content">
              <div class="notice-list">
                <div class="notice-item">
                  <i class="fas fa-dot-circle"></i>
                  <span>금리는 가입시점 기준이며, 시장금리 변동에 따라 조정될 수 있습니다</span>
                </div>
                <div class="notice-item">
                  <i class="fas fa-dot-circle"></i>
                  <span>중도해지 시 기간별 중도해지율이 적용되어 이자가 감소합니다</span>
                </div>
                <div class="notice-item">
                  <i class="fas fa-dot-circle"></i>
                  <span>이자소득세(15.4%)가 별도로 부과됩니다</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 모달 푸터 -->
       <div class="modal-footer">
        <button class="action-btn secondary" @click="openConsultModal">
          <i class="fas fa-headset"></i>
          상담 신청
        </button>

        <button class="action-btn secondary" @click="addToWishlist">
          <i class="fas" :class="isLiked ? 'fa-heart' : 'fa-heart-broken'"></i>
          {{ isLiked ? '찜취소' : '관심상품' }}
        </button>
      </div>
    </div>
  </div>

  <div v-if="showConsultModal" class="modal-overlay" @click.self="showConsultModal = false">
  <div class="modal-content" @click.stop>
    <h3>금융 상품 상담 신청</h3>
    <p><strong>{{ item.product_name }}</strong> 상품 상담을 원하시나요?</p>

    <label>전화번호</label>
    <input v-model="consultPhone" type="tel" placeholder="010-1234-5678" />

    <label>
      <input type="checkbox" v-model="agree" />
      개인정보 제공에 동의합니다.
    </label>

    <div class="modal-actions">
      <button @click="submitConsultRequest" :disabled="!agree || !consultPhone">신청</button>
      <button @click="showConsultModal = false">취소</button>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const props = defineProps({
  item: Object,
  selected: Boolean
})

const showConsultModal = ref(false)
const consultPhone = ref('')
const agree = ref(false)

function openConsultModal() {
  showConsultModal.value = true
  consultPhone.value = ''
  agree.value = false
}

function submitConsultRequest() {
  axios.post(`${import.meta.env.VITE_API_URL}/consultations/`, {
    product_name: props.item.product_name,
    phone: consultPhone.value,
  }, {
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`
    }
  }).then(() => {
    alert('상담 신청이 완료되었습니다! ✅')
    showConsultModal.value = false
  }).catch(() => {
    alert('상담 신청에 실패했어요 😥')
  })
}

const showModal = ref(false)
const isLiked = ref(false) // 찜 상태

// 금리 계산
const displayRate = computed(() => {
  return props.item.interest_rate2 || props.item.interest_rate || 0
})

// 가입한도 표시
const displayLimit = computed(() => {
  const limit = String(props.item.max_limit || '')
  if (limit === '' || limit === '한도없음') return '한도없음'
  if (/^\d+$/.test(limit)) {
    const num = parseInt(limit)
    if (num >= 100000000) return `${(num / 100000000).toFixed(0)}억원`
    if (num >= 10000) return `${(num / 10000).toFixed(0)}만원`
    return `${num}원`
  }
  return limit
})

// 모달 열기
const openModal = () => {
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

// 모달 닫기
const closeModal = () => {
  showModal.value = false
  document.body.style.overflow = 'auto'
}

// 이자 계산 버튼
const calculateInterest = () => {
  alert(`${props.item.product_name} 이자 계산기를 실행합니다.`)
  closeModal()
}

// 상품 비교 버튼
const compareProduct = () => {
  alert(`${props.item.product_name} 상품 비교 기능을 실행합니다.`)
  closeModal()
}

// 찜 기능 버튼 (axios)
const addToWishlist = () => {
  const isSaving = props.item.product_name.includes('적금')
  const endpoint = isSaving
    ? `${import.meta.env.VITE_API_URL}/products/toggle-saving-like/${props.item.id}/`
    : `${import.meta.env.VITE_API_URL}/products/toggle-deposit-like/${props.item.id}/`

  axios.post(endpoint, {}, {
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`
    }
  })
  .then(res => {
    isLiked.value = res.data.liked
  })
  .catch(err => {
    console.error('찜 실패:', err)
  })
}
</script>

<style scoped>
.product-card {
background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
border-radius: 20px;
border: 1px solid rgba(0, 0, 0, 0.06);
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
overflow: hidden;
position: relative;
animation: fadeInUp 0.6s ease-out;
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.product-card::before {
content: '';
position: absolute;
top: 0;
left: 0;
right: 0;
height: 4px;
background: linear-gradient(90deg, #3b82f6, #60a5fa, #93c5fd);
transform: scaleX(0);
transition: transform 0.3s ease;
}

.product-card:hover::before {
transform: scaleX(1);
}

.product-card:hover {
transform: translateY(-4px);
box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
border-color: rgba(59, 130, 246, 0.2);
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

.card-header {
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
color: white;
padding: 20px;
display: flex;
justify-content: space-between;
align-items: flex-start;
position: relative;
overflow: hidden;
}

.card-header::before {
content: '';
position: absolute;
top: 0;
left: 0;
right: 0;
bottom: 0;
background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23dots)"/></svg>');
opacity: 0.3;
}

.header-content {
flex: 1;
position: relative;
z-index: 1;
}

.product-title {
margin: 0 0 8px 0;
font-size: 18px;
font-weight: 700;
line-height: 1.3;
text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.bank-badge {
background: rgba(255, 255, 255, 0.2);
padding: 4px 12px;
border-radius: 12px;
font-size: 12px;
font-weight: 600;
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.3);
}

.card-rank {
width: 32px;
height: 32px;
background: rgba(255, 255, 255, 0.2);
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
position: relative;
z-index: 1;
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.3);
}

.card-rank i {
color: #fbbf24;
font-size: 16px;
}

.card-content {
padding: 24px;
}

.product-info {
margin-bottom: 20px;
}

.info-row {
display: flex;
gap: 16px;
margin-bottom: 16px;
}

.info-row:last-child {
margin-bottom: 0;
}

.info-item {
display: flex;
align-items: center;
gap: 12px;
flex: 1;
min-width: 0;
}

.info-item.full-width {
flex: 1 1 100%;
}

.info-icon {
width: 36px;
height: 36px;
border-radius: 10px;
display: flex;
align-items: center;
justify-content: center;
font-size: 14px;
color: #6b7280;
background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
border: 1px solid rgba(0, 0, 0, 0.06);
flex-shrink: 0;
}

.info-details {
flex: 1;
min-width: 0;
}

.label {
display: block;
font-size: 12px;
color: #6b7280;
font-weight: 600;
text-transform: uppercase;
letter-spacing: 0.05em;
margin-bottom: 2px;
}

.value {
display: block;
font-size: 14px;
color: #374151;
font-weight: 600;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
}

.value.highlight {
color: #dc2626;
font-size: 16px;
font-weight: 700;
}

.detail-btn {
width: 100%;
padding: 12px 16px;
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
color: white;
border: none;
border-radius: 12px;
font-weight: 600;
font-size: 14px;
cursor: pointer;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
gap: 8px;
box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.detail-btn:hover {
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

/* 모달 스타일 */
.modal-overlay {
position: fixed;
top: 0;
left: 0;
right: 0;
bottom: 0;
background: rgba(0, 0, 0, 0.5);
display: flex;
align-items: center;
justify-content: center;
z-index: 1000;
backdrop-filter: blur(5px);
animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
from { opacity: 0; }
to { opacity: 1; }
}

.modal-content {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 20px;
width: 90%;
max-width: 600px;
max-height: 90vh;
overflow-y: auto;
box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
border: 1px solid rgba(255, 255, 255, 0.2);
backdrop-filter: blur(10px);
animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
from {
  opacity: 0;
  transform: translateY(-50px) scale(0.9);
}
to {
  opacity: 1;
  transform: translateY(0) scale(1);
}
}

.modal-header {
display: flex;
justify-content: space-between;
align-items: flex-start;
padding: 24px;
border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.modal-title h3 {
font-size: 20px;
font-weight: 700;
color: #1f2937;
margin: 0 0 4px 0;
}

.modal-bank {
font-size: 14px;
color: #6b7280;
font-weight: 500;
}

.close-btn {
width: 32px;
height: 32px;
background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
border: none;
border-radius: 8px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
color: #6b7280;
transition: all 0.3s ease;
}

.close-btn:hover {
background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
color: white;
transform: scale(1.1);
}

.modal-body {
padding: 24px;
}

/* 핵심 정보 카드 */
.highlight-card {
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 16px;
margin-bottom: 24px;
}

.highlight-item {
background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
border-radius: 12px;
padding: 16px;
text-align: center;
border: 1px solid rgba(0, 0, 0, 0.06);
}

.highlight-icon {
width: 40px;
height: 40px;
border-radius: 10px;
display: flex;
align-items: center;
justify-content: center;
font-size: 16px;
color: white;
margin: 0 auto 8px;
}

.highlight-icon.rate {
background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
}

.highlight-icon.term {
background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
}

.highlight-icon.limit {
background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
}

.highlight-label {
display: block;
font-size: 12px;
color: #6b7280;
font-weight: 600;
margin-bottom: 4px;
}

.highlight-value {
font-size: 16px;
font-weight: 700;
color: #1f2937;
}

/* 상세 섹션 */
.detail-sections {
display: flex;
flex-direction: column;
gap: 20px;
}

.detail-section {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
padding: 20px;
border-radius: 12px;
border: 1px solid rgba(0, 0, 0, 0.05);
}

.section-header {
display: flex;
align-items: center;
gap: 8px;
margin-bottom: 16px;
padding-bottom: 12px;
border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.section-header i {
color: #3b82f6;
font-size: 16px;
}

.section-header h5 {
font-size: 16px;
font-weight: 700;
color: #1f2937;
margin: 0;
}

.section-content {
font-size: 14px;
}

.detail-item {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 12px;
}

.detail-item:last-child {
margin-bottom: 0;
}

.detail-label {
color: #6b7280;
font-weight: 500;
}

.detail-value {
color: #374151;
font-weight: 600;
}

/* 금리 비교 */
.rate-comparison {
display: grid;
grid-template-columns: repeat(2, 1fr);
gap: 16px;
}

.rate-box {
text-align: center;
padding: 16px;
border-radius: 12px;
border: 1px solid rgba(0, 0, 0, 0.06);
}

.rate-box.basic {
background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

.rate-box.premium {
background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
}

.rate-label {
display: block;
font-size: 12px;
color: #6b7280;
font-weight: 600;
margin-bottom: 8px;
}

.rate-value {
display: block;
font-size: 18px;
font-weight: 700;
color: #1f2937;
}

/* 혜택 목록 */
.benefit-list {
display: flex;
flex-direction: column;
gap: 12px;
}

.benefit-item {
display: flex;
align-items: center;
gap: 12px;
font-size: 14px;
color: #374151;
}

.benefit-item i {
color: #059669;
font-size: 16px;
}

.benefit-item strong {
color: #059669;
font-weight: 700;
}

/* 주의사항 */
.notice-list {
display: flex;
flex-direction: column;
gap: 10px;
}

.notice-item {
display: flex;
align-items: flex-start;
gap: 8px;
font-size: 13px;
color: #6b7280;
line-height: 1.5;
}

.notice-item i {
color: #f59e0b;
font-size: 8px;
margin-top: 6px;
}

/* 모달 푸터 */
.modal-footer {
display: flex;
gap: 12px;
padding: 24px;
border-top: 2px solid rgba(59, 130, 246, 0.1);
}

.action-btn {
flex: 1;
padding: 12px 16px;
border-radius: 12px;
font-size: 14px;
font-weight: 600;
cursor: pointer;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
gap: 6px;
border: none;
}

.action-btn.primary {
background: linear-gradient(135deg, #059669 0%, #10b981 100%);
color: white;
box-shadow: 0 4px 16px rgba(5, 150, 105, 0.3);
}

.action-btn.primary:hover {
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(5, 150, 105, 0.4);
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

.consult-modal {
  background: white;
  border-radius: 16px;
  padding: 32px 28px;
  width: 90%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  font-family: 'Noto Sans KR', sans-serif;
  animation: fadeInModal 0.3s ease-out;
  text-align: left;
}

.consult-modal h3 {
  margin: 0 0 16px;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

.consult-modal p {
  font-size: 14px;
  color: #374151;
  margin-bottom: 20px;
}

.consult-modal label {
  display: block;
  font-size: 13px;
  color: #6b7280;
  margin: 12px 0 4px;
  font-weight: 500;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #374151;
  gap: 8px;
  margin-bottom: 24px;
}

.consult-modal input[type="tel"] {
  width: 100%;
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 14px;
  margin-bottom: 16px;
  outline: none;
}

.consult-modal input[type="tel"]:focus {
  border-color: #3b82f6;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-actions button {
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-actions button:first-child {
  background-color: #3b82f6;
  color: white;
}


.modal-actions button:first-child:hover {
  background-color: #2563eb;
}

.modal-actions button:last-child {
  background-color: #e5e7eb;
  color: #374151;
}

.modal-actions button:last-child:hover {
  background-color: #d1d5db;
}

@keyframes fadeInModal {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}


/* 반응형 디자인 */
@media (max-width: 768px) {
.card-content {
  padding: 20px;
}

.info-row {
  flex-direction: column;
  gap: 12px;
}

.modal-content {
  width: 95%;
  margin: 20px;
 
}

.highlight-card {
  grid-template-columns: 1fr;
  gap: 12px;
}

.rate-comparison {
  grid-template-columns: 1fr;
  gap: 12px;
}

.modal-footer {
  flex-direction: column;
}
}

@media (max-width: 480px) {
.card-header {
  padding: 16px;
}

.product-title {
  font-size: 16px;
}

.card-content {
  padding: 16px;
}

.modal-header,
.modal-body,
.modal-footer {
  padding: 16px;
}

.detail-sections {
  gap: 16px;
}

.detail-section {
  padding: 16px;
}
}
</style>