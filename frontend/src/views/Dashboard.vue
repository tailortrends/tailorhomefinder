<template>
  <div class="dashboard-page">
    <div class="container">
      <!-- Header -->
      <div class="dashboard-header">
        <div>
          <h1>My Dashboard</h1>
          <p class="welcome-text">Welcome, {{ authStore.user?.email }}</p>
        </div>
        <div class="header-actions">
          <router-link 
            v-if="authStore.user?.email === ADMIN_EMAIL"
            :to="{ name: 'admin' }" 
            class="btn btn-admin"
          >
            Admin Panel
          </router-link>
          <button class="btn btn-signout" @click="handleLogout">Sign Out</button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </div>
          <span class="stat-label">Saved Properties</span>
          <span class="stat-value">{{ favorites.length }}</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
          </div>
          <span class="stat-label">Recent Searches</span>
          <span class="stat-value">{{ savedSearches.length }}</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
          </div>
          <span class="stat-label">Notifications</span>
          <span class="stat-value">0</span>
        </div>
      </div>

      <!-- Two Column Layout -->
      <div class="dashboard-grid">
        <!-- Saved Properties -->
        <section class="dashboard-section">
          <div class="section-header">
            <h2>Saved Properties</h2>
            <router-link :to="{ name: 'search' }" class="view-all">Browse more →</router-link>
          </div>

          <div v-if="loadingFavs" class="loading-state">
            <div class="spinner"></div>
          </div>

          <div v-else-if="favorites.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
            <p>No saved properties yet.<br/>Click the heart on any property to save it here.</p>
          </div>

          <div v-else class="favorites-list">
            <div 
              v-for="property in favorites"
              :key="property.id"
              class="fav-card"
              @click="goToProperty(property.id)"
            >
              <img :src="property.image" :alt="property.title" class="fav-image" />
              <div class="fav-info">
                <h3>{{ property.title }}</h3>
                <p class="fav-location">{{ property.location }}</p>
                <div class="fav-stats">
                  <span>{{ property.beds }} bed</span>
                  <span>{{ property.baths }} bath</span>
                  <span>{{ property.sqft?.toLocaleString() }} sqft</span>
                </div>
              </div>
              <span class="fav-price">{{ formatPrice(property.price) }}</span>
            </div>
          </div>
        </section>

        <!-- Saved Searches & Chat -->
        <section class="dashboard-section">
          <!-- Saved Searches -->
          <div class="section-header">
            <h2>Saved Searches</h2>
          </div>

          <div v-if="savedSearches.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
            <p>No saved searches yet.<br/>Searches will appear here when you save them.</p>
          </div>

          <!-- Chat Assistant -->
          <div class="chat-section">
            <div class="section-header">
              <h2>Property Assistant</h2>
              <span class="chat-badge">AI Powered</span>
            </div>
            <div class="chat-container">
              <div class="chat-messages" ref="chatMessages">
                <div 
                  v-for="(msg, idx) in chatHistory"
                  :key="idx"
                  :class="['chat-msg', msg.role === 'user' ? 'user' : 'assistant']"
                >
                  <div class="chat-bubble">{{ msg.content }}</div>
                </div>
              </div>
              <div class="chat-input-area">
                <input 
                  v-model="chatInput"
                  type="text"
                  placeholder="Ask about properties..."
                  @keyup.enter="sendChat"
                />
                <button class="chat-send-btn" @click="sendChat" :disabled="!chatInput.trim() || chatLoading">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 2 L11 13"/>
                    <path d="M22 2 L15 22 L11 13 L2 9 Z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePropertiesStore } from '@/stores/properties'
import { formatPrice } from '@/utils/propertyHelpers'
import type { Property } from '@/types/property'

// Admin email — change this to your email
const ADMIN_EMAIL = 'stailor45@gmail.com'

const router = useRouter()
const authStore = useAuthStore()
const propertiesStore = usePropertiesStore()

const favorites = ref<Property[]>([])
const savedSearches = ref<any[]>([])
const loadingFavs = ref(true)

