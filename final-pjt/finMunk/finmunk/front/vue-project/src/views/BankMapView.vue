<template>
    <div class="bank-finder">
      <!-- 페이지 헤더 -->
      <div class="page-header">
        <div class="header-icon">
          <i class="fas fa-university"></i>
        </div>
        <div class="header-content">
          <h1 class="page-title">🏦 은행 찾기</h1>
          <p class="page-subtitle">가까운 은행을 찾아보세요</p>
        </div>
      </div>
  
      <!-- 검색 필터 -->
      <div class="search-filters">
        <div class="filter-group">
          <label class="filter-label">광역시/도</label>
          <select v-model="selectedSido" @change="onSidoChange" class="filter-select">
            <option value="">광역시/도 선택</option>
            <option v-for="sido in sidoList" :key="sido" :value="sido">{{ sido }}</option>
          </select>
        </div>
  
        <div class="filter-group">
          <label class="filter-label">시/군/구</label>
          <select v-model="selectedSigungu" :disabled="!selectedSido" class="filter-select">
            <option value="">시/군/구 선택</option>
            <option v-for="sigungu in sigunguList" :key="sigungu" :value="sigungu">{{ sigungu }}</option>
          </select>
        </div>
  
        <div class="filter-group">
          <label class="filter-label">은행</label>
          <select v-model="selectedBank" class="filter-select">
            <option value="">은행 선택</option>
            <option v-for="bank in bankList" :key="bank" :value="bank">{{ bank }}</option>
          </select>
        </div>
  
        <button 
          @click="searchBanks" 
          :disabled="!canSearch"
          class="search-btn"
        >
          <i class="fas fa-search"></i>
          지도에서 찾기
        </button>
      </div>
  
      <!-- 메인 콘텐츠 -->
      <div class="main-content">
        <!-- 지도 영역 -->
        <div class="map-container">
          <div id="kakaoMap" class="map"></div>
          <div v-if="isLoading" class="map-loading">
            <div class="loading-spinner"></div>
            <p>은행을 검색하고 있습니다...</p>
          </div>
        </div>
  
        <!-- 사이드바 -->
        <div class="sidebar">
          <!-- 탭 네비게이션 -->
          <div class="tab-nav">
            <button 
              @click="activeTab = 'list'"
              :class="['tab-button', { active: activeTab === 'list' }]"
            >
              <i class="fas fa-list"></i>
              검색 결과
            </button>
            <button 
              @click="activeTab = 'detail'"
              :class="['tab-button', { active: activeTab === 'detail' }]"
            >
              <i class="fas fa-info-circle"></i>
              상세 정보
            </button>
          </div>
  
          <!-- 탭 콘텐츠 -->
          <div class="tab-content">
            <!-- 검색 결과 탭 -->
            <div v-if="activeTab === 'list'" class="tab-pane">
              <div class="search-info" v-if="searchKeyword">
                <h3>검색 결과</h3>
                <div class="search-summary">
                  <p><strong>검색어:</strong> {{ searchKeyword }}</p>
                  <p><strong>결과:</strong> {{ bankData.length }}개 은행</p>
                </div>
              </div>
  
              <div v-if="!hasSearched" class="initial-message">
                <div class="message-icon">🏦</div>
                <h4>검색 조건을 설정하세요</h4>
                <p>광역시/도, 시/군/구, 은행을 선택하고<br>'지도에서 찾기' 버튼을 클릭하세요</p>
              </div>
  
              <div v-else-if="bankData.length === 0" class="no-results">
                <div class="no-results-icon">🔍</div>
                <h4>검색 결과가 없습니다</h4>
                <p>다른 조건으로 다시 검색해보세요</p>
              </div>
  
              <div v-else class="bank-list">
                <div 
                  v-for="(bank, index) in bankData" 
                  :key="bank.id"
                  @click="selectBank(bank, index)"
                  :class="['bank-item', { active: selectedBankIndex === index }]"
                >
                  <div class="bank-header">
                    <h4 class="bank-name">{{ bank.place_name }}</h4>
                    <span class="bank-category">{{ getBankCategory(bank.place_name) }}</span>
                  </div>
                  <p class="bank-address">{{ bank.address_name }}</p>
                  <div class="bank-meta">
                    <span v-if="bank.phone" class="bank-phone">
                      <i class="fas fa-phone"></i>
                      {{ bank.phone }}
                    </span>
                    <span class="bank-distance">
                      <i class="fas fa-map-marker-alt"></i>
                      {{ formatDistance(bank.distance) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- 상세 정보 탭 -->
            <div v-if="activeTab === 'detail'" class="tab-pane">
              <div v-if="!selectedBankData" class="no-selection">
                <div class="selection-icon">📍</div>
                <h4>은행을 선택하세요</h4>
                <p>목록에서 은행을 선택하시면<br>상세 정보를 확인할 수 있습니다</p>
              </div>
  
              <div v-else class="detail-view">
                <div class="detail-header">
                  <h3>{{ selectedBankData.place_name }}</h3>
                  <span class="detail-category">{{ selectedBankData.category_name || '은행/금융' }}</span>
                </div>
  
                <div class="detail-sections">
                  <!-- 위치 정보 -->
                  <div class="detail-section">
                    <h4><i class="fas fa-map-marker-alt"></i> 위치 정보</h4>
                    <div class="detail-item">
                      <span class="item-label">주소</span>
                      <span class="item-value">{{ selectedBankData.address_name }}</span>
                    </div>
                    <div v-if="selectedBankData.road_address_name" class="detail-item">
                      <span class="item-label">도로명</span>
                      <span class="item-value">{{ selectedBankData.road_address_name }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="item-label">거리</span>
                      <span class="item-value">{{ formatDistance(selectedBankData.distance) }}</span>
                    </div>
                  </div>
  
                  <!-- 연락처 정보 -->
                  <div v-if="selectedBankData.phone" class="detail-section">
                    <h4><i class="fas fa-phone"></i> 연락처</h4>
                    <div class="detail-item">
                      <span class="item-label">전화번호</span>
                      <span class="item-value">{{ selectedBankData.phone }}</span>
                    </div>
                  </div>
  
                  <!-- 영업 시간 -->
                  <div class="detail-section">
                    <h4><i class="fas fa-clock"></i> 영업 시간</h4>
                    <div class="detail-item">
                      <span class="item-label">평일</span>
                      <span class="item-value">{{ getBankInfo(selectedBankData.place_name).businessHours }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="item-label">토요일</span>
                      <span class="item-value">{{ getBankInfo(selectedBankData.place_name).saturdayHours }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="item-label">일요일</span>
                      <span class="item-value">{{ getBankInfo(selectedBankData.place_name).sundayHours }}</span>
                    </div>
                  </div>
  
                  <!-- 서비스 정보 -->
                  <div class="detail-section">
                    <h4><i class="fas fa-university"></i> 서비스</h4>
                    <div class="detail-item">
                      <span class="item-label">제공 서비스</span>
                      <span class="item-value">{{ getBankInfo(selectedBankData.place_name).services }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="item-label">주차</span>
                      <span class="item-value">{{ getBankInfo(selectedBankData.place_name).parking }}</span>
                    </div>
                  </div>
                </div>
  
                <!-- 액션 버튼들 -->
                <div class="action-buttons">
                  <button @click="focusOnMap" class="action-btn primary">
                    <i class="fas fa-map"></i>
                    지도에서 보기
                  </button>
                  <button v-if="selectedBankData.phone" @click="callBank" class="action-btn secondary">
                    <i class="fas fa-phone"></i>
                    전화걸기
                  </button>
                </div>
  
                <div class="action-buttons">
                  <button @click="openKakaoMap" class="action-btn secondary">
                    <i class="fas fa-external-link-alt"></i>
                    카카오맵에서 보기
                  </button>
                  <button @click="getDirections" class="action-btn secondary">
                    <i class="fas fa-route"></i>
                    길찾기
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- 토스트 메시지 -->
      <div v-if="showToast" class="toast" :class="toastType">
        <i class="fas" :class="getToastIcon()"></i>
        {{ toastMessage }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, nextTick } from 'vue'
  
  // 반응형 상태
  const selectedSido = ref('')
  const selectedSigungu = ref('')
  const selectedBank = ref('')
  const activeTab = ref('list')
  const bankData = ref([])
  const selectedBankData = ref(null)
  const selectedBankIndex = ref(-1)
  const hasSearched = ref(false)
  const isLoading = ref(false)
  const searchKeyword = ref('')
  const showToast = ref(false)
  const toastMessage = ref('')
  const toastType = ref('success')
  
  // 카카오맵 관련
  let map = null
  let ps = null
  let infowindow = null
  let markers = []
  
  // 지역 데이터
  const sigunguData = {
    "서울특별시": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "부산광역시": ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
    "대구광역시": ["남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구"],
    "인천광역시": ["강화군", "계양구", "남동구", "동구", "미추홀구", "부평구", "서구", "연수구", "옹진군", "중구"],
    "광주광역시": ["광산구", "남구", "동구", "북구", "서구"],
    "대전광역시": ["대덕구", "동구", "서구", "유성구", "중구"],
    "울산광역시": ["남구", "동구", "북구", "중구", "울주군"],
    "세종특별자치시": ["세종시"],
    "경기도": ["고양시", "수원시", "성남시", "용인시", "부천시", "안산시", "안양시", "남양주시", "화성시", "평택시", "의정부시", "시흥시", "파주시", "김포시", "광명시", "광주시", "군포시", "오산시", "이천시", "안성시", "의왕시", "하남시", "여주시", "양평군", "동두천시", "과천시", "가평군", "연천군"],
    "강원특별자치도": ["강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"],
    "충청북도": ["괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "진천군", "청주시", "충주시"],
    "충청남도": ["계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "예산군", "천안시", "청양군", "태안군", "홍성군"],
    "전라북도": ["고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시", "정읍시", "진안군"],
    "전라남도": ["강진군", "고흥군", "곡성군", "광양시", "구례군", "나주시", "담양군", "목포시", "무안군", "보성군", "순천시", "신안군", "여수시", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"],
    "경상북도": ["경산시", "경주시", "고령군", "구미시", "군위군", "김천시", "문경시", "봉화군", "상주시", "성주군", "안동시", "영덕군", "영양군", "영주시", "영천시", "예천군", "울릉군", "울진군", "의성군", "청도군", "청송군", "칠곡군", "포항시"],
    "경상남도": ["거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "진주시", "창녕군", "창원시", "통영시", "하동군", "함안군", "함양군", "합천군"],
    "제주특별자치도": ["서귀포시", "제주시"]
  }
  
  const sidoList = Object.keys(sigunguData)
  const bankList = ["KB국민은행", "신한은행", "우리은행", "하나은행", "NH농협은행", "IBK기업은행", "SC제일은행", "씨티은행", "카카오뱅크", "케이뱅크", "토스뱅크", "대구은행", "부산은행", "광주은행", "전북은행", "제주은행", "경남은행", "수협은행", "새마을금고", "신협"]
  
  // 계산된 속성
  const sigunguList = computed(() => {
    return selectedSido.value ? sigunguData[selectedSido.value] || [] : []
  })
  
  const canSearch = computed(() => {
    return selectedSido.value && selectedSigungu.value && selectedBank.value
  })
  
  // 메서드
  const onSidoChange = () => {
    selectedSigungu.value = ''
  }
  
  const initKakaoMap = () => {
    if (!window.kakao || !window.kakao.maps) {
      console.error('카카오맵 API가 로드되지 않았습니다')
      showToastMessage('카카오맵을 불러올 수 없습니다', 'error')
      return false
    }
  
    try {
      const container = document.getElementById('kakaoMap')
      if (!container) {
        console.error('지도 컨테이너를 찾을 수 없습니다')
        return false
      }
  
      const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 5
      }
      
      map = new kakao.maps.Map(container, options)
      ps = new kakao.maps.services.Places()
      infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
      
      console.log('카카오맵 초기화 완료')
      return true
    } catch (error) {
      console.error('카카오맵 초기화 실패:', error)
      showToastMessage('지도 초기화에 실패했습니다', 'error')
      return false
    }
  }
  
  const searchBanks = () => {
    if (!canSearch.value) {
      showToastMessage('모든 항목을 선택해주세요', 'warning')
      return
    }
  
    if (!ps) {
      showToastMessage('지도 서비스를 초기화할 수 없습니다', 'error')
      return
    }
  
    const keyword = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`
    searchKeyword.value = keyword
    hasSearched.value = true
    isLoading.value = true
  
    console.log('🔍 검색 키워드:', keyword)
  
    // 이전 마커 제거
    clearMarkers()
  
    try {
      ps.keywordSearch(keyword, (data, status) => {
        isLoading.value = false
        
        console.log('검색 상태:', status)
        console.log('검색 결과:', data)
        
        if (status === kakao.maps.services.Status.OK) {
          if (data && data.length > 0) {
            bankData.value = data.map((place, index) => ({
              ...place,
              id: place.id || `bank_${index}`,
              distance: 0 // 거리는 실제 계산으로 대체 가능
            }))
            
            displayMarkers(data)
            showToastMessage(`${data.length}개의 은행을 찾았습니다`, 'success')
          } else {
            bankData.value = []
            showToastMessage('검색 결과가 없습니다', 'info')
          }
        } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
          bankData.value = []
          showToastMessage('검색 결과가 없습니다', 'info')
        } else if (status === kakao.maps.services.Status.ERROR) {
          bankData.value = []
          showToastMessage('검색 중 오류가 발생했습니다', 'error')
        } else {
          bankData.value = []
          showToastMessage('알 수 없는 오류가 발생했습니다', 'error')
        }
      }, {
        size: 15,
        page: 1
      })
    } catch (error) {
      isLoading.value = false
      console.error('검색 실행 오류:', error)
      showToastMessage('검색 실행 중 오류가 발생했습니다', 'error')
    }
  }
  
  const clearMarkers = () => {
    try {
      markers.forEach(marker => {
        if (marker && marker.setMap) {
          marker.setMap(null)
        }
      })
      markers = []
      if (infowindow && infowindow.close) {
        infowindow.close()
      }
    } catch (error) {
      console.error('마커 제거 오류:', error)
    }
  }
  
  const displayMarkers = (places) => {
    if (!map || !kakao || !kakao.maps) {
      console.error('지도가 초기화되지 않았습니다')
      return
    }
  
    try {
      const bounds = new kakao.maps.LatLngBounds()
  
      places.forEach((place, index) => {
        const position = new kakao.maps.LatLng(place.y, place.x)
        const marker = new kakao.maps.Marker({
          map: map,
          position: position
        })
  
        kakao.maps.event.addListener(marker, 'click', () => {
          selectBank(place, index)
          
          if (infowindow) {
            infowindow.setContent(`
              <div style="padding:10px;font-size:14px;max-width:300px;line-height:1.5">
                <strong>${place.place_name}</strong><br>
                <span style="color:#777;font-size:12px">${place.address_name}</span><br>
                ${place.phone ? `<span style="color:#4DD0B1;font-size:13px">${place.phone}</span>` : ''}
              </div>
            `)
            infowindow.open(map, marker)
          }
        })
  
        markers.push(marker)
        bounds.extend(position)
      })
  
      map.setBounds(bounds)
    } catch (error) {
      console.error('마커 표시 오류:', error)
      showToastMessage('지도에 마커를 표시할 수 없습니다', 'error')
    }
  }
  
  const selectBank = (bank, index) => {
    selectedBankData.value = bank
    selectedBankIndex.value = index
    
    // 지도 중심 이동
    if (map) {
      try {
        const position = new kakao.maps.LatLng(bank.y, bank.x)
        map.setCenter(position)
        map.setLevel(3)
  
        // 정보창 표시
        if (markers[index] && infowindow) {
          infowindow.setContent(`
            <div style="padding:10px;font-size:14px;max-width:300px;line-height:1.5">
              <strong>${bank.place_name}</strong><br>
              <span style="color:#777;font-size:12px">${bank.address_name}</span><br>
              ${bank.phone ? `<span style="color:#4DD0B1;font-size:13px">${bank.phone}</span>` : ''}
            </div>
          `)
          infowindow.open(map, markers[index])
        }
      } catch (error) {
        console.error('지도 이동 오류:', error)
      }
    }
  }
  
  const focusOnMap = () => {
    if (selectedBankData.value && map) {
      try {
        const position = new kakao.maps.LatLng(selectedBankData.value.y, selectedBankData.value.x)
        map.setCenter(position)
        map.setLevel(2)
        activeTab.value = 'list'
      } catch (error) {
        console.error('지도 포커스 오류:', error)
        showToastMessage('지도 이동 중 오류가 발생했습니다', 'error')
      }
    }
  }
  
  const callBank = () => {
    if (selectedBankData.value?.phone) {
      window.location.href = `tel:${selectedBankData.value.phone}`
    }
  }
  
  const openKakaoMap = () => {
    if (selectedBankData.value) {
      const url = `https://map.kakao.com/link/map/${selectedBankData.value.place_name},${selectedBankData.value.y},${selectedBankData.value.x}`
      window.open(url, '_blank')
    }
  }
  
  const getDirections = () => {
    if (selectedBankData.value) {
      const url = `https://map.kakao.com/link/to/${selectedBankData.value.place_name},${selectedBankData.value.y},${selectedBankData.value.x}`
      window.open(url, '_blank')
    }
  }
  
  const getBankCategory = (placeName) => {
    const name = placeName.toLowerCase()
    if (name.includes('atm') || name.includes('현금자동입출금기')) return 'ATM'
    if (name.includes('kb') || name.includes('국민')) return '시중은행'
    if (name.includes('신한') || name.includes('우리') || name.includes('하나')) return '시중은행'
    if (name.includes('농협') || name.includes('기업')) return '특수은행'
    if (name.includes('카카오') || name.includes('케이뱅크') || name.includes('토스')) return '인터넷은행'
    if (name.includes('대구') || name.includes('부산') || name.includes('광주')) return '지방은행'
    return '은행'
  }
  
  const getBankInfo = (placeName) => {
    const bankName = placeName.toLowerCase()
    
    if (bankName.includes('atm') || bankName.includes('현금자동입출금기')) {
      return {
        businessHours: '24시간 운영',
        saturdayHours: '24시간 운영',
        sundayHours: '24시간 운영',
        parking: 'ATM',
        services: '현금입출금, 이체'
      }
    }
    
    let defaultInfo = {
      businessHours: '평일 09:00 - 16:00',
      saturdayHours: '토요일 휴무',
      sundayHours: '일요일 휴무',
      parking: '주차 가능',
      services: '예금, 대출, 환전, 상담'
    }
    
    if (bankName.includes('kb') || bankName.includes('국민')) {
      defaultInfo.saturdayHours = '토요일 09:00 - 13:00'
      defaultInfo.services = '예금, 대출, 환전, 보험, 투자상품'
    } else if (bankName.includes('신한')) {
      defaultInfo.saturdayHours = '토요일 09:00 - 13:00'
      defaultInfo.services = '예금, 대출, 환전, 보험, 카드발급'
    } else if (bankName.includes('카카오뱅크') || bankName.includes('케이뱅크') || bankName.includes('토스뱅크')) {
      defaultInfo = {
        businessHours: '온라인 전용 (24시간)',
        saturdayHours: '온라인 전용 (24시간)',
        sundayHours: '온라인 전용 (24시간)',
        parking: '매장 없음',
        services: '온라인 뱅킹 전용'
      }
    }
    
    return defaultInfo
  }
  
  const formatDistance = (distance) => {
    if (!distance) return '-'
    if (distance < 1000) return `${Math.round(distance)}m`
    return `${(distance / 1000).toFixed(1)}km`
  }
  
  const showToastMessage = (message, type = 'success') => {
    toastMessage.value = message
    toastType.value = type
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
  }
  
  const getToastIcon = () => {
    switch (toastType.value) {
      case 'success': return 'fa-check-circle'
      case 'warning': return 'fa-exclamation-triangle'
      case 'error': return 'fa-exclamation-circle'
      case 'info': return 'fa-info-circle'
      default: return 'fa-check-circle'
    }
  }
  
  // 라이프사이클
  onMounted(() => {
    console.log('컴포넌트 마운트됨')
    
    // 카카오맵 API 로드 확인 후 초기화
    const checkKakaoMap = () => {
      if (window.kakao && window.kakao.maps) {
        console.log('카카오맵 API 로드 확인됨')
        nextTick(() => {
          const success = initKakaoMap()
          if (!success) {
            setTimeout(checkKakaoMap, 500) // 실패시 재시도
          }
        })
      } else {
        console.log('카카오맵 API 로딩 중...')
      }
    }
    
    // 지도 컨테이너가 준비될 때까지 대기
    nextTick(() => {
      setTimeout(checkKakaoMap, 200)
    })
  })
  </script>
  
  <style scoped>
  .bank-finder {
    max-width: 1400px;
    margin: 0 auto;
    padding: 32px 20px;
    min-height: 100vh;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  }
  
  /* 페이지 헤더 */
  .page-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 40px;
    padding: 24px;
    background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
    border-radius: 20px;
    color: white;
    box-shadow: 0 8px 32px rgba(77, 208, 177, 0.3);
  }
  
  .header-icon {
    width: 64px;
    height: 64px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    backdrop-filter: blur(10px);
  }
  
  .header-content {
    flex: 1;
  }
  
  .page-title {
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 8px 0;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }
  
  .page-subtitle {
    font-size: 16px;
    margin: 0;
    opacity: 0.9;
    font-weight: 500;
  }
  
  /* 검색 필터 */
  .search-filters {
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
    padding: 24px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    animation: fadeInUp 0.6s ease-out;
  }
  
  .filter-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .filter-label {
    font-size: 14px;
    font-weight: 600;
    color: #374151;
  }
  
  .filter-select {
    padding: 12px 16px;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    font-size: 14px;
    background: white;
    transition: all 0.3s ease;
  }
  
  .filter-select:focus {
    outline: none;
    border-color: #4DD0B1;
    box-shadow: 0 0 0 3px rgba(77, 208, 177, 0.1);
  }
  
  .filter-select:disabled {
    background: #f9fafb;
    color: #9ca3af;
    cursor: not-allowed;
  }
  
  .search-btn {
    background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    align-self: flex-end;
    white-space: nowrap;
    box-shadow: 0 4px 16px rgba(77, 208, 177, 0.3);
  }
  
  .search-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(77, 208, 177, 0.4);
  }
  
  .search-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
  
  /* 메인 콘텐츠 */
  .main-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
    height: 600px;
  }
  
  /* 지도 영역 */
  .map-container {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    background: white;
  }
  
  .map {
    width: 100%;
    height: 100%;
  }
  
  .map-loading {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
  }
  
  .loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid #e5e7eb;
    border-top: 4px solid #4DD0B1;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .map-loading p {
    font-size: 16px;
    color: #6b7280;
    font-weight: 500;
    margin: 0;
  }
  
  /* 사이드바 */
  .sidebar {
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  /* 탭 네비게이션 */
  .tab-nav {
    display: flex;
    background: #f8f9fa;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .tab-button {
    flex: 1;
    padding: 16px 12px;
    border: none;
    background: none;
    cursor: pointer;
    font-weight: 600;
    color: #6b7280;
    transition: all 0.3s ease;
    border-bottom: 3px solid transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 14px;
  }
  
  .tab-button.active {
    color: #4DD0B1;
    border-bottom-color: #4DD0B1;
    background: white;
  }
  
  .tab-button:hover:not(.active) {
    background: #f1f5f9;
    color: #374151;
  }
  
  /* 탭 콘텐츠 */
  .tab-content {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
  }
  
  .tab-pane {
    height: 100%;
  }
  
  /* 검색 정보 */
  .search-info h3 {
    font-size: 18px;
    font-weight: 700;
    color: #1f2937;
    margin: 0 0 16px 0;
  }
  
  .search-summary {
    background: #f8fafc;
    padding: 12px 16px;
    border-radius: 8px;
    border-left: 4px solid #4DD0B1;
    margin-bottom: 20px;
  }
  
  .search-summary p {
    margin: 4px 0;
    font-size: 14px;
    color: #374151;
  }
  
  /* 초기 메시지 */
  .initial-message, .no-selection {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px 20px;
    height: 100%;
  }
  
  .message-icon, .selection-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }
  
  .initial-message h4, .no-selection h4 {
    font-size: 18px;
    font-weight: 600;
    color: #374151;
    margin: 0 0 8px 0;
  }
  
  .initial-message p, .no-selection p {
    font-size: 14px;
    color: #6b7280;
    margin: 0;
    line-height: 1.5;
  }
  
  /* 검색 결과 없음 */
  .no-results {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px 20px;
  }
  
  .no-results-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }
  
  .no-results h4 {
    font-size: 18px;
    font-weight: 600;
    color: #374151;
    margin: 0 0 8px 0;
  }
  
  .no-results p {
    font-size: 14px;
    color: #6b7280;
    margin: 0;
  }
  
  /* 은행 목록 */
  .bank-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .bank-item {
    background: #f8fafc;
    border: 2px solid transparent;
    border-radius: 12px;
    padding: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease-out;
  }
  
  .bank-item:hover {
    background: #f1f5f9;
    border-color: #e5e7eb;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .bank-item.active {
    background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
    color: white;
    border-color: #4DD0B1;
    box-shadow: 0 4px 16px rgba(77, 208, 177, 0.3);
  }
  
  .bank-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
  }
  
  .bank-name {
    font-size: 16px;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
    line-height: 1.3;
  }
  
  .bank-item.active .bank-name {
    color: white;
  }
  
  .bank-category {
    background: #e5e7eb;
    color: #6b7280;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .bank-item.active .bank-category {
    background: rgba(255, 255, 255, 0.2);
    color: white;
  }
  
  .bank-address {
    font-size: 13px;
    color: #6b7280;
    margin: 0 0 8px 0;
    line-height: 1.4;
  }
  
  .bank-item.active .bank-address {
    color: rgba(255, 255, 255, 0.9);
  }
  
  .bank-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    font-size: 12px;
  }
  
  .bank-phone, .bank-distance {
    display: flex;
    align-items: center;
    gap: 4px;
    color: #4DD0B1;
    font-weight: 500;
  }
  
  .bank-item.active .bank-phone,
  .bank-item.active .bank-distance {
    color: white;
  }
  
  /* 상세 정보 */
  .detail-view {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .detail-header {
    text-align: center;
    padding-bottom: 20px;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 24px;
  }
  
  .detail-header h3 {
    font-size: 20px;
    font-weight: 700;
    color: #1f2937;
    margin: 0 0 8px 0;
  }
  
  .detail-category {
    background: #f3f4f6;
    color: #6b7280;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
  }
  
  .detail-sections {
    flex: 1;
    overflow-y: auto;
  }
  
  .detail-section {
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid #f3f4f6;
  }
  
  .detail-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
  }
  
  .detail-section h4 {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .detail-section h4 i {
    color: #4DD0B1;
    width: 16px;
  }
  
  .detail-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 8px 0;
    border-bottom: 1px solid #f9fafb;
  }
  
  .detail-item:last-child {
    border-bottom: none;
  }
  
  .item-label {
    font-weight: 500;
    color: #6b7280;
    min-width: 80px;
    font-size: 14px;
  }
  
  .item-value {
    color: #374151;
    text-align: right;
    flex: 1;
    margin-left: 12px;
    font-size: 14px;
  }
  
  /* 액션 버튼 */
  .action-buttons {
    display: flex;
    gap: 8px;
    margin-top: 16px;
  }
  
  .action-btn {
    flex: 1;
    padding: 12px 16px;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  
  .action-btn.primary {
    background: linear-gradient(135deg, #4DD0B1 0%, #3CBFA0 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(77, 208, 177, 0.3);
  }
  
  .action-btn.primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(77, 208, 177, 0.4);
  }
  
  .action-btn.secondary {
    background: #f8fafc;
    color: #4DD0B1;
    border: 1px solid #e5e7eb;
  }
  
  .action-btn.secondary:hover {
    background: #f1f5f9;
    border-color: #4DD0B1;
  }
  
  /* 토스트 메시지 */
  .toast {
    position: fixed;
    top: 100px;
    right: 20px;
    padding: 16px 24px;
    border-radius: 12px;
    color: white;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 1000;
    animation: slideInRight 0.3s ease-out;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  }
  
  .toast.success {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  }
  
  .toast.warning {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  }
  
  .toast.error {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  }
  
  .toast.info {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  }
  
  @keyframes slideInRight {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
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
  
  /* 반응형 디자인 */
  @media (max-width: 1024px) {
    .main-content {
      grid-template-columns: 1fr;
      height: auto;
    }
    
    .map-container {
      height: 400px;
      order: 2;
    }
    
    .sidebar {
      height: 500px;
      order: 1;
      margin-bottom: 24px;
    }
  }
  
  @media (max-width: 768px) {
    .bank-finder {
      padding: 20px 16px;
    }
    
    .page-header {
      flex-direction: column;
      text-align: center;
      gap: 16px;
    }
    
    .search-filters {
      flex-direction: column;
      gap: 16px;
    }
    
    .search-btn {
      align-self: stretch;
    }
    
    .main-content {
      gap: 16px;
    }
    
    .sidebar {
      height: 400px;
    }
    
    .tab-content {
      padding: 16px;
    }
    
    .action-buttons {
      flex-direction: column;
    }
  }
  
  @media (max-width: 480px) {
    .bank-meta {
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
    }
    
    .detail-item {
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
    }
    
    .item-value {
      text-align: left;
      margin-left: 0;
    }
  }
  </style>