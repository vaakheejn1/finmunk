<!-- Recommendresultcard.vue -->

<template>
    <div class="recommendation-card" :id="title === '예금' ? 'deposit-section' : 'saving-section'" ref="scrollTarget">
      <div class="card-header">
        <div class="header-icon">
          <i class="icon" :class="title === '예금' ? 'deposit-icon' : 'saving-icon'">📊</i>
        </div>
        <div class="header-content">
          <h3 class="card-title">{{ title }} 추천 TOP {{ products.length }}</h3>
          <p class="card-subtitle">맞춤형 금융상품을 확인하세요</p>
        </div>
      </div>
  
      <div class="user-profile">
        <div class="profile-item">
          <span class="profile-label">나이</span>
          <span class="profile-value">{{ user.age }}세</span>
        </div>
        <div class="profile-item">
          <span class="profile-label">월소득</span>
          <span class="profile-value">{{ user.monthly_income }}만원</span>
        </div>
        <div class="profile-item">
          <span class="profile-label">자산</span>
          <span class="profile-value">{{ user.assets }}만원</span>
        </div>
      </div>
  
      <div class="products-container">
        <div
          v-for="(item, index) in products"
          :key="index"
          class="product-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="product-header">
            <div class="bank-icon">🏦</div>
            <h4 class="product-name">{{ item.상품명 }}</h4>
            <div class="product-rank">{{ index + 1 }}위</div>
          </div>

          <!-- 찜하기 버튼 추가 -->
          <div class="wishlist-section">
            <button 
              @click="toggleWishlist(item, index)"
              :class="['wishlist-btn', { 'liked': item.isLiked, 'loading': item.isToggling }]"
              :disabled="item.isToggling"
            >
              <span class="heart-icon">{{ item.isLiked ? '❤️' : '🤍' }}</span>
              <span class="btn-text">
                {{ item.isToggling ? '처리중...' : (item.isLiked ? '찜 해제' : '찜하기') }}
              </span>
            </button>
          </div>
  
          <div class="product-details">
            <div class="detail-row">
              <div class="detail-item">
                <span class="detail-label">기간</span>
                <span class="detail-value">{{ item.기간 }}개월</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">월납입금</span>
                <span class="detail-value highlight">{{ item.월납입금 }}만원</span>
              </div>
            </div>
  
            <div class="detail-row">
              <div class="detail-item">
                <span class="detail-label">금리</span>
                <span class="detail-value rate">{{ item.금리 }}%</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">예상이자</span>
                <span class="detail-value profit">+{{ item.예상이자 }}만원</span>
              </div>
            </div>
  
            <div class="detail-row full-width">
              <div class="detail-item">
                <span class="detail-label">가입한도</span>
                <span class="detail-value">{{ formatLimit(item.가입한도) }}</span>
              </div>
            </div>
          </div>
  
          <div class="product-summary">
            <div class="summary-icon">💰</div>
            <p class="summary-text">
              {{ item.기간 }}개월 동안 매월 {{ item.월납입금 }}만원 저축 시
              <strong>{{ item.예상이자 }}만원</strong>의 이자 수익 예상
            </p>
          </div>
  
          <button
            class="toggle-btn"
            @click="toggleDetail(index)"
            :class="{ active: selectedIndex === index }"
          >
            <i class="fas" :class="selectedIndex === index ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
            {{ selectedIndex === index ? '상세정보 접기' : '상세정보 보기' }}
          </button>
  
          <div
            v-if="selectedIndex === index"
            class="detail-box"
            :style="{ animationDelay: '0.1s' }"
          >
            <div class="detail-sections">
              <!-- 기본 정보 섹션 -->
              <div class="detail-section">
                <div class="section-header">
                  <i class="fas fa-info-circle"></i>
                  <h5>기본 정보</h5>
                </div>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="info-label">가입 방법</span>
                    <span class="info-value">{{ item.가입방법 || '영업점, 인터넷뱅킹' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">만기 유형</span>
                    <span class="info-value">{{ item.만기유형 || '만기일시지급' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">기본 금리</span>
                    <span class="info-value rate">{{ (parseFloat(item.금리) - 0.3).toFixed(1) }}%</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">최고 금리</span>
                    <span class="info-value rate">{{ item.최고금리 || item.금리 }}%</span>
                  </div>
                </div>
              </div>
  
              <!-- 우대 조건 섹션 -->
              <div class="detail-section">
                <div class="section-header">
                  <i class="fas fa-star"></i>
                  <h5>우대 조건</h5>
                </div>
                <div class="benefit-list">
                  <div class="benefit-item">
                    <i class="fas fa-check-circle"></i>
                    <span>인터넷뱅킹 가입 시 <strong>+0.1%</strong></span>
                  </div>
                  <div class="benefit-item">
                    <i class="fas fa-check-circle"></i>
                    <span>자동이체 등록 시 <strong>+0.1%</strong></span>
                  </div>
                  <div class="benefit-item">
                    <i class="fas fa-check-circle"></i>
                    <span>급여이체 고객 <strong>+0.1%</strong></span>
                  </div>
                </div>
              </div>
  
              <!-- 수익 시뮬레이션 섹션 -->
              <div class="detail-section">
                <div class="section-header">
                  <i class="fas fa-calculator"></i>
                  <h5>수익 시뮬레이션</h5>
                </div>
                <div class="simulation-box">
                  <div class="simulation-row">
                    <span class="sim-label">월 납입액</span>
                    <span class="sim-value">{{ item.월납입금 }}만원</span>
                  </div>
                  <div class="simulation-row">
                    <span class="sim-label">적용 금리</span>
                    <span class="sim-value rate">{{ item.금리 }}%</span>
                  </div>
                  <div class="simulation-row">
                    <span class="sim-label">저축 기간</span>
                    <span class="sim-value">{{ item.기간 }}개월</span>
                  </div>
                  <div class="divider"></div>
                  <div class="simulation-row">
                    <span class="sim-label">총 납입액</span>
                    <span class="sim-value">{{ (item.월납입금 * item.기간).toLocaleString() }}만원</span>
                  </div>
                  <div class="simulation-row">
                    <span class="sim-label">이자 수익</span>
                    <span class="sim-value profit">+{{ item.예상이자 }}만원</span>
                  </div>
                  <div class="simulation-row highlight">
                    <span class="sim-label">만기 수령액</span>
                    <span class="sim-value total">
                      {{ (item.월납입금 * item.기간 + item.예상이자).toLocaleString() }}만원
                    </span>
                  </div>
                </div>
              </div>
  
              <!-- 유의사항 섹션 -->
              <div class="detail-section">
                <div class="section-header">
                  <i class="fas fa-exclamation-triangle"></i>
                  <h5>유의사항</h5>
                </div>
                <div class="notice-list">
                  <div class="notice-item">
                    <i class="fas fa-dot-circle"></i>
                    <span>금리는 가입시점 기준이며, 시장금리 변동에 따라 조정될 수 있습니다</span>
                  </div>
                  <div class="notice-item">
                    <i class="fas fa-dot-circle"></i>
                    <span>중도해지 시 중도해지이율이 적용됩니다</span>
                  </div>
                  <div class="notice-item">
                    <i class="fas fa-dot-circle"></i>
                    <span>이자소득세(15.4%)가 부과됩니다</span>
                  </div>
                </div>
              </div>
  
              <!-- 액션 버튼 -->
              <div class="action-section">
                <button class="action-btn primary" @click="consultProduct(item)">
                  <i class="fas fa-headset"></i>
                  상담 신청
                </button>
                <button class="action-btn secondary" @click="compareProduct(item)">
                  <i class="fas fa-balance-scale"></i>
                  상품 비교
                </button>
                <button class="action-btn secondary" @click="findBranch(item)">
                  <i class="fas fa-map-marker-alt"></i>
                  지점 찾기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div v-if="showConsultModal" class="modal-overlay" @click.self="closeConsultModal">
        <div class="modal">
          <h3>금융 정보 상담 신청</h3>
          <p><strong>{{ currentProduct?.상품명 }}</strong> 상품 상담을 원하시나요?</p>

          <label>전화번호</label>
          <input v-model="consultPhone" placeholder="010-1234-5678" type="tel" />

          <label><input type="checkbox" v-model="agree" /> 개인정보 제공에 동의합니다.</label>

          <div class="modal-actions">
            <button @click="submitConsultRequest" :disabled="!agree || !consultPhone">신청</button>
            <button @click="closeConsultModal">취소</button>
          </div>
        </div>
      </div>
    </Teleport>

  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const props = defineProps({
    title: String,
    products: Array,
    user: Object,
  })
  
  const selectedIndex = ref(null)
  const scrollTarget = ref(null)
  
  // 컴포넌트 마운트 시 각 상품에 찜 상태 초기화
  onMounted(() => {
    console.log('추천 상품 데이터:', props.products)
    console.log('제목:', props.title)
    initializeWishlistStatus()
  })

  const showConsultModal = ref(false)
  const consultPhone = ref('')
  const agree = ref(false)
  const currentProduct = ref(null)

  function consultProduct(item) {
    currentProduct.value = item
    showConsultModal.value = true
    consultPhone.value = ''
    agree.value = false
  }

  function closeConsultModal() {
    showConsultModal.value = false
  }

  // 신청 전송
  function submitConsultRequest() {
    axios.post(`${import.meta.env.VITE_API_URL}/consultations/`, {
      product_name: currentProduct.value.상품명,
      phone: consultPhone.value,
    }, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    }).then(() => {
      alert('상담 신청이 완료되었습니다!')
      closeConsultModal()
    }).catch(() => {
      alert('오류가 발생했어요 😥')
    })
  }
  
  // 찜 상태 초기화
  const initializeWishlistStatus = () => {
    props.products.forEach(item => {
      // 백엔드에서 이미 설정된 값들 확인
      if (!item.hasOwnProperty('isLiked')) {
        item.isLiked = false
      }
      if (!item.hasOwnProperty('isToggling')) {
        item.isToggling = false
      }
      // 백엔드에서 제공하는 실제 상품 ID 사용
      if (!item.hasOwnProperty('productId')) {
        item.productId = item.id
      }
    })
  }
  
  // 찜하기 토글 함수
// 찜하기 토글 함수
const toggleWishlist = async (item, index) => {
  if (item.isToggling || !item.productId) {
    if (!item.productId) {
      showToast('이 상품은 찜하기를 지원하지 않습니다.', 'error')
    }
    return
  }

  item.isToggling = true

  try {
    const isSaving = props.title === '적금'
    const endpoint = `${import.meta.env.VITE_API_URL}/products/${isSaving ? 'toggle-saving-like' : 'toggle-deposit-like'}/${item.productId}/`

    const response = await axios.post(endpoint, {}, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })

    item.isLiked = response.data.liked
    showToast(
      item.isLiked 
        ? `${item.상품명}을(를) 찜 목록에 추가했습니다! ❤️` 
        : `${item.상품명}을(를) 찜 목록에서 제거했습니다.`,
      'success'
    )
  } catch (error) {
    console.error('찜 실패:', error)
    if (error.response?.status === 404) {
      showToast('상품을 찾을 수 없습니다.', 'error')
    } else if (error.response?.status === 401) {
      showToast('로그인이 필요합니다.', 'error')
    } else {
      showToast('찜하기에 실패했습니다. 다시 시도해주세요.', 'error')
    }
  } finally {
    item.isToggling = false
  }
}

  
  // 토스트 메시지 함수
  const showToast = (message, type = 'success') => {
    // 간단한 alert 구현 (추후 더 나은 토스트 UI로 교체 가능)
    const emoji = type === 'success' ? '✅' : '❌'
    alert(`${emoji} ${message}`)
  }
  
  function toggleDetail(index) {
    selectedIndex.value = selectedIndex.value === index ? null : index
  }
  
  import { useRouter } from 'vue-router'
  const router = useRouter()

  function compareProduct(item) {
    router.push({ name: 'Compare' })
  }

  function findBranch(item) {
    router.push({ name: 'Bankmap' })
  }


  
  function formatLimit(limit) {
    const amount = Number(limit)
    if (!amount || amount === 0) return '한도 없음'
    if (amount >= 100000000) return `${(amount / 100000000).toLocaleString()}억 원`
    if (amount >= 10000) return `${(amount / 10000).toLocaleString()}만원`
    return `${amount.toLocaleString()}원`
  }
  </script>  
  
<style scoped>
.recommendation-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 24px;
  padding: 32px;
  margin: 24px 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideUp 0.6s ease-out;
}

.recommendation-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.12);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.header-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.icon {
  font-size: 24px;
  filter: brightness(0) invert(1);
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 4px 0;
  letter-spacing: -0.025em;
}