// Chat state
const chatInput = ref('')
const chatLoading = ref(false)
const chatMessages = ref<HTMLElement | null>(null)
const chatHistory = ref<{ role: string; content: string }[]>([
  { role: 'assistant', content: 'Hi! I\'m your property assistant. Ask me anything like "What are the best neighborhoods in Phoenix?" or "Show me 3 bed homes under $500K".' }
])

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push({ name: 'home' })
  } catch (e) {
    console.error('Logout error:', e)
  }
}

const goToProperty = (id: string) => {
  router.push({ name: 'property-detail', params: { id } })
}

const loadFavorites = async () => {
  loadingFavs.value = true
  try {
    // Load all properties first
    if (propertiesStore.properties.length === 0) {
      await propertiesStore.fetchProperties()
    }

    // Get saved favorite IDs from localStorage
    const saved = localStorage.getItem('tailor_favorites')
    const favoriteIds: string[] = saved ? JSON.parse(saved) : []

    // Match IDs to actual property objects
    favorites.value = propertiesStore.properties.filter(p => favoriteIds.includes(p.id))
  } catch (e) {
    console.error('Error loading favorites:', e)
  } finally {
    loadingFavs.value = false
  }
}

// Simple AI chat using keyword matching (works without backend)
const sendChat = async () => {
  const msg = chatInput.value.trim()
  if (!msg || chatLoading.value) return

  chatHistory.value.push({ role: 'user', content: msg })
  chatInput.value = ''
  chatLoading.value = true

  await nextTick()
  scrollChatToBottom()

  // Simulate thinking delay
  await new Promise(r => setTimeout(r, 800))

  // Simple keyword-based responses
  const lower = msg.toLowerCase()
  let response = ''

  if (lower.includes('neighborhood') || lower.includes('area') || lower.includes('best place')) {
    response = 'Some great Phoenix neighborhoods include Scottsdale (luxury condos & golf), Paradise Valley (high-end estates), Ahwatukee (family-friendly), and Downtown Phoenix (urban living). Would you like me to help you search in any of these areas?'
  } else if (lower.includes('budget') || lower.includes('afford') || lower.includes('price')) {
    response = 'Based on the Phoenix market, here\'s a rough guide:\n• Under $300K: Smaller homes, older builds\n• $300K–$600K: Mid-range 3-4 bed homes\n• $600K–$1M: Luxury single-family\n• $1M+: Estates & custom builds\nWould you like me to filter properties by a specific price range?'
  } else if (lower.includes('bedroom') || lower.includes('bed') || lower.includes('family')) {
    response = 'For a family, I\'d recommend looking at 3-4 bedroom homes. We have properties ranging from 1 to 5+ bedrooms. Want me to search for homes with a specific number of bedrooms? Just tell me your budget too and I can narrow it down!'
  } else if (lower.includes('invest') || lower.includes('rental') || lower.includes('roi')) {
    response = 'Great question! Phoenix is a strong investment market. Key factors to consider:\n• Rental yield: typically 4-6% in Phoenix\n• Appreciation: Phoenix saw ~8-12% annual growth recently\n• Best areas for rentals: Scottsdale, Tempe, Chandler\nWould you like to explore specific investment properties?'
  } else if (lower.includes('search') || lower.includes('find') || lower.includes('show')) {
    response = 'I can help you search! Head to the Search page and use the filters for price, bedrooms, bathrooms, property type, and city. You can also toggle to Map view to see properties on an interactive map. Want any tips on narrowing your search?'
  } else {
    response = 'That\'s a great question! I\'m best at helping with property searches, neighborhood info, budgeting, and investment advice. Try asking me something like:\n• "What neighborhoods are good for families?"\n• "Help me find a 3 bed under $500K"\n• "Is Phoenix good for investing?"'
  }

  chatHistory.value.push({ role: 'assistant', content: response })
  chatLoading.value = false

  await nextTick()
  scrollChatToBottom()
}

