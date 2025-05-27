import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'


// View import
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import RecommendView from '@/views/RecommendView.vue'
import CompareView from '@/views/CompareView.vue'
import MarketView from '@/views/MarketView.vue'
import VideoView from '@/views/VideoView.vue'
import VideoDetail from '../components/video/VideoDetail.vue'
import CommunityView from '@/views/CommunityView.vue'
import MypageView from '@/views/MypageView.vue'
import CommunityWriteView from '@/views/CommunityWriteView.vue'
import CommunityArticleView from '@/views/CommunityArticleView.vue'
import Bankmap from '@/views/BankMapView.vue'
import UserProfile from '@/components/community/UserProfileView.vue'




const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/signup', name: 'Signup', component: SignupView },
  { path: '/recommend', name: 'Recommend', component: RecommendView , meta: { requiresAuth: true } },
  { path: '/compare', name: 'Compare', component: CompareView , meta: { requiresAuth: true } },
  { path: '/market', name: 'Market', component: MarketView },
  { path: '/videos', name: 'Videos', component: VideoView , meta: { requiresAuth: true } },
  { path: '/community', name: 'Community', component: CommunityView }, 
  { path: '/community/write', name: 'CommunityWrite', component: CommunityWriteView, meta: { requiresAuth: true } },
  { path: '/mypage', name: 'MyPage', component: MypageView , meta: { requiresAuth: true } },
  // { path: '/community/:id', name: 'CommunityArticle', component: CommunityArticleView },
  { path: '/videos/detail/:videoId', name: 'video-detail', component: VideoDetail, props: true},
  { path: '/bankmap', name: 'Bankmap', component:Bankmap},
  { path: '/community/articles/:id', name: 'CommunityArticle', component: CommunityArticleView},
  { path: '/profile/:user_id', name: 'UserProfile', component: UserProfile},
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const store = useUserStore()

  // 로그인이 필요한 라우트인데 로그인 안 했으면
  if (to.meta.requiresAuth && !store.token) {
    alert('로그인이 필요한 서비스입니다!')
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
