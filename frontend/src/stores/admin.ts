import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { adminApi, usersApi, agentsApi, crmApi } from '@/services/adminService'
import type {
  User,
  UserList,
  UserStats,
  Agent,
  AgentList,
  AgentStats,
  AdminDashboardStats,
  CRMDashboardStats,
  FeatureSetting,
  ActivityLog,
  Task,
  Pipeline,
  Interaction,
  PipelineStats
} from '@/types/admin'

// Admin email for authorization check
const ADMIN_EMAIL = 'stailor45@gmail.com'

export const useAdminStore = defineStore('admin', () => {
  // State
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Dashboard Stats
  const dashboardStats = ref<AdminDashboardStats | null>(null)
  const crmStats = ref<CRMDashboardStats | null>(null)

  // Users
  const users = ref<User[]>([])
  const userStats = ref<UserStats | null>(null)
  const totalUsers = ref(0)
  const currentUser = ref<User | null>(null)

  // Agents
  const agents = ref<Agent[]>([])
  const agentStats = ref<AgentStats | null>(null)
  const totalAgents = ref(0)
  const currentAgent = ref<Agent | null>(null)

  // Features
  const features = ref<FeatureSetting[]>([])

  // Activity
  const recentActivity = ref<ActivityLog[]>([])

  // CRM
  const tasks = ref<Task[]>([])
  const pipelines = ref<Pipeline[]>([])
  const pipelineStats = ref<PipelineStats | null>(null)
  const interactions = ref<Interaction[]>([])

  // Computed
  const activeUsers = computed(() => users.value.filter(u => u.status === 'active'))
  const activeAgents = computed(() => agents.value.filter(a => a.status === 'active'))
  const enabledFeatures = computed(() => features.value.filter(f => f.is_enabled))

  // Check if current user is admin
  const isAdmin = (email?: string) => {
    return email === ADMIN_EMAIL
  }

  // ================== Dashboard Actions ==================

  const fetchDashboardStats = async () => {
    try {
      loading.value = true
      error.value = null
      dashboardStats.value = await adminApi.getDashboardStats()
    } catch (err: any) {
      error.value = err.message
      console.error('Failed to fetch dashboard stats:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCRMStats = async () => {
    try {
      crmStats.value = await crmApi.getCRMStats()
    } catch (err: any) {
      console.error('Failed to fetch CRM stats:', err)
    }
  }

  const fetchRecentActivity = async (limit = 10) => {
    try {
      const data = await adminApi.getRecentActivity(limit)
      recentActivity.value = data.activities
    } catch (err: any) {
      console.error('Failed to fetch recent activity:', err)
    }
  }

  // ================== User Actions ==================

  const fetchUsers = async (params?: {
    status?: string
    role?: string
    search?: string
    limit?: number
    offset?: number
  }) => {
    try {
      loading.value = true
      error.value = null
      const data: UserList = await usersApi.getUsers(params)
      users.value = data.users
      totalUsers.value = data.total
    } catch (err: any) {
      error.value = err.message
      console.error('Failed to fetch users:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchUserStats = async () => {
    try {
      userStats.value = await usersApi.getUserStats()
    } catch (err: any) {
      console.error('Failed to fetch user stats:', err)
    }
  }

  const fetchUser = async (userId: string) => {
    try {
      loading.value = true
      currentUser.value = await usersApi.getUser(userId)
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (userId: string, data: Partial<User>) => {
    try {
      loading.value = true
      const updated = await usersApi.updateUser(userId, data)
      const index = users.value.findIndex(u => u.id === userId)
      if (index !== -1) {
        users.value[index] = updated
      }
      if (currentUser.value?.id === userId) {
        currentUser.value = updated
      }
      return updated
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUserStatus = async (userId: string, status: string) => {
    try {
      await usersApi.updateUserStatus(userId, status)
      const index = users.value.findIndex(u => u.id === userId)
      if (index !== -1) {
        users.value[index].status = status as any
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  const assignAgentToUser = async (userId: string, agentId: string) => {
    try {
      await usersApi.assignAgentToUser(userId, agentId)
      const index = users.value.findIndex(u => u.id === userId)
      if (index !== -1) {
        users.value[index].assigned_agent_id = agentId
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  // ================== Agent Actions ==================

  const fetchAgents = async (params?: {
    status?: string
    role?: string
    search?: string
    limit?: number
    offset?: number
  }) => {
    try {
      loading.value = true
      error.value = null
      const data: AgentList = await agentsApi.getAgents(params)
      agents.value = data.agents
      totalAgents.value = data.total
    } catch (err: any) {
      error.value = err.message
      console.error('Failed to fetch agents:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchAgentStats = async () => {
    try {
      agentStats.value = await agentsApi.getAgentStats()
    } catch (err: any) {
      console.error('Failed to fetch agent stats:', err)
    }
  }

  const fetchAgent = async (agentId: string) => {
    try {
      loading.value = true
      currentAgent.value = await agentsApi.getAgent(agentId)
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createAgent = async (data: Partial<Agent>) => {
    try {
      loading.value = true
      const newAgent = await agentsApi.createAgent(data)
      agents.value.unshift(newAgent)
      totalAgents.value++
      return newAgent
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateAgent = async (agentId: string, data: Partial<Agent>) => {
    try {
      loading.value = true
      const updated = await agentsApi.updateAgent(agentId, data)
      const index = agents.value.findIndex(a => a.id === agentId)
      if (index !== -1) {
        agents.value[index] = updated
      }
      if (currentAgent.value?.id === agentId) {
        currentAgent.value = updated
      }
      return updated
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateAgentStatus = async (agentId: string, status: string) => {
    try {
      await agentsApi.updateAgentStatus(agentId, status)
      const index = agents.value.findIndex(a => a.id === agentId)
      if (index !== -1) {
        agents.value[index].status = status as any
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  const deleteAgent = async (agentId: string) => {
    try {
      await agentsApi.deleteAgent(agentId)
      agents.value = agents.value.filter(a => a.id !== agentId)
      totalAgents.value--
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  // ================== Feature Actions ==================

  const fetchFeatures = async (category?: string) => {
    try {
      loading.value = true
      const data = await adminApi.getFeatures({ category })
      features.value = data.features
    } catch (err: any) {
      error.value = err.message
      console.error('Failed to fetch features:', err)
    } finally {
      loading.value = false
    }
  }

  const toggleFeature = async (featureKey: string, isEnabled: boolean, enabledBy?: string) => {
    try {
      const updated = await adminApi.toggleFeature(featureKey, isEnabled, enabledBy)
      const index = features.value.findIndex(f => f.feature_key === featureKey)
      if (index !== -1) {
        features.value[index] = updated
      }
      return updated
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  const seedDefaultFeatures = async () => {
    try {
      await adminApi.seedDefaultFeatures()
      await fetchFeatures()
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  // ================== CRM Actions ==================

  const fetchTasks = async (params?: {
    customer_id?: string
    assigned_agent_id?: string
    status?: string
    priority?: string
  }) => {
    try {
      loading.value = true
      const data = await crmApi.getTasks(params)
      tasks.value = data.tasks
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createTask = async (data: any) => {
    try {
      const task = await crmApi.createTask(data)
      tasks.value.unshift(task)
      return task
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  const completeTask = async (taskId: string) => {
    try {
      await crmApi.completeTask(taskId)
      const index = tasks.value.findIndex(t => t.id === taskId)
      if (index !== -1) {
        tasks.value[index].status = 'completed'
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  const fetchPipeline = async (params?: { stage?: string; assigned_agent_id?: string }) => {
    try {
      loading.value = true
      const data = await crmApi.getPipeline(params)
      pipelines.value = data.pipelines
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const fetchPipelineStats = async () => {
    try {
      pipelineStats.value = await crmApi.getPipelineStats()
    } catch (err: any) {
      console.error('Failed to fetch pipeline stats:', err)
    }
  }

  const updatePipelineStage = async (customerId: string, stage: string) => {
    try {
      await crmApi.updateCustomerStage(customerId, stage)
      const index = pipelines.value.findIndex(p => p.customer_id === customerId)
      if (index !== -1) {
        pipelines.value[index].stage = stage as any
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  const fetchInteractions = async (params?: { customer_id?: string; agent_id?: string }) => {
    try {
      const data = await crmApi.getInteractions(params)
      interactions.value = data.interactions
    } catch (err: any) {
      error.value = err.message
    }
  }

  const createInteraction = async (data: any) => {
    try {
      const interaction = await crmApi.createInteraction(data)
      interactions.value.unshift(interaction)
      return interaction
    } catch (err: any) {
      error.value = err.message
      throw err
    }
  }

  // Reset store
  const reset = () => {
    loading.value = false
    error.value = null
    dashboardStats.value = null
    crmStats.value = null
    users.value = []
    userStats.value = null
    totalUsers.value = 0
    currentUser.value = null
    agents.value = []
    agentStats.value = null
    totalAgents.value = 0
    currentAgent.value = null
    features.value = []
    recentActivity.value = []
    tasks.value = []
    pipelines.value = []
    pipelineStats.value = null
    interactions.value = []
  }

  return {
    // State
    loading,
    error,
    dashboardStats,
    crmStats,
    users,
    userStats,
    totalUsers,
    currentUser,
    agents,
    agentStats,
    totalAgents,
    currentAgent,
    features,
    recentActivity,
    tasks,
    pipelines,
    pipelineStats,
    interactions,

    // Computed
    activeUsers,
    activeAgents,
    enabledFeatures,

    // Methods
    isAdmin,
    fetchDashboardStats,
    fetchCRMStats,
    fetchRecentActivity,
    fetchUsers,
    fetchUserStats,
    fetchUser,
    updateUser,
    updateUserStatus,
    assignAgentToUser,
    fetchAgents,
    fetchAgentStats,
    fetchAgent,
    createAgent,
    updateAgent,
    updateAgentStatus,
    deleteAgent,
    fetchFeatures,
    toggleFeature,
    seedDefaultFeatures,
    fetchTasks,
    createTask,
    completeTask,
    fetchPipeline,
    fetchPipelineStats,
    updatePipelineStage,
    fetchInteractions,
    createInteraction,
    reset
  }
})