const scrollChatToBottom = () => {
  if (chatMessages.value) {
    chatMessages.value.scrollTop = chatMessages.value.scrollHeight
  }
}

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.dashboard-page {
  min-height: calc(100vh - 70px);
  background: #0c0c0c;
  padding: 2rem 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-family: Georgia, serif;
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.25rem;
}

.welcome-text {
  color: #9ca3af;
  font-size: 0.9rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.btn {
  padding: 0.6rem 1.25rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn-admin {
  background: #D4AF37;
  color: #000;
}

.btn-admin:hover {
  background: #C5A028;
}

.btn-signout {
  background: rgba(255,255,255,0.07);
  color: #9ca3af;
  border: 1px solid rgba(255,255,255,0.1);
}

.btn-signout:hover {
  color: #fff;
  border-color: rgba(255,255,255,0.3);
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: border-color 0.2s;
}

.stat-card:hover {
  border-color: rgba(212, 175, 55, 0.3);
}

.stat-icon {
  color: #D4AF37;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #9ca3af;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  font-family: Georgia, serif;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.dashboard-section {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.section-header h2 {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
}

.view-all {
  color: #D4AF37;
  font-size: 0.8rem;
  text-decoration: none;
  font-weight: 600;
}

.view-all:hover {
  text-decoration: underline;
}

/* Empty & Loading */
.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: #6b7280;
}

.empty-state svg {
  margin-bottom: 0.75rem;
  color: #4b5563;
}

.empty-state p {
  font-size: 0.85rem;
  line-height: 1.5;
}

.loading-state {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  border: 2px solid rgba(255,255,255,0.1);
  border-top: 2px solid #D4AF37;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Favorites List */
.favorites-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.fav-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.fav-card:hover {
  border-color: rgba(212, 175, 55, 0.4);
  background: rgba(212, 175, 55, 0.04);
}

.fav-image {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 0.375rem;
  flex-shrink: 0;
}

.fav-info {
  flex: 1;
  min-width: 0;
}

.fav-info h3 {
  color: #fff;
  font-size: 0.9rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fav-location {
  color: #6b7280;
  font-size: 0.78rem;
  margin-top: 0.15rem;
}

.fav-stats {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.fav-stats span {
  color: #9ca3af;
  font-size: 0.75rem;
}

.fav-price {
  color: #D4AF37;
  font-weight: 700;
  font-size: 0.95rem;
  white-space: nowrap;
  font-family: Georgia, serif;
}

/* Chat */
.chat-section {
  margin-top: 1.5rem;
  border-top: 1px solid rgba(255,255,255,0.06);
  padding-top: 1.5rem;
}

.chat-badge {
  background: rgba(212, 175, 55, 0.15);
  color: #D4AF37;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 280px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.5rem;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chat-msg {
  display: flex;
}

.chat-msg.user {
  justify-content: flex-end;
}

.chat-msg.assistant {
  justify-content: flex-start;
}

.chat-bubble {
  max-width: 85%;
  padding: 0.6rem 0.9rem;
  border-radius: 0.5rem;
  font-size: 0.82rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.chat-msg.user .chat-bubble {
  background: #D4AF37;
  color: #000;
  font-weight: 500;
}

.chat-msg.assistant .chat-bubble {
  background: rgba(255,255,255,0.07);
  color: #d1d5db;
}

.chat-input-area {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.chat-input-area input {
  flex: 1;
  padding: 0.6rem 0.85rem;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 0.375rem;
  background: rgba(255,255,255,0.04);
  color: #fff;
  font-size: 0.82rem;
  outline: none;
  transition: border-color 0.2s;
}

.chat-input-area input:focus {
  border-color: #D4AF37;
}

.chat-input-area input::placeholder {
  color: #4b5563;
}

.chat-send-btn {
  padding: 0.6rem 0.85rem;
  background: #D4AF37;
  border: none;
  border-radius: 0.375rem;
  color: #000;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-send-btn:hover {
  background: #C5A028;
}

.chat-send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .dashboard-grid { grid-template-columns: 1fr; }
  .dashboard-header { flex-direction: column; gap: 1rem; }
}
</style>