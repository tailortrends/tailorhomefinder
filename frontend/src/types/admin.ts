// Admin Dashboard Type Definitions

// ================== User Types ==================

export type UserStatus = 'active' | 'inactive' | 'suspended' | 'pending'
export type UserRole = 'customer' | 'agent' | 'admin'

export interface User {
  id: string
  firebase_uid?: string
  email: string
  first_name?: string
  last_name?: string
  full_name?: string
  phone?: string

  // Profile
  avatar_url?: string
  bio?: string

  // Address
  address?: string
  city?: string
  state?: string
  zip_code?: string

  // Preferences
  preferred_locations?: string[]
  min_budget?: number
  max_budget?: number
  preferred_beds?: number
  preferred_baths?: number
  preferred_sqft_min?: number
  preferred_sqft_max?: number
  preferred_property_types?: string[]
  move_in_timeline?: string

  // Financial
  pre_approved: boolean
  pre_approval_amount?: number
  financing_type?: string

  // Status
  status: UserStatus
  role: UserRole

  // Assignment
  assigned_agent_id?: string

  // Activity
  last_login_at?: string
  last_active_at?: string
  search_count: number
  saved_properties_count: number
  inquiries_count: number

  // Communication
  email_notifications: boolean
  sms_notifications: boolean
  marketing_emails: boolean

  // Notes
  internal_notes?: string
  referral_source?: string

  // Timestamps
  created_at: string
  updated_at?: string
}

export interface UserList {
  total: number
  users: User[]
  limit: number
  offset: number
}

export interface UserStats {
  total_users: number
  active_users: number
  inactive_users: number
  new_users_today: number
  new_users_this_week: number
  new_users_this_month: number
  users_by_status: Record<string, number>
  users_by_role: Record<string, number>
}

// ================== Agent Types ==================

export type AgentStatus = 'active' | 'inactive' | 'on_leave' | 'terminated'
export type AgentRole = 'junior_agent' | 'senior_agent' | 'team_lead' | 'manager' | 'admin'

export interface Agent {
  id: string
  firebase_uid?: string
  email: string
  first_name: string
  last_name: string
  full_name?: string
  phone?: string
  mobile?: string

  // Profile
  avatar_url?: string
  bio?: string
  title?: string

  // License
  license_number?: string
  license_state?: string
  license_expiry?: string

  // Specializations
  specializations?: string[]
  service_areas?: string[]
  languages?: string[]

  // Status & Role
  status: AgentStatus
  role: AgentRole
  is_admin: boolean

  // Metrics
  total_customers: number
  active_customers: number
  closed_deals: number
  rating: number
  reviews_count: number

  // Capacity
  max_customers: number
  has_capacity?: boolean

  // Schedule
  working_hours?: Record<string, string>
  timezone: string

  // Commission
  commission_rate?: number

  // Team
  manager_id?: string
  team_name?: string

  // Activity
  last_login_at?: string
  last_active_at?: string

  // Timestamps
  created_at: string
  updated_at?: string
  hired_at?: string

  // Notes
  internal_notes?: string
}

export interface AgentList {
  total: number
  agents: Agent[]
  limit: number
  offset: number
}

export interface AgentStats {
  total_agents: number
  active_agents: number
  total_customers_managed: number
  avg_customers_per_agent: number
  total_closed_deals: number
  agents_by_status: Record<string, number>
  agents_by_role: Record<string, number>
  top_performers: AgentPerformer[]
}

export interface AgentPerformer {
  id: string
  name: string
  closed_deals: number
  rating: number
  active_customers: number
}

// ================== CRM Types ==================

export type InteractionType =
  | 'phone_call'
  | 'email'
  | 'sms'
  | 'in_person'
  | 'video_call'
  | 'property_tour'
  | 'open_house'
  | 'document_sent'
  | 'offer_submitted'
  | 'contract_signed'
  | 'other'

export type InteractionOutcome =
  | 'positive'
  | 'neutral'
  | 'negative'
  | 'follow_up_needed'
  | 'no_answer'
  | 'left_voicemail'

export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent'
export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled' | 'overdue'

export type PipelineStage =
  | 'new_lead'
  | 'contacted'
  | 'qualified'
  | 'viewing_properties'
  | 'making_offers'
  | 'under_contract'
  | 'closing'
  | 'closed_won'
  | 'closed_lost'
  | 'on_hold'

export interface Interaction {
  id: string
  customer_id: string
  agent_id?: string
  property_id?: string

  interaction_type: InteractionType
  subject?: string
  description: string
  outcome?: InteractionOutcome

  duration_minutes?: number
  scheduled_at?: string
  completed_at?: string

  follow_up_required: boolean
  follow_up_date?: string
  follow_up_notes?: string

  attachments?: string[]

  created_at: string
  updated_at?: string

  // Populated
  customer_name?: string
  agent_name?: string
}

export interface InteractionList {
  total: number
  interactions: Interaction[]
  limit: number
  offset: number
}

export interface CustomerNote {
  id: string
  customer_id: string
  agent_id?: string
  title?: string
  content: string
  category?: string
  is_pinned: boolean
  is_important: boolean
  is_private: boolean
  created_at: string
  updated_at?: string
  agent_name?: string
}

export interface NoteList {
  total: number
  notes: CustomerNote[]
  limit: number
  offset: number
}

