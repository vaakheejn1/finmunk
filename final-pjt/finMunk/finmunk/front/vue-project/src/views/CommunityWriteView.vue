<template>
  <div class="write-container">
    <!-- 배경 장식 -->
    <div class="bg-decoration">
      <span class="floating-acorn" v-for="n in 5" :key="n">🌰</span>
    </div>

    <!-- 헤더 -->
    <header class="write-header">
      <h1 class="page-title">
        <span class="title-icon wiggle">{{ isEditMode ? '📝' : '✍️' }}</span>
        {{ isEditMode ? '글 수정하기' : '새 글 쓰기' }}
        <span class="squirrel-helper bounce">🐿️</span>
      </h1>
      <p class="page-subtitle">
        {{ isEditMode ? '내용을 수정해주세요' : '다람쥐들과 나누고 싶은 이야기를 적어주세요!' }}
      </p>
    </header>

    <!-- 작성 폼 -->
    <form @submit.prevent="submitArticle" class="write-form">
      <!-- 카테고리 선택 -->
      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">📂</span>
          카테고리
        </label>
        <div class="category-select-wrapper">
          <select v-model="category" class="category-select">
            <option value="notice">📢 공지사항</option>
            <option value="event">🎉 이벤트</option>
            <option value="tip">💡 자유게시판</option>
          </select>
          <span class="select-arrow">▼</span>
        </div>
      </div>

      <!-- 제목 입력 -->
      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">📌</span>
          제목
        </label>
        <input 
          v-model="title" 
          type="text"
          placeholder="어떤 이야기를 나누고 싶으신가요?" 
          class="form-input title-input"
          required
        />
        <div class="input-decoration">
          <span class="deco-leaf">🍃</span>
        </div>
      </div>

      <!-- 내용 입력 -->
      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">📝</span>
          내용
        </label>
        <div class="textarea-wrapper">
          <textarea 
            v-model="content" 
            placeholder="자유롭게 이야기를 들려주세요! 다람쥐들이 기다리고 있어요 🐿️" 
            class="form-textarea"
            rows="10"
            required
          ></textarea>
          <div class="char-count">
            <span>{{ content.length }}</span> / 5000
          </div>
        </div>
      </div>

      <!-- 이미지 업로드 -->
      <div class="form-group">
        <label class="form-label">
          <span class="label-icon">🖼️</span>
          이미지 업로드
        </label>
        
        <div class="file-upload-area">
          <input 
            type="file" 
            @change="onFileChange" 
            accept="image/*"
            id="file-input"
            class="file-input"
          />
          <label for="file-input" class="file-label">
            <div class="upload-content">
              <span class="upload-icon">📸</span>
              <span class="upload-text">이미지를 선택해주세요</span>
              <span class="upload-hint">최대 10MB (JPG, PNG, GIF)</span>
            </div>
          </label>
        </div>

        <!-- 이미지 미리보기 -->
        <div v-if="previewUrl" class="image-preview">
          <div class="preview-header">
            <span>미리보기</span>
            <button type="button" @click="removeImage" class="remove-btn">❌</button>
          </div>
          <img :src="previewUrl" alt="미리보기" class="preview-image" />
        </div>
      </div>

      <!-- 버튼 그룹 -->
      <div class="button-group">
        <RouterLink to="/community" class="cancel-btn">
          <span>🔙</span>
          취소
        </RouterLink>
        <button type="submit" class="submit-btn" :disabled="!title || !content">
          <span class="btn-icon">{{ isEditMode ? '✏️' : '💾' }}</span>
          {{ isEditMode ? '수정하기' : '저장하기' }}
        </button>
      </div>
    </form>

    <!-- 도움말 -->
    <div class="help-section">
      <h3>
        <span class="help-icon">💡</span>
        작성 팁
      </h3>
      <ul class="help-list">
        <li>
          <span class="list-icon">🌰</span>
          친절하고 따뜻한 말투로 작성해주세요
        </li>
        <li>
          <span class="list-icon">🌰</span>
          유용한 정보는 다른 다람쥐들도 좋아해요
        </li>
        <li>
          <span class="list-icon">🌰</span>
          이미지를 추가하면 더 생생한 이야기가 돼요
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const isEditMode = ref(false)
const articleId = route.query.id

