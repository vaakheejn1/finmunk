<!-- src/components/UserProfileModal.vue -->
<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-content">
      <button class="close-btn" @click="close">❌</button>

      <div v-if="user">
        <img :src="user.profile_image" alt="프로필" class="profile-img" v-if="user.profile_image">
        <h3>@{{ user.username }}</h3>
        <p>팔로워 {{ user.followers_count }}명 • 팔로잉 {{ user.followings_count }}명</p>

        <button @click="toggleFollow">
          {{ user.is_following ? '언팔로우' : '팔로우' }}
        </button>

        <h4>작성 글</h4>
        <ul>
          <li v-for="article in user.articles" :key="article.id">{{ article.title }}</li>
        </ul>

        <h4>작성 댓글</h4>
        <ul>
          <li v-for="comment in user.comments" :key="comment.id">{{ comment.content }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  userId: Number,
  show: Boolean
})
const emit = defineEmits(['close'])

const user = ref(null)

watch(() => props.userId, (newId) => {
  if (newId) {
    axios.get(`${import.meta.env.VITE_API_URL}/users/profile/${newId}/`)
      .then(res => user.value = res.data)
  }
})

const toggleFollow = () => {
  axios.post(`${import.meta.env.VITE_API_URL}/users/follow/${props.userId}/`)
    .then(() => {
      return axios.get(`${import.meta.env.VITE_API_URL}/users/profile/${props.userId}/`)
    })
    .then(res => {
      user.value = res.data
    })
}

const close = () => {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 20px;
  width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  border-radius: 12px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
}
.profile-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}
</style>