export interface Task {
  id: string
  customer_id?: string
  assigned_agent_id?: string
  property_id?: string
  title: string
  description?: string
  priority: TaskPriority
  status: TaskStatus
  due_date?: string
  reminder_date?: string
  completed_at?: string
  task_type?: string
  created_at: string
  updated_at?: string

  // Populated
  customer_name?: string
  assigned_agent_name?: string
}

export interface TaskList {
  total: number
  tasks: Task[]
  limit: number
  offset: number
}

export interface Pipeline {
  id: string
  customer_id: string
  assigned_agent_id?: string
  stage: PipelineStage
  previous_stage?: string
  stage_entered_at: string
  last_stage_change?: string
  expected_close_date?: string
  deal_value?: number
  probability: number
  lost_reason?: string
  lost_to_competitor?: string
  lead_source?: string
  created_at: string
  updated_at?: string

  // Populated
  customer_name?: string
  customer_email?: string
  assigned_agent_name?: string
}

export interface PipelineList {
  total: number
  pipelines: Pipeline[]
  limit: number
  offset: number
}

export interface PipelineStats {
  total_leads: number
  leads_by_stage: Record<string, number>
  total_deal_value: number
  avg_deal_value: number
  conversion_rate: number
  avg_time_to_close?: number
}

// ================== Feature Settings ==================

export interface FeatureSetting {
  id: string
  feature_key: string
  feature_name: string
  description?: string
  is_enabled: boolean
  category?: string
  display_order: number
  min_role: string
  created_at: string
  updated_at?: string
  enabled_by?: string
  enabled_at?: string
}

export interface FeatureSettingList {
  total: number
  features: FeatureSetting[]
}

// ================== Activity Log ==================

export interface ActivityLog {
  id: string
  actor_id: string
  actor_type: string
  actor_email?: string
  action: string
  action_category?: string
  description?: string
  target_type?: string
  target_id?: string
  details?: Record<string, any>
  ip_address?: string
  created_at: string
}

export interface ActivityLogList {
  total: number
  activities: ActivityLog[]
  limit: number
  offset: number
}

// ================== Dashboard Stats ==================

export interface AdminDashboardStats {
  total_customers: number
  active_customers: number
  total_agents: number
  active_agents: number
  total_inquiries: number
  new_inquiries: number
  total_properties: number
  properties_viewed: number
  leads_this_month: number
  conversions_this_month: number
  revenue_this_month?: number
}

export interface CRMDashboardStats {
  total_interactions: number
  interactions_today: number
  pending_tasks: number
  overdue_tasks: number
  follow_ups_due: number
  pipeline_value: number
  customers_in_pipeline: number
}

// ================== Constants ==================

export const USER_STATUS_OPTIONS = [
  { label: 'Active', value: 'active' },
  { label: 'Inactive', value: 'inactive' },
  { label: 'Suspended', value: 'suspended' },
  { label: 'Pending', value: 'pending' }
]

export const USER_ROLE_OPTIONS = [
  { label: 'Customer', value: 'customer' },
  { label: 'Agent', value: 'agent' },
  { label: 'Admin', value: 'admin' }
]

export const AGENT_STATUS_OPTIONS = [
  { label: 'Active', value: 'active' },
  { label: 'Inactive', value: 'inactive' },
  { label: 'On Leave', value: 'on_leave' },
  { label: 'Terminated', value: 'terminated' }
]

export const AGENT_ROLE_OPTIONS = [
  { label: 'Junior Agent', value: 'junior_agent' },
  { label: 'Senior Agent', value: 'senior_agent' },
  { label: 'Team Lead', value: 'team_lead' },
  { label: 'Manager', value: 'manager' },
  { label: 'Admin', value: 'admin' }
]

export const INTERACTION_TYPE_OPTIONS = [
  { label: 'Phone Call', value: 'phone_call' },
  { label: 'Email', value: 'email' },
  { label: 'SMS', value: 'sms' },
  { label: 'In Person', value: 'in_person' },
  { label: 'Video Call', value: 'video_call' },
  { label: 'Property Tour', value: 'property_tour' },
  { label: 'Open House', value: 'open_house' },
  { label: 'Document Sent', value: 'document_sent' },
  { label: 'Offer Submitted', value: 'offer_submitted' },
  { label: 'Contract Signed', value: 'contract_signed' },
  { label: 'Other', value: 'other' }
]

export const TASK_PRIORITY_OPTIONS = [
  { label: 'Low', value: 'low' },
  { label: 'Medium', value: 'medium' },
  { label: 'High', value: 'high' },
  { label: 'Urgent', value: 'urgent' }
]

export const TASK_STATUS_OPTIONS = [
  { label: 'Pending', value: 'pending' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' }
]

export const PIPELINE_STAGE_OPTIONS = [
  { label: 'New Lead', value: 'new_lead' },
  { label: 'Contacted', value: 'contacted' },
  { label: 'Qualified', value: 'qualified' },
  { label: 'Viewing Properties', value: 'viewing_properties' },
  { label: 'Making Offers', value: 'making_offers' },
  { label: 'Under Contract', value: 'under_contract' },
  { label: 'Closing', value: 'closing' },
  { label: 'Closed Won', value: 'closed_won' },
  { label: 'Closed Lost', value: 'closed_lost' },
  { label: 'On Hold', value: 'on_hold' }
]

export const FEATURE_CATEGORIES = [
  { label: 'Dashboard', value: 'dashboard' },
  { label: 'Search', value: 'search' },
  { label: 'Property', value: 'property' },
  { label: 'Contact', value: 'contact' }
]
