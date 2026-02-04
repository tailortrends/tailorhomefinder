<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Property } from '@/types/property'
import { inquiryService, type ContactFormData as InquiryFormData } from '@/services/inquiryService'

const props = defineProps<{
  property: Property
}>()

const emit = defineEmits<{
  (e: 'submit', data: ContactFormData): void
}>()

interface ContactFormData {
  name: string
  email: string
  phone: string
  message: string
  propertyId: string
  inquiryType?: 'general' | 'schedule_tour' | 'request_info' | 'make_offer'
}

// Form state
const formData = ref<ContactFormData>({
  name: '',
  email: '',
  phone: '',
  message: `Hi, I'm interested in ${props.property.street || props.property.title}. Please send me more information.`,
  propertyId: props.property.id,
  inquiryType: 'general'
})

const isSubmitting = ref(false)
const isSubmitted = ref(false)
const errors = ref<Record<string, string>>({})

// Validation
const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const validatePhone = (phone: string): boolean => {
  const re = /^[\d\s\-\(\)]+$/
  return phone.length >= 10 && re.test(phone)
}

const isFormValid = computed(() => {
  return (
    formData.value.name.trim() !== '' &&
    validateEmail(formData.value.email) &&
    validatePhone(formData.value.phone) &&
    formData.value.message.trim() !== ''
  )
})

// Form submission
async function handleSubmit() {
  // Clear previous errors
  errors.value = {}

  // Validate
  if (!formData.value.name.trim()) {
    errors.value.name = 'Name is required'
  }

  if (!validateEmail(formData.value.email)) {
    errors.value.email = 'Please enter a valid email'
  }

  if (!validatePhone(formData.value.phone)) {
    errors.value.phone = 'Please enter a valid phone number'
  }

  if (!formData.value.message.trim()) {
    errors.value.message = 'Message is required'
  }

  if (Object.keys(errors.value).length > 0) return

  isSubmitting.value = true

  try {
    // Determine inquiry type from message
    let inquiryType: 'general' | 'schedule_tour' | 'request_info' | 'make_offer' = 'general'
    const messageLower = formData.value.message.toLowerCase()
    if (messageLower.includes('tour') || messageLower.includes('schedule') || messageLower.includes('visit')) {
      inquiryType = 'schedule_tour'
    } else if (messageLower.includes('offer')) {
      inquiryType = 'make_offer'
    } else if (messageLower.includes('information') || messageLower.includes('info')) {
      inquiryType = 'request_info'
    }

    // Build property address
    const propertyAddress = props.property.street
      ? `${props.property.street}, ${props.property.city}, ${props.property.state} ${props.property.zipCode}`
      : props.property.location || props.property.title

    // Submit to API
    const response = await inquiryService.submitContactForm({
      name: formData.value.name,
      email: formData.value.email,
      phone: formData.value.phone,
      message: formData.value.message,
      property_id: formData.value.propertyId,
      property_address: propertyAddress,
      property_price: props.property.price,
      inquiry_type: inquiryType
    })

    if (response.success) {
      // Emit the form data for any parent handling
      emit('submit', { ...formData.value })

      isSubmitted.value = true

      // Reset form after 5 seconds
      setTimeout(() => {
        isSubmitted.value = false
        formData.value = {
          name: '',
          email: '',
          phone: '',
          message: `Hi, I'm interested in ${props.property.street || props.property.title}. Please send me more information.`,
          propertyId: props.property.id,
          inquiryType: 'general'
        }
      }, 5000)
    } else {
      errors.value.submit = response.message || 'Failed to send message. Please try again.'
    }
  } catch (error) {
    console.error('Contact form submission error:', error)
    errors.value.submit = error instanceof Error ? error.message : 'Failed to send message. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

// Quick action buttons
const quickActions = [
  {
    label: 'Schedule Tour',
    icon: 'calendar',
    message: 'I would like to schedule a tour of this property.',
    inquiryType: 'schedule_tour' as const
  },
  {
    label: 'Request Info',
    icon: 'info',
    message: 'Please send me more information about this property.',
    inquiryType: 'request_info' as const
  },
  {
    label: 'Make Offer',
    icon: 'document',
    message: 'I am interested in making an offer on this property.',
    inquiryType: 'make_offer' as const
  }
]

function setQuickMessage(message: string, inquiryType: 'general' | 'schedule_tour' | 'request_info' | 'make_offer' = 'general') {
  const propertyRef = props.property.street || props.property.title
  formData.value.message = `${message} Property: ${propertyRef}`
  formData.value.inquiryType = inquiryType
}

const getIcon = (iconName: string) => {
  const icons: Record<string, string> = {
    calendar: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
    info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    document: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
  }
  return icons[iconName] || icons.info
}
</script>

<template>
  <div class="contact-form">
    <!-- Header -->
    <div class="form-header">
      <h3 class="form-title">Contact Agent</h3>
      <p class="form-subtitle">Get more information about this property</p>
    </div>

    <!-- Success Message -->
    <Transition name="slide-fade">
      <div v-if="isSubmitted" class="success-message">
        <svg class="w-12 h-12 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h4 class="success-title">Message Sent!</h4>
        <p class="success-text">
          {{ formData.inquiryType === 'schedule_tour'
            ? 'An agent will contact you within 24 hours to schedule your tour.'
            : 'An agent will contact you shortly. Check your email for confirmation.' }}
        </p>
      </div>
    </Transition>

    <!-- Form -->
    <form v-if="!isSubmitted" @submit.prevent="handleSubmit" class="contact-form-inner">
      <!-- Quick Actions -->
      <div class="quick-actions">
        <p class="quick-actions-label">Quick Actions:</p>
        <div class="quick-actions-grid">
          <button
            v-for="action in quickActions"
            :key="action.label"
            type="button"
            class="quick-action-btn"
            @click="setQuickMessage(action.message, action.inquiryType)"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getIcon(action.icon)" />
            </svg>
            {{ action.label }}
          </button>
        </div>
      </div>

      <!-- Name -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Full Name *</span>
        </label>
        <input
          v-model="formData.name"
          type="text"
          placeholder="John Doe"
          class="input input-bordered"
          :class="{ 'input-error': errors.name }"
        />
        <label v-if="errors.name" class="label">
          <span class="label-text-alt text-error">{{ errors.name }}</span>
        </label>
      </div>

      <!-- Email -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Email Address *</span>
        </label>
        <input
          v-model="formData.email"
          type="email"
          placeholder="john@example.com"
          class="input input-bordered"
          :class="{ 'input-error': errors.email }"
        />
        <label v-if="errors.email" class="label">
          <span class="label-text-alt text-error">{{ errors.email }}</span>
        </label>
      </div>

      <!-- Phone -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Phone Number *</span>
        </label>
        <input
          v-model="formData.phone"
          type="tel"
          placeholder="(555) 123-4567"
          class="input input-bordered"
          :class="{ 'input-error': errors.phone }"
        />
        <label v-if="errors.phone" class="label">
          <span class="label-text-alt text-error">{{ errors.phone }}</span>
        </label>
      </div>

      <!-- Message -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">Message *</span>
        </label>
        <textarea
          v-model="formData.message"
          rows="5"
          placeholder="Tell us about your interest..."
          class="textarea textarea-bordered"
          :class="{ 'input-error': errors.message }"
        />
        <label v-if="errors.message" class="label">
          <span class="label-text-alt text-error">{{ errors.message }}</span>
        </label>
      </div>

      <!-- Submit Error -->
      <div v-if="errors.submit" class="alert alert-error">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ errors.submit }}</span>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        class="btn btn-primary btn-lg w-full"
        :disabled="!isFormValid || isSubmitting"
      >
        <span v-if="!isSubmitting">Send Message</span>
        <span v-else class="loading loading-spinner loading-sm"></span>
        <span v-if="isSubmitting">Sending...</span>
      </button>

      <!-- Privacy Notice -->
      <p class="privacy-notice">
        By clicking "Send Message", you agree to our 
        <a href="#" class="link link-primary">Terms of Service</a> and 
        <a href="#" class="link link-primary">Privacy Policy</a>.
      </p>
    </form>
  </div>
