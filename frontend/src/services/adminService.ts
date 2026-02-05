/**
 * Admin API Service
 * Handles all API calls for admin dashboard, users, agents, CRM, and features
 */

const API_BASE = 'http://localhost:8000'

// ================== Users API ==================

export const usersApi = {
  async getUsers(params?: {
    status?: string
    role?: string
    assigned_agent_id?: string
    search?: string
    limit?: number
    offset?: number
  }) {
    const searchParams = new URLSearchParams()
    if (params?.status) searchParams.append('status', params.status)
    if (params?.role) searchParams.append('role', params.role)
    if (params?.assigned_agent_id) searchParams.append('assigned_agent_id', params.assigned_agent_id)
    if (params?.search) searchParams.append('search', params.search)
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE}/api/users/?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch users')
    return response.json()
  },

  async getUser(userId: string) {
    const response = await fetch(`${API_BASE}/api/users/${userId}`)
    if (!response.ok) throw new Error('Failed to fetch user')
    return response.json()
  },

  async getUserByFirebaseUid(firebaseUid: string) {
    const response = await fetch(`${API_BASE}/api/users/firebase/${firebaseUid}`)
    if (!response.ok) throw new Error('Failed to fetch user')
    return response.json()
  },

  async getUserStats() {
    const response = await fetch(`${API_BASE}/api/users/stats`)
    if (!response.ok) throw new Error('Failed to fetch user stats')
    return response.json()
  },

  async createUser(data: any) {
    const response = await fetch(`${API_BASE}/api/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create user')
    return response.json()
  },

  async syncUser(data: any) {
    const response = await fetch(`${API_BASE}/api/users/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to sync user')
    return response.json()
  },

  async updateUser(userId: string, data: any) {
    const response = await fetch(`${API_BASE}/api/users/${userId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to update user')
    return response.json()
  },

  async updateUserStatus(userId: string, status: string) {
    const response = await fetch(`${API_BASE}/api/users/${userId}/status?status=${status}`, {
      method: 'PATCH'
    })
    if (!response.ok) throw new Error('Failed to update user status')
    return response.json()
  },

  async assignAgentToUser(userId: string, agentId: string) {
    const response = await fetch(`${API_BASE}/api/users/${userId}/assign-agent?agent_id=${agentId}`, {
      method: 'PATCH'
    })
    if (!response.ok) throw new Error('Failed to assign agent')
    return response.json()
  },

  async deleteUser(userId: string) {
    const response = await fetch(`${API_BASE}/api/users/${userId}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete user')
    return response.json()
  }
}

// ================== Agents API ==================

export const agentsApi = {
  async getAgents(params?: {
    status?: string
    role?: string
    is_admin?: boolean
    search?: string
    limit?: number
    offset?: number
  }) {
    const searchParams = new URLSearchParams()
    if (params?.status) searchParams.append('status', params.status)
    if (params?.role) searchParams.append('role', params.role)
    if (params?.is_admin !== undefined) searchParams.append('is_admin', params.is_admin.toString())
    if (params?.search) searchParams.append('search', params.search)
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE}/api/agents/?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch agents')
    return response.json()
  },

  async getAgent(agentId: string) {
    const response = await fetch(`${API_BASE}/api/agents/${agentId}`)
    if (!response.ok) throw new Error('Failed to fetch agent')
    return response.json()
  },

  async getAgentStats() {
    const response = await fetch(`${API_BASE}/api/agents/stats`)
    if (!response.ok) throw new Error('Failed to fetch agent stats')
    return response.json()
  },

  async createAgent(data: any) {
    const response = await fetch(`${API_BASE}/api/agents/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create agent')
    return response.json()
  },

  async updateAgent(agentId: string, data: any) {
    const response = await fetch(`${API_BASE}/api/agents/${agentId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to update agent')
    return response.json()
  },

  async updateAgentStatus(agentId: string, status: string) {
    const response = await fetch(`${API_BASE}/api/agents/${agentId}/status?status=${status}`, {
      method: 'PATCH'
    })
    if (!response.ok) throw new Error('Failed to update agent status')
    return response.json()
  },

  async assignCustomerToAgent(customerId: string, agentId: string, notes?: string) {
    const response = await fetch(`${API_BASE}/api/agents/assign-customer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_id: customerId, agent_id: agentId, notes })
    })
    if (!response.ok) throw new Error('Failed to assign customer')
    return response.json()
  },

  async getAgentCustomers(agentId: string, limit = 20, offset = 0) {
    const response = await fetch(
      `${API_BASE}/api/agents/${agentId}/customers?limit=${limit}&offset=${offset}`
    )
    if (!response.ok) throw new Error('Failed to fetch agent customers')
    return response.json()
  },

  async deleteAgent(agentId: string) {
    const response = await fetch(`${API_BASE}/api/agents/${agentId}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete agent')
    return response.json()
  }
}

// ================== CRM API ==================

export const crmApi = {
  // Interactions
  async getInteractions(params?: {
    customer_id?: string
    agent_id?: string
    interaction_type?: string
    limit?: number
    offset?: number
  }) {
    const searchParams = new URLSearchParams()
    if (params?.customer_id) searchParams.append('customer_id', params.customer_id)
    if (params?.agent_id) searchParams.append('agent_id', params.agent_id)
    if (params?.interaction_type) searchParams.append('interaction_type', params.interaction_type)
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE}/api/crm/interactions?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch interactions')
    return response.json()
  },

  async createInteraction(data: any) {
    const response = await fetch(`${API_BASE}/api/crm/interactions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create interaction')
    return response.json()
  },

  async updateInteraction(interactionId: string, data: any) {
    const response = await fetch(`${API_BASE}/api/crm/interactions/${interactionId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to update interaction')
    return response.json()
  },

  async deleteInteraction(interactionId: string) {
    const response = await fetch(`${API_BASE}/api/crm/interactions/${interactionId}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete interaction')
    return response.json()
  },

  // Notes
  async getNotes(params?: {
    customer_id?: string
    agent_id?: string
    category?: string
    is_pinned?: boolean
    limit?: number
    offset?: number
  }) {
    const searchParams = new URLSearchParams()
    if (params?.customer_id) searchParams.append('customer_id', params.customer_id)
    if (params?.agent_id) searchParams.append('agent_id', params.agent_id)
    if (params?.category) searchParams.append('category', params.category)
    if (params?.is_pinned !== undefined) searchParams.append('is_pinned', params.is_pinned.toString())
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE}/api/crm/notes?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch notes')
    return response.json()
  },

  async createNote(data: any) {
    const response = await fetch(`${API_BASE}/api/crm/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create note')
    return response.json()
  },

  async updateNote(noteId: string, data: any) {
    const response = await fetch(`${API_BASE}/api/crm/notes/${noteId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to update note')
    return response.json()
  },

  async deleteNote(noteId: string) {
    const response = await fetch(`${API_BASE}/api/crm/notes/${noteId}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete note')
    return response.json()
  },

  // Tasks
  async getTasks(params?: {
    customer_id?: string
    assigned_agent_id?: string
    status?: string
    priority?: string
    limit?: number
    offset?: number
  }) {
    const searchParams = new URLSearchParams()
    if (params?.customer_id) searchParams.append('customer_id', params.customer_id)
    if (params?.assigned_agent_id) searchParams.append('assigned_agent_id', params.assigned_agent_id)
    if (params?.status) searchParams.append('status', params.status)
    if (params?.priority) searchParams.append('priority', params.priority)
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE}/api/crm/tasks?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch tasks')
    return response.json()
  },

  async getOverdueTasks(agentId?: string) {
    const params = agentId ? `?assigned_agent_id=${agentId}` : ''
    const response = await fetch(`${API_BASE}/api/crm/tasks/overdue${params}`)
    if (!response.ok) throw new Error('Failed to fetch overdue tasks')
    return response.json()
  },

  async createTask(data: any) {
    const response = await fetch(`${API_BASE}/api/crm/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create task')
    return response.json()
  },

  async updateTask(taskId: string, data: any) {
    const response = await fetch(`${API_BASE}/api/crm/tasks/${taskId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to update task')
    return response.json()
  },

  async completeTask(taskId: string) {
    const response = await fetch(`${API_BASE}/api/crm/tasks/${taskId}/complete`, {
      method: 'PATCH'
    })
    if (!response.ok) throw new Error('Failed to complete task')
    return response.json()
  },

  async deleteTask(taskId: string) {
    const response = await fetch(`${API_BASE}/api/crm/tasks/${taskId}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete task')
    return response.json()
  },

  // Pipeline
  async getPipeline(params?: {
    stage?: string
    assigned_agent_id?: string
    limit?: number
    offset?: number
  }) {
    const searchParams = new URLSearchParams()
    if (params?.stage) searchParams.append('stage', params.stage)
    if (params?.assigned_agent_id) searchParams.append('assigned_agent_id', params.assigned_agent_id)
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE}/api/crm/pipeline?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch pipeline')
    return response.json()
  },

  async getPipelineStats() {
    const response = await fetch(`${API_BASE}/api/crm/pipeline/stats`)
    if (!response.ok) throw new Error('Failed to fetch pipeline stats')
    return response.json()
  },

  async createPipelineEntry(data: any) {
    const response = await fetch(`${API_BASE}/api/crm/pipeline`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create pipeline entry')
    return response.json()
  },

  async updatePipeline(pipelineId: string, data: any) {
    const response = await fetch(`${API_BASE}/api/crm/pipeline/${pipelineId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to update pipeline')
    return response.json()
  },

  async updateCustomerStage(customerId: string, stage: string) {
    const response = await fetch(
      `${API_BASE}/api/crm/pipeline/customer/${customerId}/stage?stage=${stage}`,
      { method: 'PATCH' }
    )
    if (!response.ok) throw new Error('Failed to update pipeline stage')
    return response.json()
  },

  // Stats
  async getCRMStats() {
    const response = await fetch(`${API_BASE}/api/crm/stats`)
    if (!response.ok) throw new Error('Failed to fetch CRM stats')
    return response.json()
  }
}

// ================== Admin API ==================

export const adminApi = {
  async getDashboardStats() {
    const response = await fetch(`${API_BASE}/api/admin/stats`)
    if (!response.ok) throw new Error('Failed to fetch dashboard stats')
    return response.json()
  },

  // Features
  async getFeatures(params?: { category?: string; is_enabled?: boolean }) {
    const searchParams = new URLSearchParams()
    if (params?.category) searchParams.append('category', params.category)
    if (params?.is_enabled !== undefined) searchParams.append('is_enabled', params.is_enabled.toString())

    const response = await fetch(`${API_BASE}/api/admin/features?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch features')
    return response.json()
  },

  async getFeature(featureKey: string) {
    const response = await fetch(`${API_BASE}/api/admin/features/${featureKey}`)
    if (!response.ok) throw new Error('Failed to fetch feature')
    return response.json()
  },

  async createFeature(data: any) {
    const response = await fetch(`${API_BASE}/api/admin/features`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create feature')
    return response.json()
  },

  async updateFeature(featureKey: string, data: any) {
    const response = await fetch(`${API_BASE}/api/admin/features/${featureKey}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to update feature')
    return response.json()
  },

  async toggleFeature(featureKey: string, isEnabled: boolean, enabledBy?: string) {
    const response = await fetch(`${API_BASE}/api/admin/features/${featureKey}/toggle`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_enabled: isEnabled, enabled_by: enabledBy })
    })
    if (!response.ok) throw new Error('Failed to toggle feature')
    return response.json()
  },

  async deleteFeature(featureKey: string) {
    const response = await fetch(`${API_BASE}/api/admin/features/${featureKey}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete feature')
    return response.json()
  },

  async seedDefaultFeatures() {
    const response = await fetch(`${API_BASE}/api/admin/features/seed`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('Failed to seed features')
    return response.json()
  },

  // Activity Logs
  async getActivityLogs(params?: {
    actor_id?: string
    actor_type?: string
    action?: string
    action_category?: string
    limit?: number
    offset?: number
  }) {
    const searchParams = new URLSearchParams()
    if (params?.actor_id) searchParams.append('actor_id', params.actor_id)
    if (params?.actor_type) searchParams.append('actor_type', params.actor_type)
    if (params?.action) searchParams.append('action', params.action)
    if (params?.action_category) searchParams.append('action_category', params.action_category)
    if (params?.limit) searchParams.append('limit', params.limit.toString())
    if (params?.offset) searchParams.append('offset', params.offset.toString())

    const response = await fetch(`${API_BASE}/api/admin/activity?${searchParams}`)
    if (!response.ok) throw new Error('Failed to fetch activity logs')
    return response.json()
  },

  async getRecentActivity(limit = 10) {
    const response = await fetch(`${API_BASE}/api/admin/activity/recent?limit=${limit}`)
    if (!response.ok) throw new Error('Failed to fetch recent activity')
    return response.json()
  },

  async createActivityLog(data: any) {
    const response = await fetch(`${API_BASE}/api/admin/activity`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create activity log')
    return response.json()
  }
}
