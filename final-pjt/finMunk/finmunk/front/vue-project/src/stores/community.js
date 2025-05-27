import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'

export const useCommunityStore = defineStore('community', () => {
  const articles = ref([])         // 게시글 목록
  const selectedArticle = ref(null) // 현재 보고 있는 게시글
  const comments = ref([])         // 댓글 목록

  const userStore = useUserStore()

  // 게시글 전체 조회
  const loadArticles = function (category = '') {
    let url = `${import.meta.env.VITE_API_URL}/community/articles/`
    if (category) {
      url += `?category=${category}`
    }
  
    axios({
      method: 'GET',
      url: url,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then(function (res) {
      articles.value = res.data
    })
    .catch(function (err) {
      console.error('게시글 목록 조회 실패:', err)
    })
  }

  // 게시글 하나 조회
  const loadArticle = function (articleId) {
    axios({
      method: 'GET',
      url: `${import.meta.env.VITE_API_URL}/community/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then(function (res) {
      selectedArticle.value = res.data
    })
    .catch(function (err) {
      console.error('게시글 상세 조회 실패:', err)
    })
  }

  // 게시글 삭제
  const deleteArticle = function (articleId, callback) {
    axios({
      method: 'DELETE',
      url: `${import.meta.env.VITE_API_URL}/community/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then(function () {
      if (callback) callback()
    })
    .catch(function (err) {
      alert('삭제 실패')
      console.error(err)
    })
  }

  // 댓글 불러오기
  const loadComments = function (articleId) {
    axios({
      method: 'GET',
      url: `${import.meta.env.VITE_API_URL}/community/comments/?article=${articleId}`
    })
    .then(function (res) {
      comments.value = res.data
    })
    .catch(function (err) {
      console.error('댓글 불러오기 실패:', err)
    })
  }


  // 댓글 작성
const createComment = function (articleId, content, callback) {
  // if (!content.trim()) return
  if (!content) return

  axios({
    method: 'POST',
    url: `${import.meta.env.VITE_API_URL}/community/comments/`,
    data: {
      content: content,
      article: articleId
    },
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
  .then(function () {
    if (callback) callback()
  })
  .catch(function (err) {
    alert('댓글 작성 실패')
    console.error(err)
  })
}

// 댓글 수정
const updateComment = function (commentId,  articleId, content,callback) {
  if (!content) return
  // if (!content.trim()) return

  axios({
    method: 'PUT',
    url: `${import.meta.env.VITE_API_URL}/community/comments/${commentId}/`,
    data: {
      content: content,
      article: Number(articleId)
    },
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
  .then(function () {
    if (callback) callback()
  })
  .catch(function (err) {
    alert('댓글 수정 실패')
    console.error(err)
  })
}

// 댓글 삭제
const deleteComment = function (commentId, callback) {
  axios({
    method: 'DELETE',
    url: `${import.meta.env.VITE_API_URL}/community/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
  .then(function () {
    if (callback) callback()
  })
  .catch(function (err) {
    alert('댓글 삭제 실패')
    console.error(err)
  })
}

  return {
    articles,
    selectedArticle,
    comments,
    loadArticles,
    loadArticle,
    deleteArticle,
    loadComments,
    createComment,
    updateComment,
    deleteComment,
  }
  
},
{persist:true})