</template>

<style scoped>
.contact-form {
  @apply bg-white rounded-xl p-6 shadow-lg;
  @apply sticky top-24;
  border: 1px solid hsl(var(--b2));
}

/* Header */
.form-header {
  @apply mb-6 pb-6 border-b border-base-200;
}

.form-title {
  @apply text-2xl font-bold text-base-content mb-2;
  font-feature-settings: 'ss01', 'ss02';
}

.form-subtitle {
  @apply text-base-content/60;
}

/* Success Message */
.success-message {
  @apply flex flex-col items-center justify-center py-12;
  @apply text-center;
}

.success-message svg {
  @apply text-success;
}

.success-title {
  @apply text-2xl font-bold text-success mb-2;
}

.success-text {
  @apply text-base-content/60;
}

/* Form */
.contact-form-inner {
  @apply space-y-4;
}

/* Quick Actions */
.quick-actions {
  @apply mb-6;
}

.quick-actions-label {
  @apply text-sm font-medium text-base-content/70 mb-3;
}

.quick-actions-grid {
  @apply grid grid-cols-1 gap-2;
}

.quick-action-btn {
  @apply flex items-center gap-2;
  @apply px-4 py-3 rounded-lg;
  @apply bg-base-200 hover:bg-primary hover:text-white;
  @apply text-left text-sm font-medium;
  @apply transition-all duration-300;
  @apply border-2 border-transparent hover:border-primary;
}

.quick-action-btn:hover {
  @apply shadow-md;
}

/* Privacy Notice */
.privacy-notice {
  @apply text-xs text-base-content/50 text-center mt-4;
}

/* Transitions */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .contact-form {
    @apply static;
  }
}
</style>
