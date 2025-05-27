<template>
  <div class="mypage-container">
    <!-- 헤더 영역 - 다람쥐 테마 -->
    <div class="header-section">
      <div class="floating-acorns">
        <span class="acorn" v-for="n in 5" :key="n">🌰</span>
      </div>
      <div class="header-content">
        <div class="user-avatar-wrapper">
          <div class="avatar-circle">
            <img
              v-if="store.user.profile_image"
              :src="`http://localhost:8000${store.user.profile_image}`"
              alt="프로필 이미지"
              class="profile-img"
            />
            <span v-else class="squirrel-emoji">🐿️</span>
          </div>
          <div class="avatar-decoration">
            <span class="leaf left">🍃</span>
            <span class="leaf right">🍃</span>
          </div>
        </div>
        <div class="user-info">
          <h2 class="user-name">
            <span class="bounce-text">{{ store.user.username }}</span>
            <span class="squirrel-icon">🐿️</span>
          </h2>
          <p class="user-subtitle">
            <span>{{ store.user.bio || '자기소개가 없습니다.' }}</span>
          </p>
        </div>
        <button @click="showEditModal = true" class="edit-btn">
          <span class="btn-icon">🌰</span>
          정보수정
        </button>
      </div>
    </div>

    <!-- 정보 카드들 - 애니메이션 추가 -->
    <div class="info-cards">
      <div class="info-card" v-for="(card, index) in infoCards" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">
        <div class="card-icon bounce">{{ card.icon }}</div>
        <div class="card-content">
          <h3>{{ card.title }}</h3>
          <div v-html="card.content"></div>
        </div>
        <div class="card-bg-icon">{{ card.bgIcon }}</div>
      </div>
    </div>

    <!-- 찜한 상품 섹션 -->
    <div class="wishlist-section">
      <h2 class="section-title">
        <span class="title-icon wiggle">❤️</span>
        찜한 상품 목록
        <span class="acorn-count">🌰 × {{ deposits.length + savings.length }}</span>
      </h2>

      <div class="products-container">
        <transition-group name="card-flip" tag="div" class="product-grid">
          <div
            v-for="item in paginatedProducts"
            :key="item.id"
            class="product-card"
            @click="openProductModal(item)"
          >
            <div class="product-header">
              <span class="product-type">{{ item.product_type === 'deposit' ? '💰' : '💸' }}</span>
              <span class="bank-badge">{{ item.bank_name }}</span>
            </div>
            <div class="product-title">{{ item.product_name }}</div>
            <div class="product-details">
              <div class="detail-item">
                <span class="detail-icon">📈</span>
                <span>{{ item.interest_rate2 || item.interest_rate }}%</span>
              </div>
              <div class="detail-item">
                <span class="detail-icon">⏱️</span>
                <span>{{ item.save_term }}개월</span>
              </div>
            </div>
            <div class="hover-squirrel">🐿️</div>
          </div>
        </transition-group>
        <!-- 페이지네이션 컨트롤 -->
<div v-if="totalPages > 1" class="pagination">
  <button @click="prevPage" :disabled="currentPage === 1">이전</button>
  <span>&lt;{{ currentPage }}/{{ totalPages }}&gt;</span>
  <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
</div>
      </div>
    </div>

    <!-- 좋아요한 게시글 섹션 -->
    <div class="liked-section">
      <h2 class="section-title">
        <span class="title-icon bounce">🧡</span>
        좋아요한 게시글
        <span class="acorn-count">🌰 × {{ likedArticles.length }}</span>
      </h2>

      <transition-group name="slide-fade" tag="div" class="liked-grid">
  <RouterLink
    v-for="article in paginatedArticles"
    :key="article.id"
    :to="{ name: 'CommunityArticle', params: { id: article.id } }"
    class="liked-card"
  >
          <div class="liked-header">
            <span class="liked-icon">📌</span>
            <h3 class="liked-title">{{ article.title }}</h3>
          </div>
          <p class="liked-preview">{{ truncateText(article.content, 60) }}</p>
          <div class="liked-footer">
            <span class="author">✍️ {{ article.user.username }}</span>
            <span class="comments">💬 {{ article.comment_count }}</span>
          </div>
          <div class="card-squirrel">🐿️</div>
        </RouterLink>
      </transition-group>
        <!-- 페이지네이션 버튼 -->
