<template>
  <div class="admin-page">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-logo">
        <span>Tailor</span> Admin
      </div>
      <nav class="sidebar-nav">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="currentTab = tab.id"
          :class="{ active: currentTab === tab.id }"
          class="nav-btn"
        >
          <component :is="tab.icon" class="nav-icon" />
          {{ tab.label }}
        </button>
      </nav>
      <div class="sidebar-footer">
        <div class="admin-user">
          <div class="admin-avatar">{{ userInitials }}</div>
          <div class="admin-info">
            <div class="admin-name">{{ userName }}</div>
            <div class="admin-role">Administrator</div>
          </div>
        </div>
        <router-link :to="{ name: 'dashboard' }" class="back-link">
          ← Back to App
        </router-link>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="admin-main">
      <div class="content-wrapper">

        <!-- OVERVIEW TAB -->
        <div v-if="currentTab === 'overview'" class="tab-content">
          <h1 class="page-title">Dashboard Overview</h1>

          <!-- Stats Grid -->
          <div class="stats-grid">
            <div class="stat-box">
              <div class="stat-icon customers-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              </div>
              <div class="stat-content">
                <div class="stat-label">Total Customers</div>
                <div class="stat-value">{{ dashboardStats?.total_customers || 0 }}</div>
                <div class="stat-change positive">{{ dashboardStats?.active_customers || 0 }} active</div>
              </div>
            </div>
            <div class="stat-box">
              <div class="stat-icon agents-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              </div>
              <div class="stat-content">
                <div class="stat-label">Agents</div>
                <div class="stat-value">{{ dashboardStats?.total_agents || 0 }}</div>
                <div class="stat-change positive">{{ dashboardStats?.active_agents || 0 }} active</div>
              </div>
            </div>
            <div class="stat-box">
              <div class="stat-icon inquiries-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
              </div>
              <div class="stat-content">
                <div class="stat-label">Inquiries</div>
                <div class="stat-value">{{ dashboardStats?.total_inquiries || 0 }}</div>
                <div class="stat-change highlight">{{ dashboardStats?.new_inquiries || 0 }} new</div>
              </div>
            </div>
            <div class="stat-box">
              <div class="stat-icon leads-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
              </div>
              <div class="stat-content">
                <div class="stat-label">Leads This Month</div>
                <div class="stat-value">{{ dashboardStats?.leads_this_month || 0 }}</div>
                <div class="stat-change positive">{{ dashboardStats?.conversions_this_month || 0 }} converted</div>
              </div>
            </div>
          </div>

          <!-- CRM Quick Stats -->
          <div class="stats-grid small">
            <div class="stat-box-small">
              <div class="stat-value-small">{{ crmStats?.pending_tasks || 0 }}</div>
              <div class="stat-label-small">Pending Tasks</div>
            </div>
            <div class="stat-box-small warning">
              <div class="stat-value-small">{{ crmStats?.overdue_tasks || 0 }}</div>
              <div class="stat-label-small">Overdue Tasks</div>
            </div>
            <div class="stat-box-small">
              <div class="stat-value-small">{{ crmStats?.follow_ups_due || 0 }}</div>
              <div class="stat-label-small">Follow-ups Due</div>
            </div>
            <div class="stat-box-small highlight">
              <div class="stat-value-small">${{ formatNumber(crmStats?.pipeline_value || 0) }}</div>
              <div class="stat-label-small">Pipeline Value</div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="panel">
            <div class="panel-header">
              <h2>Recent Activity</h2>
            </div>
            <div class="activity-list" v-if="recentActivity.length">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-icon" :class="getActivityClass(activity.action)">
                  {{ getActivityIcon(activity.action) }}
                </div>
                <div class="activity-content">
                  <div class="activity-text">
                    <strong>{{ activity.actor_email || 'System' }}</strong>
                    {{ activity.description || activity.action }}
                  </div>
                  <div class="activity-time">{{ formatTime(activity.created_at) }}</div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>No recent activity</p>
            </div>
          </div>
        </div>

        <!-- CUSTOMERS TAB -->
        <div v-if="currentTab === 'customers'" class="tab-content">
          <div class="page-header">
            <h1 class="page-title">Customer Management</h1>
            <div class="header-actions">
              <input
                v-model="customerSearch"
                type="text"
                placeholder="Search customers..."
                class="search-input"
                @input="debouncedSearchCustomers"
              />
              <select v-model="customerStatusFilter" class="filter-select" @change="fetchCustomers">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="pending">Pending</option>
              </select>
            </div>
          </div>

          <!-- Customer Stats -->
          <div class="mini-stats">
            <div class="mini-stat">
              <span class="mini-value">{{ userStats?.total_users || 0 }}</span>
              <span class="mini-label">Total</span>
            </div>
            <div class="mini-stat active">
              <span class="mini-value">{{ userStats?.active_users || 0 }}</span>
              <span class="mini-label">Active</span>
            </div>
            <div class="mini-stat">
              <span class="mini-value">{{ userStats?.new_users_this_month || 0 }}</span>
              <span class="mini-label">This Month</span>
            </div>
          </div>

          <!-- Customers Table -->
          <div class="panel">
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Customer</th>
                    <th>Contact</th>
                    <th>Status</th>
                    <th>Agent</th>
                    <th>Activity</th>
                    <th>Joined</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.id">
                    <td>
                      <div class="user-cell">
                        <div class="user-avatar">{{ getInitials(user.full_name || user.email) }}</div>
                        <div class="user-info">
                          <div class="user-name">{{ user.full_name || 'No Name' }}</div>
                          <div class="user-email">{{ user.email }}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="contact-info">
                        <div v-if="user.phone">{{ user.phone }}</div>
                        <div class="text-muted" v-else>No phone</div>
                      </div>
                    </td>
                    <td>
                      <span :class="['status-badge', `status-${user.status}`]">
                        {{ user.status }}
                      </span>
                    </td>
                    <td>
                      <span v-if="user.assigned_agent_id" class="agent-assigned">
                        Assigned
                      </span>
                      <button v-else class="btn-link" @click="openAssignAgent(user)">
                        Assign
                      </button>
                    </td>
                    <td>
                      <div class="activity-stats">
                        <span title="Searches">{{ user.search_count }} searches</span>
                        <span title="Saved">{{ user.saved_properties_count }} saved</span>
                      </div>
                    </td>
                    <td>{{ formatDate(user.created_at) }}</td>
                    <td>
                      <div class="action-buttons">
                        <button class="btn-icon" @click="viewCustomer(user)" title="View">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                        </button>
                        <button class="btn-icon" @click="editCustomer(user)" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                        </button>
                        <button
                          class="btn-icon"
                          :class="{ 'text-danger': user.status === 'active' }"
                          @click="toggleUserStatus(user)"
                          :title="user.status === 'active' ? 'Deactivate' : 'Activate'"
                        >
                          <svg v-if="user.status === 'active'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" /></svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="!users.length && !loading">
                    <td colspan="7" class="empty-cell">No customers found</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-if="loading" class="loading-overlay">
              <div class="spinner"></div>
            </div>
          </div>
        </div>

        <!-- AGENTS TAB -->
        <div v-if="currentTab === 'agents'" class="tab-content">
          <div class="page-header">
            <h1 class="page-title">Agent Management</h1>
            <div class="header-actions">
              <input
                v-model="agentSearch"
                type="text"
                placeholder="Search agents..."
                class="search-input"
                @input="debouncedSearchAgents"
              />
              <button class="btn-primary" @click="showAddAgentModal = true">
                + Add Agent
              </button>
            </div>
          </div>

          <!-- Agent Stats -->
          <div class="mini-stats">
            <div class="mini-stat">
              <span class="mini-value">{{ agentStats?.total_agents || 0 }}</span>
              <span class="mini-label">Total Agents</span>
            </div>
            <div class="mini-stat active">
              <span class="mini-value">{{ agentStats?.active_agents || 0 }}</span>
              <span class="mini-label">Active</span>
            </div>
            <div class="mini-stat">
              <span class="mini-value">{{ agentStats?.total_closed_deals || 0 }}</span>
              <span class="mini-label">Total Deals</span>
            </div>
            <div class="mini-stat highlight">
              <span class="mini-value">{{ agentStats?.total_customers_managed || 0 }}</span>
              <span class="mini-label">Customers Managed</span>
            </div>
          </div>

          <!-- Agents Table -->
          <div class="panel">
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Agent</th>
                    <th>Contact</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Customers</th>
                    <th>Deals</th>
                    <th>Rating</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="agent in agents" :key="agent.id">
                    <td>
                      <div class="user-cell">
                        <div class="user-avatar agent">{{ getInitials(agent.full_name) }}</div>
                        <div class="user-info">
                          <div class="user-name">{{ agent.full_name }}</div>
                          <div class="user-email">{{ agent.title || agent.email }}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="contact-info">
                        <div>{{ agent.email }}</div>
                        <div v-if="agent.phone" class="text-muted">{{ agent.phone }}</div>
                      </div>
                    </td>
                    <td>
                      <span class="role-badge">{{ formatRole(agent.role) }}</span>
                    </td>
                    <td>
                      <span :class="['status-badge', `status-${agent.status}`]">
                        {{ agent.status }}
                      </span>
                    </td>
                    <td>
                      <div class="capacity-info">
                        <span>{{ agent.active_customers }}/{{ agent.max_customers }}</span>
                        <div class="capacity-bar">
                          <div
                            class="capacity-fill"
                            :style="{ width: (agent.active_customers / agent.max_customers * 100) + '%' }"
                            :class="{ warning: agent.active_customers / agent.max_customers > 0.8 }"
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td>{{ agent.closed_deals }}</td>
                    <td>
                      <div class="rating">
                        <span class="rating-value">{{ agent.rating?.toFixed(1) || '0.0' }}</span>
                        <span class="rating-star">★</span>
                      </div>
                    </td>
                    <td>
                      <div class="action-buttons">
                        <button class="btn-icon" @click="viewAgent(agent)" title="View">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                        </button>
                        <button class="btn-icon" @click="editAgent(agent)" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                        </button>
                        <button
                          class="btn-icon text-danger"
                          @click="confirmDeleteAgent(agent)"
                          title="Delete"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="!agents.length && !loading">
                    <td colspan="8" class="empty-cell">No agents found. Add your first agent!</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Top Performers -->
          <div class="panel" v-if="agentStats?.top_performers?.length">
            <div class="panel-header">
              <h2>Top Performers</h2>
            </div>
            <div class="performers-grid">
              <div v-for="(performer, index) in agentStats.top_performers" :key="performer.id" class="performer-card">
                <div class="performer-rank">#{{ index + 1 }}</div>
                <div class="performer-name">{{ performer.name }}</div>
                <div class="performer-stats">
                  <span>{{ performer.closed_deals }} deals</span>
                  <span>{{ performer.rating?.toFixed(1) }} ★</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- CRM TAB -->
        <div v-if="currentTab === 'crm'" class="tab-content">
          <div class="page-header">
            <h1 class="page-title">Customer Relationship Manager</h1>
            <div class="header-actions">
              <button class="btn-secondary" @click="crmSubTab = 'tasks'" :class="{ active: crmSubTab === 'tasks' }">Tasks</button>
              <button class="btn-secondary" @click="crmSubTab = 'interactions'" :class="{ active: crmSubTab === 'interactions' }">Interactions</button>
              <button class="btn-secondary" @click="crmSubTab = 'pipeline'" :class="{ active: crmSubTab === 'pipeline' }">Pipeline</button>
            </div>
          </div>

          <!-- CRM Stats -->
          <div class="mini-stats">
            <div class="mini-stat">
              <span class="mini-value">{{ crmStats?.total_interactions || 0 }}</span>
              <span class="mini-label">Total Interactions</span>
            </div>
            <div class="mini-stat warning" v-if="crmStats?.overdue_tasks">
              <span class="mini-value">{{ crmStats?.overdue_tasks || 0 }}</span>
              <span class="mini-label">Overdue Tasks</span>
            </div>
            <div class="mini-stat">
              <span class="mini-value">{{ crmStats?.customers_in_pipeline || 0 }}</span>
              <span class="mini-label">In Pipeline</span>
            </div>
            <div class="mini-stat highlight">
              <span class="mini-value">${{ formatNumber(crmStats?.pipeline_value || 0) }}</span>
              <span class="mini-label">Pipeline Value</span>
            </div>
          </div>

          <!-- Tasks Sub-Tab -->
          <div v-if="crmSubTab === 'tasks'" class="panel">
            <div class="panel-header">
              <h2>Tasks</h2>
              <button class="btn-primary btn-sm" @click="showAddTaskModal = true">+ Add Task</button>
            </div>
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Task</th>
                    <th>Customer</th>
                    <th>Assigned To</th>
                    <th>Priority</th>
                    <th>Due Date</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="task in tasks" :key="task.id" :class="{ overdue: isOverdue(task) }">
                    <td>
                      <div class="task-title">{{ task.title }}</div>
                      <div class="task-desc" v-if="task.description">{{ task.description }}</div>
                    </td>
                    <td>{{ task.customer_name || '-' }}</td>
                    <td>{{ task.assigned_agent_name || 'Unassigned' }}</td>
                    <td>
                      <span :class="['priority-badge', `priority-${task.priority}`]">
                        {{ task.priority }}
                      </span>
                    </td>
                    <td :class="{ 'text-danger': isOverdue(task) }">
                      {{ task.due_date ? formatDate(task.due_date) : '-' }}
                    </td>
                    <td>
                      <span :class="['status-badge', `status-${task.status}`]">
                        {{ task.status }}
                      </span>
                    </td>
                    <td>
                      <div class="action-buttons">
                        <button
                          v-if="task.status !== 'completed'"
                          class="btn-icon text-success"
                          @click="completeTask(task.id)"
                          title="Complete"
                        >
                          ✓
                        </button>
                        <button class="btn-icon" @click="editTask(task)" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="!tasks.length">
                    <td colspan="7" class="empty-cell">No tasks yet</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Interactions Sub-Tab -->
          <div v-if="crmSubTab === 'interactions'" class="panel">
            <div class="panel-header">
              <h2>Recent Interactions</h2>
              <button class="btn-primary btn-sm" @click="showAddInteractionModal = true">+ Log Interaction</button>
            </div>
            <div class="interactions-list">
              <div v-for="interaction in interactions" :key="interaction.id" class="interaction-item">
                <div class="interaction-icon" :class="interaction.interaction_type">
                  {{ getInteractionIcon(interaction.interaction_type) }}
                </div>
                <div class="interaction-content">
                  <div class="interaction-header">
                    <span class="interaction-type">{{ formatInteractionType(interaction.interaction_type) }}</span>
                    <span class="interaction-time">{{ formatTime(interaction.created_at) }}</span>
                  </div>
                  <div class="interaction-customer">{{ interaction.customer_name }}</div>
                  <div class="interaction-desc">{{ interaction.description }}</div>
                  <div class="interaction-outcome" v-if="interaction.outcome">
                    Outcome: <span :class="interaction.outcome">{{ interaction.outcome }}</span>
                  </div>
                </div>
              </div>
              <div v-if="!interactions.length" class="empty-state">
                <p>No interactions logged yet</p>
              </div>
            </div>
          </div>

          <!-- Pipeline Sub-Tab -->
          <div v-if="crmSubTab === 'pipeline'" class="pipeline-view">
            <div class="pipeline-header">
              <h2>Sales Pipeline</h2>
              <div class="pipeline-stats-inline" v-if="pipelineStats">
                <span>{{ pipelineStats.total_leads }} leads</span>
                <span>{{ pipelineStats.conversion_rate?.toFixed(1) }}% conversion</span>
                <span>${{ formatNumber(pipelineStats.total_deal_value) }} total value</span>
              </div>
            </div>
            <div class="pipeline-board">
              <div v-for="stage in pipelineStages" :key="stage.value" class="pipeline-column">
                <div class="pipeline-column-header">
                  <span class="stage-name">{{ stage.label }}</span>
                  <span class="stage-count">{{ getPipelineCountByStage(stage.value) }}</span>
                </div>
                <div class="pipeline-cards">
                  <div
                    v-for="lead in getPipelineByStage(stage.value)"
                    :key="lead.id"
                    class="pipeline-card"
                    @click="viewPipelineLead(lead)"
                  >
                    <div class="lead-name">{{ lead.customer_name }}</div>
                    <div class="lead-email">{{ lead.customer_email }}</div>
                    <div class="lead-value" v-if="lead.deal_value">${{ formatNumber(lead.deal_value) }}</div>
                    <div class="lead-agent" v-if="lead.assigned_agent_name">{{ lead.assigned_agent_name }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FEATURES TAB -->
        <div v-if="currentTab === 'features'" class="tab-content">
          <div class="page-header">
            <h1 class="page-title">Feature Management</h1>
            <div class="header-actions">
              <button class="btn-secondary" @click="seedFeatures">Seed Default Features</button>
            </div>
          </div>

          <p class="page-description">
            Control which features are visible to users on their dashboard. Toggle features on/off to customize the user experience.
          </p>

          <!-- Features by Category -->
          <div v-for="category in featureCategories" :key="category" class="panel">
            <div class="panel-header">
              <h2>{{ formatCategory(category) }} Features</h2>
            </div>
            <div class="features-list">
              <div
                v-for="feature in getFeaturesByCategory(category)"
                :key="feature.feature_key"
                class="feature-item"
              >
                <div class="feature-info">
                  <div class="feature-name">{{ feature.feature_name }}</div>
                  <div class="feature-desc">{{ feature.description }}</div>
                  <div class="feature-key">Key: {{ feature.feature_key }}</div>
                </div>
                <div class="feature-toggle">
                  <label class="toggle-switch">
                    <input
                      type="checkbox"
                      :checked="feature.is_enabled"
                      @change="toggleFeature(feature)"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span class="toggle-label">{{ feature.is_enabled ? 'Enabled' : 'Disabled' }}</span>
                </div>
              </div>
              <div v-if="!getFeaturesByCategory(category).length" class="empty-state">
                <p>No features in this category</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>

    <!-- Add Agent Modal -->
    <div v-if="showAddAgentModal" class="modal-overlay" @click.self="showAddAgentModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingAgent ? 'Edit Agent' : 'Add New Agent' }}</h3>
          <button class="modal-close" @click="showAddAgentModal = false">&times;</button>
        </div>
        <form @submit.prevent="saveAgent" class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>First Name *</label>
              <input v-model="agentForm.first_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Last Name *</label>
              <input v-model="agentForm.last_name" type="text" required />
            </div>
          </div>
          <div class="form-group">
            <label>Email *</label>
            <input v-model="agentForm.email" type="email" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Phone</label>
              <input v-model="agentForm.phone" type="tel" />
            </div>
            <div class="form-group">
              <label>Mobile</label>
              <input v-model="agentForm.mobile" type="tel" />
            </div>
          </div>
          <div class="form-group">
            <label>Title</label>
            <input v-model="agentForm.title" type="text" placeholder="e.g. Senior Real Estate Agent" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Role</label>
              <select v-model="agentForm.role">
                <option value="junior_agent">Junior Agent</option>
                <option value="senior_agent">Senior Agent</option>
                <option value="team_lead">Team Lead</option>
                <option value="manager">Manager</option>
              </select>
            </div>
            <div class="form-group">
              <label>Max Customers</label>
              <input v-model.number="agentForm.max_customers" type="number" min="1" max="500" />
            </div>
          </div>
          <div class="form-group">
            <label>Bio</label>
            <textarea v-model="agentForm.bio" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>
              <input type="checkbox" v-model="agentForm.is_admin" />
              Grant Admin Access
            </label>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-secondary" @click="showAddAgentModal = false">Cancel</button>
            <button type="submit" class="btn-primary" :disabled="savingAgent">
              {{ savingAgent ? 'Saving...' : (editingAgent ? 'Update Agent' : 'Add Agent') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Customer Detail Modal -->
    <div v-if="showCustomerModal" class="modal-overlay" @click.self="showCustomerModal = false">
      <div class="modal modal-lg">
        <div class="modal-header">
          <h3>Customer Details</h3>
          <button class="modal-close" @click="showCustomerModal = false">&times;</button>
        </div>
        <div class="modal-body" v-if="selectedCustomer">
          <div class="customer-detail-grid">
            <div class="detail-section">
              <h4>Basic Information</h4>
              <div class="detail-row">
                <span class="detail-label">Name:</span>
                <span>{{ selectedCustomer.full_name || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Email:</span>
                <span>{{ selectedCustomer.email }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Phone:</span>
                <span>{{ selectedCustomer.phone || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Status:</span>
                <span :class="['status-badge', `status-${selectedCustomer.status}`]">{{ selectedCustomer.status }}</span>
              </div>
            </div>
            <div class="detail-section">
              <h4>Search Preferences</h4>
              <div class="detail-row">
                <span class="detail-label">Budget:</span>
                <span v-if="selectedCustomer.min_budget || selectedCustomer.max_budget">
                  ${{ formatNumber(selectedCustomer.min_budget || 0) }} - ${{ formatNumber(selectedCustomer.max_budget || 0) }}
                </span>
                <span v-else>Not specified</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Beds:</span>
                <span>{{ selectedCustomer.preferred_beds || 'Any' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Timeline:</span>
                <span>{{ selectedCustomer.move_in_timeline || 'Not specified' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Pre-Approved:</span>
                <span>{{ selectedCustomer.pre_approved ? 'Yes' : 'No' }}</span>
              </div>
            </div>
            <div class="detail-section">
              <h4>Activity</h4>
              <div class="detail-row">
                <span class="detail-label">Searches:</span>
                <span>{{ selectedCustomer.search_count }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Saved Properties:</span>
                <span>{{ selectedCustomer.saved_properties_count }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Inquiries:</span>
                <span>{{ selectedCustomer.inquiries_count }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Last Active:</span>
                <span>{{ selectedCustomer.last_active_at ? formatTime(selectedCustomer.last_active_at) : 'Never' }}</span>
              </div>
            </div>
            <div class="detail-section" v-if="selectedCustomer.internal_notes">
              <h4>Internal Notes</h4>
              <p class="notes-content">{{ selectedCustomer.internal_notes }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import type { User, Agent, Task, Pipeline } from '@/types/admin'
import { PIPELINE_STAGE_OPTIONS } from '@/types/admin'

const adminStore = useAdminStore()
const authStore = useAuthStore()

const {
  loading,
  dashboardStats,
  crmStats,
  users,
  userStats,
  agents,
  agentStats,
  features,
  recentActivity,
  tasks,
  pipelines,
  pipelineStats,
  interactions
} = storeToRefs(adminStore)

// Tabs
const tabs = [
  { id: 'overview', label: 'Overview', icon: 'span' },
  { id: 'customers', label: 'Customers', icon: 'span' },
  { id: 'agents', label: 'Agents', icon: 'span' },
  { id: 'crm', label: 'CRM', icon: 'span' },
  { id: 'features', label: 'Features', icon: 'span' }
]

const currentTab = ref('overview')
const crmSubTab = ref('tasks')

// Search & Filters
const customerSearch = ref('')
const customerStatusFilter = ref('')
const agentSearch = ref('')

// Modals
const showAddAgentModal = ref(false)
const showCustomerModal = ref(false)
const showAddTaskModal = ref(false)
const showAddInteractionModal = ref(false)

// Form States
const editingAgent = ref<Agent | null>(null)
const selectedCustomer = ref<User | null>(null)
const savingAgent = ref(false)

const agentForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  mobile: '',
  title: '',
  role: 'junior_agent',
  max_customers: 50,
  bio: '',
  is_admin: false
})

// Pipeline stages
const pipelineStages = PIPELINE_STAGE_OPTIONS.filter(s =>
  !['closed_won', 'closed_lost'].includes(s.value)
)

// Computed
const userName = computed(() => {
  return authStore.user?.displayName || authStore.user?.email?.split('@')[0] || 'Admin'
})

const userInitials = computed(() => {
  const name = userName.value
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const featureCategories = computed(() => {
  const cats = new Set(features.value.map(f => f.category || 'other'))
  return Array.from(cats)
})

// Methods
const formatNumber = (num: number) => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(0) + 'K'
  return num.toString()
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatTime = (date: string) => {
  const d = new Date(date)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}h ago`
  return formatDate(date)
}

const getInitials = (name: string) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const formatRole = (role: string) => {
  return role.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const formatCategory = (cat: string) => {
  return cat.charAt(0).toUpperCase() + cat.slice(1)
}

const formatInteractionType = (type: string) => {
  return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const getActivityClass = (action: string) => {
  if (action.includes('login')) return 'login'
  if (action.includes('create')) return 'create'
  if (action.includes('update')) return 'update'
  return 'default'
}

const getActivityIcon = (action: string) => {
  if (action.includes('login')) return '→'
  if (action.includes('create')) return '+'
  if (action.includes('update')) return '✎'
  return '•'
}

const getInteractionIcon = (type: string) => {
  const icons: Record<string, string> = {
    phone_call: '📞',
    email: '✉️',
    sms: '💬',
    in_person: '🤝',
    video_call: '📹',
    property_tour: '🏠',
    other: '📋'
  }
  return icons[type] || '📋'
}

const isOverdue = (task: Task) => {
  if (!task.due_date || task.status === 'completed') return false
  return new Date(task.due_date) < new Date()
}

const getFeaturesByCategory = (category: string) => {
  return features.value.filter(f => (f.category || 'other') === category)
}

const getPipelineByStage = (stage: string) => {
  return pipelines.value.filter(p => p.stage === stage)
}

const getPipelineCountByStage = (stage: string) => {
  return pipelines.value.filter(p => p.stage === stage).length
}

// Actions
const fetchCustomers = async () => {
  await adminStore.fetchUsers({
    status: customerStatusFilter.value || undefined,
    search: customerSearch.value || undefined,
    role: 'customer'
  })
}

const fetchAgents = async () => {
  await adminStore.fetchAgents({
    search: agentSearch.value || undefined
  })
}

let searchTimeout: number
const debouncedSearchCustomers = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(fetchCustomers, 300) as unknown as number
}

const debouncedSearchAgents = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(fetchAgents, 300) as unknown as number
}

const viewCustomer = (user: User) => {
  selectedCustomer.value = user
  showCustomerModal.value = true
}

const editCustomer = (user: User) => {
  selectedCustomer.value = user
  // Could open edit modal
}

const toggleUserStatus = async (user: User) => {
  const newStatus = user.status === 'active' ? 'inactive' : 'active'
  await adminStore.updateUserStatus(user.id, newStatus)
}

const openAssignAgent = (user: User) => {
  // Could open agent selection modal
}

const viewAgent = (agent: Agent) => {
  // View agent details
}

const editAgent = (agent: Agent) => {
  editingAgent.value = agent
  agentForm.value = {
    first_name: agent.first_name,
    last_name: agent.last_name,
    email: agent.email,
    phone: agent.phone || '',
    mobile: agent.mobile || '',
    title: agent.title || '',
    role: agent.role,
    max_customers: agent.max_customers,
    bio: agent.bio || '',
    is_admin: agent.is_admin
  }
  showAddAgentModal.value = true
}

const saveAgent = async () => {
  savingAgent.value = true
  try {
    if (editingAgent.value) {
      await adminStore.updateAgent(editingAgent.value.id, agentForm.value)
    } else {
      await adminStore.createAgent(agentForm.value)
    }
    showAddAgentModal.value = false
    resetAgentForm()
  } catch (err) {
    console.error('Failed to save agent:', err)
  } finally {
    savingAgent.value = false
  }
}

const confirmDeleteAgent = async (agent: Agent) => {
  if (confirm(`Are you sure you want to remove ${agent.full_name}?`)) {
    await adminStore.deleteAgent(agent.id)
  }
}

const resetAgentForm = () => {
  editingAgent.value = null
  agentForm.value = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    mobile: '',
    title: '',
    role: 'junior_agent',
    max_customers: 50,
    bio: '',
    is_admin: false
  }
}

const completeTask = async (taskId: string) => {
  await adminStore.completeTask(taskId)
}

const editTask = (task: Task) => {
  // Open task edit modal
}

const viewPipelineLead = (lead: Pipeline) => {
  // View lead details
}

const toggleFeature = async (feature: any) => {
  await adminStore.toggleFeature(
    feature.feature_key,
    !feature.is_enabled,
    authStore.user?.email
  )
}

const seedFeatures = async () => {
  await adminStore.seedDefaultFeatures()
}

// Lifecycle
onMounted(async () => {
  // Load initial data
  await Promise.all([
    adminStore.fetchDashboardStats(),
    adminStore.fetchCRMStats(),
    adminStore.fetchRecentActivity(),
    adminStore.fetchUserStats(),
    adminStore.fetchAgentStats(),
    adminStore.fetchFeatures()
  ])
})

// Watch tab changes to load data
watch(currentTab, async (tab) => {
  if (tab === 'customers' && !users.value.length) {
    await fetchCustomers()
  }
  if (tab === 'agents' && !agents.value.length) {
    await fetchAgents()
  }
  if (tab === 'crm') {
    await Promise.all([
      adminStore.fetchTasks(),
      adminStore.fetchPipeline(),
      adminStore.fetchPipelineStats(),
      adminStore.fetchInteractions()
    ])
  }
})

watch(showAddAgentModal, (val) => {
  if (!val) resetAgentForm()
})
</script>

<style scoped>
.admin-page {
  display: flex;
  min-height: 100vh;
  background: #0a0a0a;
}

/* Sidebar */
.admin-sidebar {
  width: 220px;
  background: #111;
  border-right: 1px solid rgba(255,255,255,0.06);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.sidebar-logo {
  padding: 1.5rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.sidebar-logo span {
  color: #D4AF37;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0.5rem;
  overflow-y: auto;
}

.nav-btn {
  width: 100%;
  padding: 0.85rem 1rem;
  margin-bottom: 0.25rem;
  background: transparent;
  border: none;
  color: #9ca3af;
  text-align: left;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-btn:hover {
  background: rgba(255,255,255,0.05);
  color: #fff;
}

.nav-btn.active {
  background: rgba(212, 175, 55, 0.15);
  color: #D4AF37;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.admin-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.admin-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #000;
}

.admin-info {
  flex: 1;
}

.admin-name {
  color: #fff;
  font-size: 0.85rem;
  font-weight: 600;
}

.admin-role {
  color: #6b7280;
  font-size: 0.7rem;
}

.back-link {
  display: block;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.8rem;
  padding: 0.5rem 0;
}

.back-link:hover {
  color: #D4AF37;
}

/* Main Content */
.admin-main {
  flex: 1;
  margin-left: 220px;
  padding: 2rem;
  overflow-y: auto;
  min-height: 100vh;
}

.content-wrapper {
  max-width: 1400px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
  font-family: Georgia, serif;
}

.page-description {
  color: #9ca3af;
  margin-bottom: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stats-grid.small {
  grid-template-columns: repeat(4, 1fr);
}

.stat-box {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.75rem;
  padding: 1.25rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-icon.customers-icon { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.stat-icon.agents-icon { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.stat-icon.inquiries-icon { background: rgba(139, 92, 246, 0.15); color: #a78bfa; }
.stat-icon.leads-icon { background: rgba(212, 175, 55, 0.15); color: #D4AF37; }

.stat-content {
  flex: 1;
}

.stat-label {
  color: #9ca3af;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.stat-value {
  color: #fff;
  font-size: 1.75rem;
  font-weight: 700;
  font-family: Georgia, serif;
  line-height: 1.2;
}

.stat-change {
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.stat-change.positive { color: #10b981; }
.stat-change.highlight { color: #D4AF37; }

/* Small Stats */
.stat-box-small {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
}

.stat-box-small.warning { border-color: rgba(239, 68, 68, 0.3); }
.stat-box-small.highlight { border-color: rgba(212, 175, 55, 0.3); }

.stat-value-small {
  color: #fff;
  font-size: 1.25rem;
  font-weight: 700;
}

.stat-box-small.warning .stat-value-small { color: #ef4444; }
.stat-box-small.highlight .stat-value-small { color: #D4AF37; }

.stat-label-small {
  color: #6b7280;
  font-size: 0.7rem;
  text-transform: uppercase;
}

/* Mini Stats */
.mini-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.mini-stat {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.5rem;
  padding: 0.75rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mini-stat.active { border-color: rgba(16, 185, 129, 0.3); }
.mini-stat.warning { border-color: rgba(239, 68, 68, 0.3); }
.mini-stat.highlight { border-color: rgba(212, 175, 55, 0.3); }

.mini-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
}

.mini-stat.active .mini-value { color: #10b981; }
.mini-stat.warning .mini-value { color: #ef4444; }
.mini-stat.highlight .mini-value { color: #D4AF37; }

.mini-label {
  color: #6b7280;
  font-size: 0.75rem;
}

/* Panel */
.panel {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.panel-header h2 {
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

/* Table */
.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 0.875rem 1rem;
  color: #6b7280;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  background: rgba(0,0,0,0.2);
  white-space: nowrap;
}

.data-table td {
  padding: 0.875rem 1rem;
  color: #d1d5db;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.875rem;
}

.data-table tr:hover td {
  background: rgba(255,255,255,0.02);
}

.data-table tr.overdue td {
  background: rgba(239, 68, 68, 0.05);
}

.empty-cell {
  text-align: center;
  color: #6b7280;
  padding: 2rem !important;
}

/* User Cell */
.user-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 600;
  color: #fff;
  flex-shrink: 0;
}

.user-avatar.agent {
  background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
  color: #000;
}

.user-name {
  color: #fff;
  font-weight: 500;
}

.user-email {
  color: #6b7280;
  font-size: 0.75rem;
}

/* Status Badge */
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-active { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.status-inactive { background: rgba(107, 114, 128, 0.15); color: #9ca3af; }
.status-pending { background: rgba(251, 191, 36, 0.15); color: #fbbf24; }
.status-suspended { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.status-completed { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.status-in_progress { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.status-cancelled { background: rgba(107, 114, 128, 0.15); color: #9ca3af; }

/* Priority Badge */
.priority-badge {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
}

.priority-low { background: rgba(107, 114, 128, 0.15); color: #9ca3af; }
.priority-medium { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.priority-high { background: rgba(251, 191, 36, 0.15); color: #fbbf24; }
.priority-urgent { background: rgba(239, 68, 68, 0.15); color: #f87171; }

/* Role Badge */
.role-badge {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.7rem;
  background: rgba(212, 175, 55, 0.1);
  color: #D4AF37;
}

/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
  color: #000;
  border: none;
  padding: 0.6rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary.btn-sm {
  padding: 0.4rem 0.75rem;
  font-size: 0.75rem;
}

.btn-secondary {
  background: transparent;
  color: #9ca3af;
  border: 1px solid rgba(255,255,255,0.1);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover,
.btn-secondary.active {
  background: rgba(255,255,255,0.05);
  color: #fff;
  border-color: rgba(255,255,255,0.2);
}

.btn-link {
  background: none;
  border: none;
  color: #D4AF37;
  cursor: pointer;
  font-size: 0.8rem;
  text-decoration: underline;
}

.btn-icon {
  background: transparent;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.4rem;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: rgba(255,255,255,0.05);
  color: #fff;
}

.btn-icon.text-success:hover { color: #10b981; }
.btn-icon.text-danger:hover { color: #ef4444; }

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

/* Inputs */
.search-input {
  background: #1a1a1a;
  border: 1px solid rgba(255,255,255,0.1);
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  width: 200px;
}

.search-input:focus {
  outline: none;
  border-color: #D4AF37;
}

.filter-select {
  background: #1a1a1a;
  border: 1px solid rgba(255,255,255,0.1);
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

/* Capacity Bar */
.capacity-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.8rem;
}

.capacity-bar {
  width: 60px;
  height: 4px;
  background: rgba(255,255,255,0.1);
  border-radius: 2px;
  overflow: hidden;
}

.capacity-fill {
  height: 100%;
  background: #10b981;
  border-radius: 2px;
  transition: width 0.3s;
}

.capacity-fill.warning {
  background: #fbbf24;
}

/* Rating */
.rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.rating-value {
  font-weight: 600;
}

.rating-star {
  color: #D4AF37;
}

/* Activity List */
.activity-list {
  padding: 0.5rem 0;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  background: rgba(107, 114, 128, 0.15);
  color: #9ca3af;
  flex-shrink: 0;
}

.activity-icon.login { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.activity-icon.create { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.activity-icon.update { background: rgba(251, 191, 36, 0.15); color: #fbbf24; }

.activity-content {
  flex: 1;
}

.activity-text {
  color: #d1d5db;
  font-size: 0.875rem;
}

.activity-time {
  color: #6b7280;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

/* Performers Grid */
.performers-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  padding: 1rem;
}

.performer-card {
  background: rgba(0,0,0,0.2);
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
}

.performer-rank {
  color: #D4AF37;
  font-size: 0.875rem;
  font-weight: 700;
}

.performer-name {
  color: #fff;
  font-weight: 600;
  margin: 0.5rem 0;
}

.performer-stats {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: #6b7280;
}

/* Interactions */
.interactions-list {
  padding: 0.5rem 0;
}

.interaction-item {
  display: flex;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}

.interaction-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.interaction-content {
  flex: 1;
}

.interaction-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.interaction-type {
  color: #D4AF37;
  font-size: 0.8rem;
  font-weight: 600;
}

.interaction-time {
  color: #6b7280;
  font-size: 0.75rem;
}

.interaction-customer {
  color: #fff;
  font-weight: 500;
}

.interaction-desc {
  color: #9ca3af;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Pipeline */
.pipeline-view {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.75rem;
  padding: 1.25rem;
}

.pipeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.pipeline-header h2 {
  color: #fff;
  font-size: 1rem;
  margin: 0;
}

.pipeline-stats-inline {
  display: flex;
  gap: 1.5rem;
  font-size: 0.8rem;
  color: #6b7280;
}

.pipeline-board {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 1rem;
}

.pipeline-column {
  min-width: 220px;
  background: rgba(0,0,0,0.2);
  border-radius: 0.5rem;
  padding: 0.75rem;
}

.pipeline-column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  margin-bottom: 0.75rem;
}

.stage-name {
  color: #fff;
  font-size: 0.8rem;
  font-weight: 600;
}

.stage-count {
  background: rgba(255,255,255,0.1);
  color: #9ca3af;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.7rem;
}

.pipeline-cards {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.pipeline-card {
  background: #1a1a1a;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.5rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.pipeline-card:hover {
  border-color: #D4AF37;
}

.lead-name {
  color: #fff;
  font-weight: 500;
  font-size: 0.875rem;
}

.lead-email {
  color: #6b7280;
  font-size: 0.75rem;
}

.lead-value {
  color: #D4AF37;
  font-weight: 600;
  margin-top: 0.5rem;
}

.lead-agent {
  color: #9ca3af;
  font-size: 0.7rem;
  margin-top: 0.25rem;
}

/* Features */
.features-list {
  padding: 0.5rem 0;
}

.feature-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-name {
  color: #fff;
  font-weight: 500;
}

.feature-desc {
  color: #6b7280;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.feature-key {
  color: #4b5563;
  font-size: 0.7rem;
  font-family: monospace;
  margin-top: 0.25rem;
}

.feature-toggle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.toggle-label {
  color: #6b7280;
  font-size: 0.8rem;
  min-width: 60px;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #374151;
  border-radius: 24px;
  transition: 0.3s;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: #fff;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle-switch input:checked + .toggle-slider {
  background-color: #D4AF37;
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background: #1a1a1a;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 0.75rem;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal.modal-lg {
  max-width: 700px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.modal-header h3 {
  color: #fff;
  font-size: 1.1rem;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  color: #6b7280;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}

.modal-close:hover {
  color: #fff;
}

.modal-body {
  padding: 1.25rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(255,255,255,0.06);
}

/* Form */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  color: #9ca3af;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  background: #111;
  border: 1px solid rgba(255,255,255,0.1);
  color: #fff;
  padding: 0.6rem 0.875rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #D4AF37;
}

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

/* Customer Detail */
.customer-detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.detail-section h4 {
  color: #D4AF37;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  font-size: 0.875rem;
}

.detail-label {
  color: #6b7280;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

/* Loading */
.loading-overlay {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255,255,255,0.1);
  border-top-color: #D4AF37;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Utilities */
.text-muted { color: #6b7280; }
.text-danger { color: #ef4444; }
.text-success { color: #10b981; }

/* Responsive */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .performers-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    width: 60px;
  }
  .sidebar-logo span,
  .nav-btn span,
  .admin-info,
  .back-link {
    display: none;
  }
  .admin-main {
    margin-left: 60px;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
  .customer-detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