.card-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

.user-profile {
  display: flex;
  gap: 24px;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 28px;
  border: 1px solid rgba(34, 197, 94, 0.1);
}

.profile-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.profile-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.profile-value {
  font-size: 18px;
  font-weight: 700;
  color: #059669;
}

.products-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-card {
  background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
  border-radius: 20px;
  padding: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeInUp 0.6s ease-out both;
  position: relative;
  overflow: hidden;
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
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
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

.product-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.bank-icon {
  font-size: 20px;
  margin-right: 12px;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-name {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  flex: 1;
}

.product-rank {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* 찜하기 버튼 스타일 */
.wishlist-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.wishlist-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.wishlist-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.wishlist-btn.liked {
  border-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
}

.wishlist-btn:not(.liked) {
  border-color: #d1d5db;
  color: #6b7280;
}

.wishlist-btn:not(.liked):hover {
  border-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
}

.wishlist-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.wishlist-btn.loading {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-color: #d1d5db;
  color: #6b7280;
}

.heart-icon {
  font-size: 16px;
  transition: transform 0.2s ease;
}

.wishlist-btn:hover .heart-icon {
  transform: scale(1.1);
}

.btn-text {
  font-size: 14px;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.detail-row {
  display: flex;
  gap: 20px;
}

.detail-row.full-width .detail-item {
  flex: 1;
}

.detail-item {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.detail-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.detail-value {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.detail-value.highlight {
  color: #1d4ed8;
  font-weight: 700;
}

.detail-value.rate {
  color: #dc2626;
  font-weight: 700;
}

.detail-value.profit {
  color: #059669;
  font-weight: 700;
}

.product-summary {
  display: flex;
  align-items: flex-start;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(245, 158, 11, 0.2);
  margin-bottom: 16px;
}

.summary-icon {
  font-size: 20px;
  margin-right: 12px;
  margin-top: 2px;
}

.summary-text {
  font-size: 14px;
  color: #92400e;
  margin: 0;
  line-height: 1.5;
  font-weight: 500;
}

.summary-text strong {
  color: #b45309;
  font-weight: 700;
}

.toggle-btn {
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

.toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

.toggle-btn.active {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  box-shadow: 0 4px 16px rgba(5, 150, 105, 0.3);
}

.toggle-btn i {
  transition: transform 0.3s ease;
}

.detail-box {
  margin-top: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(59, 130, 246, 0.1);
  animation: slideDown 0.4s ease-out both;
  backdrop-filter: blur(5px);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
    max-height: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0);
    max-height: 1000px;
  }
}

.detail-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.info-value.rate {
  color: #dc2626;
  font-weight: 700;
}

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

.simulation-box {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.simulation-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  font-size: 14px;
}

.simulation-row.highlight {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  margin: 8px -16px -16px -16px;
  padding: 12px 16px;
  border-radius: 0 0 12px 12px;
  font-weight: 700;
}

.sim-label {
  color: #6b7280;
  font-weight: 500;
}

.sim-value {
  font-weight: 600;
  color: #374151;
}

.sim-value.rate {
  color: #dc2626;
  font-weight: 700;
}

.sim-value.profit {
  color: #059669;
  font-weight: 700;
}

.sim-value.total {
  color: #b45309;
  font-weight: 700;
  font-size: 16px;
}

.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.2), transparent);
  margin: 8px 0;
}

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

.action-section {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 120px;
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

/* 모달 전체 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* 모달 본체 */
.modal {
  background: white;
  border-radius: 16px;
  padding: 28px 24px;
  width: 90%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  font-family: 'Noto Sans KR', sans-serif;
  animation: fadeInModal 0.3s ease-out;
}

/* 제목 */
.modal h3 {
  margin: 0 0 16px;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

/* 안내 문구 */
.modal p {
  font-size: 14px;
  color: #374151;
  margin-bottom: 20px;
}

/* 라벨 */
.modal label {
  display: block;
  font-size: 13px;
  color: #6b7280;
  margin: 12px 0 4px;
  font-weight: 500;
}

/* 전화번호 입력창 */
.modal input[type="tel"] {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 14px;
  margin-bottom: 10px;
  outline: none;
  transition: border-color 0.3s;
}
.modal input[type="tel"]:focus {
  border-color: #3b82f6;
}

/* 체크박스 줄 맞춤 */
.modal input[type="tel"] {
  box-sizing: border-box;
  margin-right: 6px;
  vertical-align: middle;
}

/* 버튼 영역 */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

/* 버튼 스타일 */
.modal-actions button {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
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

/* 간단한 fade-in 애니메이션 */
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
  .recommendation-card {
    padding: 20px;
    margin: 16px 0;
  }
  
  .user-profile {
    flex-direction: column;
    gap: 16px;
  }
  
  .profile-item {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .detail-row {
    flex-direction: column;
    gap: 12px;
  }
  
  .card-title {
    font-size: 20px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .action-section {
    flex-direction: column;
  }
  
  .action-btn {
    min-width: auto;
  }

  .wishlist-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .detail-sections {
    gap: 16px;
  }
  
  .detail-section {
    padding: 16px;
  }
  
  .simulation-box {
    padding: 12px;
  }
  
  .action-section {
    gap: 8px;
  }

  .wishlist-section {
    margin-bottom: 16px;
  }
}
</style>