<div v-if="totalArticlePages > 1" class="pagination article-pagination">
  <button @click="prevArticlePage" :disabled="articlePage === 1">이전</button>
  <span>&lt;{{ articlePage }}/{{ totalArticlePages }}&gt;</span>
  <button @click="nextArticlePage" :disabled="articlePage === totalArticlePages">다음</button>
</div>


    </div>

    <!-- 수정 모달 - 귀여운 스타일 -->
    <Transition name="modal">
      <div v-if="showEditModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-decoration">
            <span class="deco-item" v-for="n in 6" :key="n">🌰</span>
          </div>
          
          <div class="modal-header">
            <h3>
              <span class="header-icon wiggle">🐿️</span>
              정보 수정하기
            </h3>
            <button @click="showEditModal = false" class="close-btn">
              <span class="close-icon">✕</span>
            </button>
          </div>

          <form @submit.prevent="updateProfile" class="modal-form">
            <div class="form-group">
              <label>
                <span class="label-icon">🖼️</span>
                프로필 이미지
              </label>
              <div class="file-input-wrapper">
                <input type="file" @change="handleImageUpload" id="file-input" />
                <label for="file-input" class="file-label">
                  <span>🌰 이미지 선택</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>
                <span class="label-icon">📝</span>
                자기소개 (bio)
              </label>
              <textarea
                v-model="form.bio"
                placeholder="나를 소개해보세요!"
                class="cute-input"
                rows="3"
              />
            </div>

            <div class="form-group">
              <label>
                <span class="label-icon">🏷️</span>
                닉네임
              </label>
              <input 
                type="text" 
                v-model="form.username" 
                placeholder="귀여운 닉네임을 지어주세요!" 
                class="cute-input"
              />
            </div>

            <div class="form-group">
              <label>
                <span class="label-icon">🎂</span>
                나이
              </label>
              <input 
                type="number" 
                v-model="form.age" 
                placeholder="몇 살이신가요?" 
                class="cute-input"
              />
            </div>

            <div class="form-group">
              <label class="checkbox-wrapper">
                <input type="checkbox" v-model="form.job" class="custom-checkbox" />
                <span class="checkbox-label">
                  <span class="checkbox-icon">{{ form.job ? '✅' : '⬜' }}</span>
                  💼 현재 일하고 있어요!
                </span>
              </label>
            </div>

            <div class="form-group">
              <label>
                <span class="label-icon">💵</span>
                월 소득 (만원)
              </label>
              <input 
                type="number" 
                v-model="form.income" 
                placeholder="한 달에 얼마나 버시나요?" 
                class="cute-input"
              />
            </div>

            <div class="form-group">
              <label>
                <span class="label-icon">💎</span>
                총 자산 (만원)
              </label>
              <input 
                type="number" 
                v-model="form.assets" 
                placeholder="총 자산을 알려주세요!" 
                class="cute-input"
              />
            </div>

              <button type="button" @click="confirmWithdrawal" class="withdraw-btn">
                <span class="withdraw-icon">🗑️</span>
                탈퇴하기
              </button>
            

            <div class="modal-actions">
              <button type="button" @click="showEditModal = false" class="cancel-btn">
                <span>🙅‍♀️ 취소</span>
              </button>
              <button type="submit" class="save-btn">
                <span class="save-icon bounce">💾</span>
                저장하기
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>

    <!-- 플로팅 다람쥐 -->
    <div class="floating-squirrel" @click="playSquirrelSound">
      <span class="squirrel">🐿️</span>
      <span class="speech-bubble">도토리 모으자!</span>
    </div>
  </div>

  <template v-if="showProductModal">
  <div class="modal-overlay" @click="closeProductModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>{{ selectedItem.product_name }}</h3>
        <button class="close-btn" @click="closeProductModal">✕</button>
      </div>

      <div class="modal-body">
        <p><strong>은행:</strong> {{ selectedItem.bank_name }}</p>
        <p><strong>금리:</strong> {{ selectedItem.interest_rate2 || selectedItem.interest_rate }}%</p>
        <p><strong>기간:</strong> {{ selectedItem.save_term }}개월</p>
        <p><strong>가입제한:</strong> {{ selectedItem.join_restriction_text || '정보 없음' }}</p>
      </div>

      <div class="modal-footer">
        <button class="action-btn secondary" @click="toggleLike(selectedItem)">
          {{ selectedItem.is_liked ? '찜하기' : '찜취소' }}
        </button>
      </div>
    </div>
  </div>