const title = ref('')
const content = ref('')
const category = ref('tip')
const imageFile = ref(null)
const previewUrl = ref(null)

// 이미지 변경 시 미리보기 URL 업데이트
watch(imageFile, (newFile) => {
  if (newFile) {
    // 이전 URL revoke (메모리 해제)
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value)
    }
    previewUrl.value = URL.createObjectURL(newFile)
  } else {
    previewUrl.value = null
  }
})

// 이미지 선택 시 파일 저장
const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file && file.size <= 10 * 1024 * 1024) { // 10MB 제한
    imageFile.value = file
  } else {
    alert('이미지는 10MB 이하만 업로드 가능해요!')
    e.target.value = ''
  }
}

// 이미지 제거
const removeImage = () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
  }
  imageFile.value = null
  const fileInput = document.getElementById('file-input')
  if (fileInput) fileInput.value = ''
}

// 수정 모드일 때 기존 데이터 로드
if (articleId) {
  isEditMode.value = true
  axios({
    method: 'GET',
    url: `${import.meta.env.VITE_API_URL}/community/articles/${articleId}/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
  .then((res) => {
    title.value = res.data.title
    content.value = res.data.content
    category.value = res.data.category || 'tip'
    previewUrl.value = res.data.image
  })
  .catch((err) => {
    console.error(err)
    alert('게시글을 불러올 수 없어요 😢')
    router.push({ name: 'Community' })
  })
}

// 저장 요청
const submitArticle = () => {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  formData.append('category', category.value)
  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  const method = isEditMode.value ? 'PUT' : 'POST'
  const url = isEditMode.value
    ? `${import.meta.env.VITE_API_URL}/community/articles/${articleId}/`
    : `${import.meta.env.VITE_API_URL}/community/articles/`

  axios({
    method: method,
    url: url,
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Token ${userStore.token}`
    }
  })
  .then(() => {
    alert(isEditMode.value ? '수정 완료! 🐿️' : '작성 완료! 🐿️')
    router.push({ name: 'Community' })
  })
  .catch((err) => {
    alert(isEditMode.value ? '수정 실패 😢' : '작성 실패 😢')
    console.error(err)
  })
}
</script>

<style scoped>
/* 기본 컨테이너 */
.write-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  position: relative;
}

/* 배경 장식 */
.bg-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
}

.floating-acorn {
  position: absolute;
  font-size: 2.5rem;
  opacity: 0.08;
  animation: float 20s infinite ease-in-out;
}

.floating-acorn:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.floating-acorn:nth-child(2) { top: 20%; left: 80%; animation-delay: 4s; }
.floating-acorn:nth-child(3) { top: 50%; left: 20%; animation-delay: 8s; }
.floating-acorn:nth-child(4) { top: 70%; left: 70%; animation-delay: 12s; }
.floating-acorn:nth-child(5) { top: 30%; left: 50%; animation-delay: 16s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(180deg); }
}

