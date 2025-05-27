<template>
    <div class="notification-popup">
      <div class="notification-header">
        <h4>🔔 알림</h4>
        <button @click="$emit('close')">❌</button>
      </div>
  
      <div v-if="notifications.length">
        <ul class="notification-list">
          <li
            v-for="noti in notifications"
            :key="noti.id"
            :class="{ unread: !noti.is_read }"
            @click="goTo(noti)"
          >
            <span>{{ noti.message }}</span>
            <small>{{ formatDate(noti.created_at) }}</small>
          </li>
        </ul>
      </div>
      <p v-else class="no-notification">알림이 없습니다.</p>
    </div>
  </template>
  
<script setup>
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  notifications: Array,
})
const emit = defineEmits(['close', 'show-profile'])  // 🆕 추가

const router = useRouter()
const userStore = useUserStore()

const goTo = (noti) => {
  // 읽음 처리
  if (!noti.is_read) {
    axios.post(
      `${import.meta.env.VITE_API_URL}/community/notifications/${noti.id}/read/`,
      {},
      {
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      }
    ).catch((err) => {
      console.error('알림 읽음 처리 실패:', err)
    })
  }

  // 🧠 프로필 알림이면 모달로 열기
  const profileMatch = noti.url.match(/^\/profile\/(\d+)\/?$/)
  if (profileMatch) {
    const userId = Number(profileMatch[1])
    emit('show-profile', userId)  // 모달 오픈 요청
    emit('close')  // 팝업 닫기
    return
  }

  // 그 외는 라우터 이동
  if (noti.url) {
    router.push(noti.url)
    emit('close')
  }
}

const formatDate = (datetime) => {
  return new Date(datetime).toLocaleString()
}
</script>
  
  <style scoped>
  .notification-popup {
    position: absolute;
    top: 60px;
    right: 20px;
    width: 300px;
    max-height: 400px;
    background: white;
    border: 1px solid #ddd;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow-y: auto;
    z-index: 1000;
  }
  
  .notification-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #eee;
    background-color: #f8f8f8;
  }
  
  .notification-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .notification-list li {
    padding: 10px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background 0.2s;
  }
  
  .notification-list li:hover {
    background: #f0f0f0;
  }
  
  .notification-list li.unread {
    font-weight: bold;
    background: #e6f7ff;
  }
  
  .no-notification {
    padding: 20px;
    text-align: center;
    color: #888;
  }
  </style>
  