</template>

</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
const API_BASE_URL = import.meta.env.VITE_API_URL

const router = useRouter()

const store = useUserStore()
const showEditModal = ref(false)

const selectedItem = ref(null)
const showProductModal = ref(false)

const openProductModal = (item) => {
  selectedItem.value = item
  showProductModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeProductModal = () => {
  showProductModal.value = false
  selectedItem.value = null
  document.body.style.overflow = 'auto'
}

const form = ref({
  username: '',
  age: null,
  job: false,
  income: null,
  assets: null,
  profile_image: null,
})

const deposits = ref([])
const savings = ref([])
const likedArticles = ref([])



// 게시글 페이지네이션
const articlePage = ref(1)
const articlesPerPage = 3

const totalArticlePages = computed(() => Math.ceil(likedArticles.value.length / articlesPerPage))

const paginatedArticles = computed(() => {
  const start = (articlePage.value - 1) * articlesPerPage
  return likedArticles.value.slice(start, start + articlesPerPage)
})

const nextArticlePage = () => {
  if (articlePage.value < totalArticlePages.value) articlePage.value++
}

const prevArticlePage = () => {
  if (articlePage.value > 1) articlePage.value--
}


// 정보 카드 데이터
const infoCards = computed(() => [
  {
    icon: '👤',
    bgIcon: '🌰',
    title: '기본 정보',
    content: `
      <p><span class="label">이메일:</span> ${store.user.email}</p>
      <p><span class="label">나이:</span> ${store.user.age}세</p>
    `
  },
  {
    icon: '💼',
    bgIcon: '🍃',
    title: '직업 정보',
    content: `
      <p><span class="label">직업 상태:</span> 
        <span class="${store.user.job ? 'status-active' : 'status-inactive'}">
          ${store.user.job ? '일하는 다람쥐 🐿️' : '쉬는 다람쥐 😴'}
        </span>
      </p>
      <p><span class="label">월 소득:</span> ${formatMoney(store.user.income)}만원</p>
    `
  },
  {
    icon: '💰',
    bgIcon: '🌳',
    title: '자산 정보',
    content: `
      <p><span class="label">총 자산:</span> ${formatMoney(store.user.assets)}만원</p>
      <div class="asset-level">
        <span class="level-badge wiggle">${getAssetLevel(store.user.assets)}</span>
      </div>
    `
  }
])

onMounted(() => {
  if (store.user) {
    form.value = { ...store.user }
    fetchWishlist()
    fetchLikedArticles()
  }
})

const fetchWishlist = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/products/liked-products/`, {
      headers: { Authorization: `Token ${store.token}` }
    })

    deposits.value = res.data.deposits.map(d => ({ ...d, product_type: 'deposit' }))
    savings.value = res.data.savings.map(s => ({ ...s, product_type: 'saving' }))
  } catch (err) {
    console.error('찜 목록 불러오기 실패:', err)
  }
}


// 탈퇴하기
const confirmWithdrawal = () => {
  if (confirm('정말 탈퇴하시겠어요? 😢\n모든 정보가 삭제되고 복구할 수 없어요.')) {
    axios.delete(`${API_BASE_URL}/users/delete/`, {
      headers: { Authorization: `Token ${store.token}` }
    })

    .then(() => {
      alert('탈퇴가 완료되었어요 🐿️ 안녕히 가세요!')
      store.logOut()
      router.push({ name: 'Home' })
    })
    .catch(err => {
      console.error('탈퇴 실패:', err)
      alert('탈퇴 중 오류가 발생했어요!')
    })
  }
}


const fetchLikedArticles = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/community/articles/liked/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
    likedArticles.value = res.data
  } catch (err) {
    console.error('좋아요한 게시글 불러오기 실패:', err)
  }
}

const handleImageUpload = (event) => {
  form.value.profile_image = event.target.files[0]
}

const formatMoney = (amount) => {
  if (!amount) return '0'
  return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const getAssetLevel = (assets) => {
  if (assets >= 10000) return '🏆 도토리 왕'
  if (assets >= 5000) return '💎 부자 다람쥐'
  if (assets >= 1000) return '🌟 중산층 다람쥐'
  if (assets >= 100) return '🌱 새싹 다람쥐'
  return '🐿️ 아기 다람쥐'
}

const truncateText = (text, length) => {
  return text.length > length ? text.slice(0, length) + '...' : text
}

const closeModal = (e) => {
  if (e.target === e.currentTarget) {
    showEditModal.value = false
  }
}

const updateProfile = async () => {
  const formData = new FormData()
  Object.keys(form.value).forEach(key => {
    if (form.value[key] !== null) {
      formData.append(key, form.value[key])
    }
  })

  try {
    const res = await axios.put(`${API_BASE_URL}/users/profile/`, formData, {
      headers: {
        Authorization: `Token ${store.token}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    alert('🐿️ 도토리가 저장되었어요!')
    store.user = res.data
    showEditModal.value = false
  } catch (err) {
    console.error('수정 실패:', err)
    alert('❌ 도토리 저장에 실패했어요ㅠㅠ')
  }
}