/* 헤더 */
.write-header {
  text-align: center;
  margin-bottom: 40px;
  animation: fadeInDown 0.6s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.title-icon {
  display: inline-block;
  font-size: 2.5rem;
}

.squirrel-helper {
  display: inline-block;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 50%;
  padding: 5px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
}

/* 작성 폼 */
.write-form {
  background: white;
  border-radius: 30px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.6s ease-out 0.2s backwards;
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

/* 폼 그룹 */
.form-group {
  margin-bottom: 30px;
  position: relative;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-icon {
  font-size: 1.3rem;
}

/* 카테고리 선택 */
.category-select-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
}

.category-select {
  width: 100%;
  padding: 15px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  font-size: 1rem;
  background: #f8f8f8;
  cursor: pointer;
  appearance: none;
  transition: all 0.3s;
}

.category-select:hover,
.category-select:focus {
  border-color: #4CAF50;
  background: white;
  outline: none;
}

.select-arrow {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  pointer-events: none;
}

/* 입력 필드 */
.form-input,
.form-textarea {
  width: 100%;
  padding: 15px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #f8f8f8;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #4CAF50;
  background: white;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.title-input {
  font-weight: 600;
  font-size: 1.1rem;
}

.input-decoration {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.deco-leaf {
  font-size: 1.5rem;
  animation: sway 3s infinite ease-in-out;
}

@keyframes sway {
  0%, 100% { transform: rotate(-5deg); }
  50% { transform: rotate(5deg); }
}

/* 텍스트 영역 래퍼 */
.textarea-wrapper {
  position: relative;
}

.char-count {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-size: 0.9rem;
  color: #999;
}

/* 파일 업로드 */
.file-upload-area {
  position: relative;
  overflow: hidden;
}

.file-input {
  display: none;
}

.file-label {
  display: block;
  border: 2px dashed #4CAF50;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #f8fff8;
}

.file-label:hover {
  background: #e8f5e9;
  border-color: #45a049;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.upload-icon {
  font-size: 3rem;
}

.upload-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.upload-hint {
  font-size: 0.9rem;
  color: #666;
}

/* 이미지 미리보기 */
.image-preview {
  margin-top: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  overflow: hidden;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f8f8f8;
  border-bottom: 1px solid #e0e0e0;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  transition: transform 0.3s;
}

.remove-btn:hover {
  transform: scale(1.2);
}

.preview-image {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  display: block;
}

/* 버튼 그룹 */
.button-group {
  display: flex;
  gap: 15px;
  margin-top: 40px;
  justify-content: center;
}

.cancel-btn,
.submit-btn {
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: none;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.submit-btn {
  background: #4CAF50;
  color: white;
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
}

.submit-btn:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(76, 175, 80, 0.4);
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-icon {
  font-size: 1.2rem;
}

/* 도움말 섹션 */
.help-section {
  background: #f8f8f8;
  border-radius: 20px;
  padding: 30px;
  margin-top: 30px;
  animation: fadeIn 0.6s ease-out 0.4s backwards;
}

.help-section h3 {
  font-size: 1.3rem;
  color: #333;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.help-icon {
  font-size: 1.5rem;
}

.help-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.help-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
  font-size: 1rem;
}

.list-icon {
  font-size: 1.2rem;
}

/* 애니메이션 클래스 */
.wiggle {
  animation: wiggle 2s infinite;
}

@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

.bounce {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .write-container {
    padding: 10px;
  }

  .write-header {
    margin-bottom: 25px;
  }

  .page-title {
    font-size: 1.8rem;
  }

  .write-form {
    padding: 25px 20px;
    border-radius: 20px;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .file-label {
    padding: 30px 20px;
  }

  .upload-icon {
    font-size: 2.5rem;
  }

  .button-group {
    flex-direction: column;
    width: 100%;
  }

  .cancel-btn,
  .submit-btn {
    width: 100%;
    justify-content: center;
  }

  .help-section {
    padding: 20px;
  }
}

/* 다크 모드 */
@media (prefers-color-scheme: dark) {
  .write-container {
    background: #1a1a1a;
  }

  .write-form,
  .help-section {
    background: #2a2a2a;
    color: #f0f0f0;
  }

  .form-label {
    color: #f0f0f0;
  }

  .form-input,
  .form-textarea,
  .category-select {
    background: #333;
    border-color: #444;
    color: #f0f0f0;
  }

  .form-input:focus,
  .form-textarea:focus,
  .category-select:focus {
    background: #2a2a2a;
    border-color: #4CAF50;
  }

  .file-label {
    background: #1a1a1a;
    border-color: #4CAF50;
  }

  .file-label:hover {
    background: #2a2a2a;
  }

  .upload-text {
    color: #f0f0f0;
  }

  .cancel-btn {
    background: #333;
    color: #f0f0f0;
  }

  .cancel-btn:hover {
    background: #444;
  }
}
</style>