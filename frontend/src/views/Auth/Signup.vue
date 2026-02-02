<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Create Account</h1>
        <p>Sign up to get started</p>
      </div>

      <div class="auth-form">
        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="email"
            type="email" 
            placeholder="you@email.com"
            :class="{ 'error': errors.email }"
          />
          <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label>Password</label>
          <input 
            v-model="password"
            type="password" 
            placeholder="••••••••"
            :class="{ 'error': errors.password }"
          />
          <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input 
            v-model="confirmPassword"
            type="password" 
            placeholder="••••••••"
            :class="{ 'error': errors.confirmPassword }"
          />
          <span v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</span>
        </div>

        <div v-if="errors.general" class="error-banner">
          {{ errors.general }}
        </div>

        <button 
          class="btn btn-primary full-width"
          :disabled="loading"
          @click="handleSignup"
        >
          <span v-if="loading" class="spinner small"></span>
          <span v-else>Sign Up</span>
        </button>

        <p class="auth-footer">
          Already have an account? 
          <router-link :to="{ name: 'login' }">Sign in</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const errors = ref<Record<string, string>>({})

const validate = (): boolean => {
  errors.value = {}

  if (!email.value.trim()) {
    errors.value.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = 'Invalid email format'
  }

  if (!password.value) {
    errors.value.password = 'Password is required'
  } else if (password.value.length < 6) {
    errors.value.password = 'Password must be at least 6 characters'
  }

  if (!confirmPassword.value) {
    errors.value.confirmPassword = 'Please confirm your password'
  } else if (password.value !== confirmPassword.value) {
    errors.value.confirmPassword = 'Passwords do not match'
  }

  return Object.keys(errors.value).length === 0
}

const handleSignup = async () => {
  if (!validate()) return

  loading.value = true
  errors.value = {}

  try {
    await authStore.signUp(email.value, password.value)
    router.push({ name: 'home' })
  } catch (error: any) {
    if (error.code === 'auth/email-already-in-use') {
      errors.value.general = 'An account with this email already exists.'
    } else {
      errors.value.general = error.message || 'Signup failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--color-background, #0c0c0c);
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--color-surface, #141414);
  border: 1px solid rgba(212, 175, 55, 0.15);
  border-radius: 0.75rem;
  padding: 2.5rem;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h1 {
  font-family: var(--font-family-display, Georgia, serif);
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.auth-header p {
  color: #9ca3af;
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-group input {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.04);
  color: #ffffff;
  font-size: 0.95rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-group input::placeholder {
  color: #4b5563;
}

.form-group input:focus {
  outline: none;
  border-color: #D4AF37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15);
}

.form-group input.error {
  border-color: #ef4444;
}

.error-text {
  color: #ef4444;
  font-size: 0.78rem;
  margin-top: 0.15rem;
}

.error-banner {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  color: #f87171;
  font-size: 0.85rem;
  text-align: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #C5A028;
  color: #000;
}

.btn-primary:hover {
  background: #D4AF37;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.full-width {
  width: 100%;
}

.spinner {
  border: 2px solid rgba(0, 0, 0, 0.3);
  border-top: 2px solid #000;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.auth-footer {
  text-align: center;
  color: #9ca3af;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.auth-footer a {
  color: #D4AF37;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.auth-footer a:hover {
  color: #D4AF37;
  text-decoration: underline;
}
</style>