const playSquirrelSound = () => {
  // 다람쥐 클릭 시 애니메이션 효과
  const squirrel = document.querySelector('.floating-squirrel')
  squirrel.classList.add('clicked')
  setTimeout(() => squirrel.classList.remove('clicked'), 300)
}

const toggleLike = (item) => {
  const isSaving = item.product_type === 'saving'
  const endpoint = isSaving
    ? `${API_BASE_URL}/products/toggle-saving-like/${item.id}/`
    : `${API_BASE_URL}/products/toggle-deposit-like/${item.id}/`

  axios.post(endpoint, {}, {
    headers: { Authorization: `Token ${store.token}` }
  })

  .then(res => {
    item.is_liked = res.data.liked

    // 찜 취소 시 목록에서 제거하고 모달 닫기
    if (!res.data.liked) {
      deposits.value = deposits.value.filter(p => p.id !== item.id)
      savings.value = savings.value.filter(s => s.id !== item.id)
      closeProductModal()
    }
  })
  .catch(err => {
    console.error('찜 토글 실패:', err)
    alert('찜 변경 중 오류가 발생했어요!')
  })
}



// 페이지 네이션
const currentPage = ref(1)
const itemsPerPage = 8

const allProducts = computed(() => [...deposits.value, ...savings.value])

const totalPages = computed(() => Math.ceil(allProducts.value.length / itemsPerPage))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return allProducts.value.slice(start, start + itemsPerPage)
})

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}



</script>

<style scoped>

/* 마이페이지 좋아요 게시글 페이지네이션 */
.article-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 20px;
  font-weight: 600;
  font-size: 1rem;
}

.article-pagination button {
  background: #fb923c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.3s;
}

.article-pagination button:disabled {
  background: #ddd;
  cursor: not-allowed;
}




/*  마이페이지 상품 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  font-weight: 600;
  font-size: 1rem;
}

.pagination button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.3s;
}

.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}



/* 탈퇴버튼 */
.withdraw-btn {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
}

.withdraw-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.withdraw-icon {
  display: inline-block;
  animation: wiggle 2s infinite;
}




/* 기본 스타일 */
.mypage-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
  background: #f8fdf8;
  min-height: 100vh;
}

