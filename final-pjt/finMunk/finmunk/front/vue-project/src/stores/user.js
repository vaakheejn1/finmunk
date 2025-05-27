// 📁 src/stores/user.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)  // 이제 객체로 저장됨
  const person = ref('')
  const router = useRouter()

  // ✅ 회원가입
  const signUp = function ({ username, email, age, job, income, assets, password1, password2 }) {
    return axios({
      method: 'POST',
      url: `${import.meta.env.VITE_API_URL}/auth/registration/`,
      data: {
        username,
        email,
        age,
        job,
        income,
        assets,
        password1,
        password2,
      }
    })
    .then(() => {
      alert('회원가입 성공! 로그인 해주세요.')
      router.push({ name: 'Login' })
    })
    .catch((err) => {
      alert('회원가입 실패 😥')
      console.error(err)
    })
  }

 // ✅ 로그인
const logIn = function ({ username, password }) {
  return axios({
    method: 'POST',
    url: `${import.meta.env.VITE_API_URL}/auth/login/`,
    data: {
      username,
      password,
    }
  })
  .then((res) => {
    token.value = res.data.key
    person.value = username
    localStorage.setItem('token', token.value)
    axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
    return getUserProfile().then(() => {
      router.push({ name: 'Home' })
    })
  })
  .catch(err => {
    const res = err.response
    
    if (res?.status === 400) {
      const data = res.data
      
      // Django REST Framework의 일반적인 오류 응답 처리
      if (data.non_field_errors) {
        const errorMsg = data.non_field_errors[0]
        
        // 구체적인 오류 메시지 분류
        if (errorMsg.includes('Unable to log in') || errorMsg.includes('invalid credentials')) {
          alert('❌ 아이디 또는 비밀번호가 일치하지 않습니다.')
        } else if (errorMsg.includes('inactive')) {
          alert('❌ 비활성화된 계정입니다.')
        } else {
          alert(`❌ ${errorMsg}`)
        }
      } else if (data.username) {
        // username 필드 오류
        if (data.username[0].includes('required')) {
          alert('❌ 아이디를 입력해주세요.')
        } else {
          alert('❌ 존재하지 않는 아이디입니다.')
        }
      } else if (data.password) {
        // password 필드 오류
        if (data.password[0].includes('required')) {
          alert('❌ 비밀번호를 입력해주세요.')
        } else {
          alert('❌ 비밀번호가 일치하지 않습니다.')
        }
      } else {
        alert('❌ 로그인에 실패했습니다.')
      }
    } else if (res?.status === 401) {
      alert('❌ 아이디 또는 비밀번호가 일치하지 않습니다.')
    } else if (res?.status === 404) {
      alert('❌ 존재하지 않는 아이디입니다.')
    } else {
      alert('⚠️ 서버에 문제가 있거나 인터넷 연결을 확인해주세요.')
    }
    
    return Promise.reject(err)
  })
}
  // 사용자 정보 가져오기
  const getUserProfile = function () {
    return axios({
      method: 'GET',
      url: `${import.meta.env.VITE_API_URL}/users/profile/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res) => {
      user.value = res.data  // 이제 전체 객체를 저장
      console.log('사용자 정보:', res.data)
    })
     .catch(err => {
      console.error('사용자 정보 조회 실패:', err)
    })
  }
  
// 로그아웃
  const logOut = function () {
    token.value = ''
    user.value = null
    delete axios.defaults.headers.common['Authorization']
    router.push({ name: 'Home' })
  }
  return {
    token,
    user,
    signUp,
    logIn,
    logOut,
    getUserProfile,
  }
}, { persist: true })