/* 헤더 섹션 */
.header-section {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 30px;
  padding: 40px;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.floating-acorns {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.acorn {
  position: absolute;
  font-size: 2rem;
  animation: float 6s infinite ease-in-out;
  opacity: 0.3;
}

.acorn:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.acorn:nth-child(2) { top: 20%; left: 80%; animation-delay: 1s; }
.acorn:nth-child(3) { top: 60%; left: 20%; animation-delay: 2s; }
.acorn:nth-child(4) { top: 70%; left: 70%; animation-delay: 3s; }
.acorn:nth-child(5) { top: 40%; left: 50%; animation-delay: 4s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.header-content {
  display: flex;
  align-items: center;
  gap: 30px;
  position: relative;
  z-index: 1;
}

.user-avatar-wrapper {
  position: relative;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  animation: bounce 2s infinite;
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.squirrel-emoji {
  font-size: 3rem;
}

.avatar-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.leaf {
  position: absolute;
  font-size: 1.5rem;
  animation: sway 3s infinite ease-in-out;
}

.leaf.left {
  top: -10px;
  left: -10px;
  animation-delay: 0s;
}

.leaf.right {
  bottom: -10px;
  right: -10px;
  animation-delay: 1.5s;
}

@keyframes sway {
  0%, 100% { transform: rotate(-10deg); }
  50% { transform: rotate(10deg); }
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.bounce-text {
  display: inline-block;
  animation: textBounce 3s infinite;
}

@keyframes textBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.squirrel-icon {
  font-size: 1.5rem;
  animation: wiggle 2s infinite;
}

.user-subtitle {
  color: #555;
  margin-top: 5px;
}

.typing-text {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid #555;
  animation: typing 3s steps(20) infinite;
}

@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}

.edit-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3);
}

.edit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.btn-icon {
  animation: rotate 2s infinite linear;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 정보 카드 */
.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.info-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  animation: cardSlide 0.6s ease-out backwards;
}

@keyframes cardSlide {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
  display: inline-block;
}

.card-bg-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;
  font-size: 4rem;
  opacity: 0.1;
  transform: rotate(-15deg);
}

.label {
  color: #666;
  font-weight: 500;
}

.status-active,
.status-inactive {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-left: 10px;
}

.status-active {
  background: #4CAF50;
  color: white;
}

.status-inactive {
  background: #FF9800;
  color: white;
}

.level-badge {
  display: inline-block;
  padding: 8px 16px;
  background: linear-gradient(135deg, #FFD93D 0%, #FFB344 100%);
  color: #333;
  border-radius: 20px;
  font-weight: 700;
  margin-top: 10px;
  box-shadow: 0 3px 10px rgba(255, 193, 7, 0.3);
}

/* 찜한 상품 섹션 */
.wishlist-section,
.liked-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  display: inline-block;
}

.acorn-count {
  margin-left: auto;
  font-size: 1rem;
  color: #666;
  background: #fff3cd;
  padding: 5px 15px;
  border-radius: 20px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.product-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.product-card:hover .hover-squirrel {
  opacity: 1;
  transform: translateY(0);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.product-type {
  font-size: 1.5rem;
}

.bank-badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.product-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 15px;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 0.95rem;
}

.detail-icon {
  font-size: 1rem;
}

.hover-squirrel {
  position: absolute;
  bottom: 10px;
  right: 10px;
  font-size: 2rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s;
}

/* 좋아요한 게시글 */
.liked-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.liked-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  text-decoration: none;
  color: inherit;
  position: relative;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.liked-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.liked-card:hover .card-squirrel {
  opacity: 1;
  transform: rotate(0deg);
}

.liked-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.liked-icon {
  font-size: 1.3rem;
}

.liked-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.liked-preview {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.liked-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 0.9rem;
}

.card-squirrel {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  opacity: 0;
  transform: rotate(-45deg);
  transition: all 0.3s;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background: white;
  border-radius: 30px;
  padding: 40px;
  width: 90%;
  max-width: 500px;
  position: relative;
  overflow: visible;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
}

.modal-decoration {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.deco-item {
  font-size: 1.5rem;
  animation: bounce 2s infinite;
}

.deco-item:nth-child(even) {
  animation-delay: 0.5s;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.modal-header h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.header-icon {
  display: inline-block;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.close-btn:hover {
  background: #f5f5f5;
  transform: rotate(90deg);
}

/* 폼 스타일 */
.form-group {
  margin-bottom: 20px;
  margin-right: 2rem;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.label-icon {
  margin-right: 5px;
}

.cute-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #f8f8f8;
}

.cute-input:focus {
  outline: none;
  border-color: #4CAF50;
  background: white;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.file-input-wrapper {
  position: relative;
}

#file-input {
  display: none;
}

.file-label {
  display: inline-block;
  padding: 10px 20px;
  background: #fff3cd;
  color: #856404;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}

.file-label:hover {
  background: #ffeaa7;
  transform: translateY(-2px);
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.custom-checkbox {
  display: none;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.checkbox-icon {
  font-size: 1.2rem;
  transition: all 0.3s;
}

.modal-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.cancel-btn,
.save-btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.save-btn {
  background: #4CAF50;
  color: white;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3);
}

.save-btn:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.save-icon {
  display: inline-block;
}

/* 플로팅 다람쥐 */
.floating-squirrel {
  position: fixed;
  bottom: 30px;
  right: 30px;
  cursor: pointer;
  z-index: 999;
  animation: floatSquirrel 3s infinite ease-in-out;
}

@keyframes floatSquirrel {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.floating-squirrel .squirrel {
  font-size: 3rem;
  display: block;
  transition: all 0.3s;
}

.floating-squirrel:hover .squirrel {
  transform: scale(1.2) rotate(10deg);
}

.floating-squirrel.clicked .squirrel {
  animation: squirrelJump 0.3s ease-out;
}

@keyframes squirrelJump {
  0% { transform: scale(1); }
  50% { transform: scale(0.8); }
  100% { transform: scale(1.2); }
}

.speech-bubble {
  position: absolute;
  bottom: 100%;
  right: 0;
  background: white;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 0.9rem;
  white-space: nowrap;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s;
  pointer-events: none;
}

.speech-bubble::after {
  content: '';
  position: absolute;
  top: 100%;
  right: 20px;
  border: 8px solid transparent;
  border-top-color: white;
}

.floating-squirrel:hover .speech-bubble {
  opacity: 1;
  transform: translateY(0);
}

/* 애니메이션 클래스 */
.bounce {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.wiggle {
  animation: wiggle 2s infinite;
}

@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

/* 트랜지션 효과 */
.card-flip-enter-active,
.card-flip-leave-active {
  transition: all 0.5s;
}

.card-flip-enter-from {
  opacity: 0;
  transform: rotateY(90deg);
}

.card-flip-leave-to {
  opacity: 0;
  transform: rotateY(-90deg);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.8);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }

  .user-name {
    font-size: 1.5rem;
    justify-content: center;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .product-grid,
  .liked-grid {
    grid-template-columns: 1fr;
  }

  .section-title {
    flex-wrap: wrap;
  }

  .acorn-count {
    margin-left: 0;
    margin-top: 10px;
  }

  .floating-squirrel {
    bottom: 20px;
    right: 20px;
  }

  .floating-squirrel .squirrel {
    font-size: 2.5rem;
  }

  .modal-content {
    padding: 30px 20px;
  }
}

/* 다크 모드 지원 (선택사항) */
@media (prefers-color-scheme: dark) {
  .mypage-container {
    background: #1a1a1a;
  }

  .info-card,
  .product-card,
  .liked-card,
  .modal-content {
    background: #2a2a2a;
    color: #f0f0f0;
  }

  .user-name,
  .section-title,
  .product-title,
  .liked-title {
    color: #f0f0f0;
  }

  .label,
  .product-info,
  .liked-preview,
  .liked-footer {
    color: #b0b0b0;
  }

  .cute-input {
    background: #333;
    border-color: #444;
    color: #f0f0f0;
  }

  .cute-input:focus {
    background: #2a2a2a;
    border-color: #4CAF50;
  }
}
</style>