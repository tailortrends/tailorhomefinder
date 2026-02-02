<template>
  <div class="admin-page">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-logo">
        <span>Tailor</span> Admin
      </div>
      <nav class="sidebar-nav">
        <button 
          @click="currentTab = 'overview'"
          :class="{ active: currentTab === 'overview' }"
          class="nav-btn"
        >
          Overview
        </button>
        <button 
          @click="currentTab = 'users'"
          :class="{ active: currentTab === 'users' }"
          class="nav-btn"
        >
          Users
        </button>
        <button 
          @click="currentTab = 'analytics'"
          :class="{ active: currentTab === 'analytics' }"
          class="nav-btn"
        >
          Analytics
        </button>
        <button 
          @click="currentTab = 'properties'"
          :class="{ active: currentTab === 'properties' }"
          class="nav-btn"
        >
          Properties
        </button>
      </nav>
      <router-link :to="{ name: 'dashboard' }" class="back-link">← Back to App</router-link>
    </aside>

    <!-- Main Content -->
    <main class="admin-main">
      <div class="content-wrapper">
        
        <!-- OVERVIEW -->
        <div v-show="currentTab === 'overview'">
          <h1 class="page-title">Overview</h1>
          
          <div class="stats-grid">
            <div class="stat-box">
              <div class="stat-label">Total Users</div>
              <div class="stat-value">248</div>
              <div class="stat-change">+12 this week</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Total Searches</div>
              <div class="stat-value">1,842</div>
              <div class="stat-change">+86 today</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Properties</div>
              <div class="stat-value">52</div>
              <div class="stat-change">from 5 zip codes</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Saved</div>
              <div class="stat-value">94</div>
              <div class="stat-change">+5 today</div>
            </div>
          </div>

          <div class="panel">
            <h2>Recent Activity</h2>
            <table class="data-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Action</th>
                  <th>Details</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>stailor45@gmail.com</td>
                  <td><span class="badge badge-blue">Login</span></td>
                  <td>Web login</td>
                  <td>2 min ago</td>
                </tr>
                <tr>
                  <td>john.doe@email.com</td>
                  <td><span class="badge badge-green">Search</span></td>
                  <td>Phoenix, 3 bed, &lt; $600K</td>
                  <td>5 min ago</td>
                </tr>
                <tr>
                  <td>jane.smith@email.com</td>
                  <td><span class="badge badge-gold">Saved</span></td>
                  <td>9219 S 30th Ave</td>
                  <td>12 min ago</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- USERS -->
        <div v-show="currentTab === 'users'">
          <h1 class="page-title">User Management</h1>
          <div class="panel">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Joined</th>
                  <th>Searches</th>
                  <th>Saved</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Shyam W</td>
                  <td>stailor45@gmail.com</td>
                  <td>Jan 28, 2026</td>
                  <td>42</td>
                  <td>8</td>
                </tr>
                <tr>
                  <td>John Doe</td>
                  <td>john.doe@email.com</td>
                  <td>Jan 29, 2026</td>
                  <td>15</td>
                  <td>3</td>
                </tr>
                <tr>
                  <td>Jane Smith</td>
                  <td>jane.smith@email.com</td>
                  <td>Jan 30, 2026</td>
                  <td>7</td>
                  <td>2</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ANALYTICS -->
        <div v-show="currentTab === 'analytics'">
          <h1 class="page-title">Analytics</h1>
          <div class="analytics-grid">
            <div class="panel">
              <h2>Popular Searches</h2>
              <div class="list-item">
                <span class="rank">1</span>
                <span>Phoenix, AZ</span>
                <span class="count">342</span>
              </div>
              <div class="list-item">
                <span class="rank">2</span>
                <span>Scottsdale, AZ</span>
                <span class="count">218</span>
              </div>
              <div class="list-item">
                <span class="rank">3</span>
                <span>3 Bed Under $600K</span>
                <span class="count">195</span>
              </div>
            </div>
            <div class="panel">
              <h2>Property Types</h2>
              <div class="list-item">
                <span class="dot" style="background: #D4AF37;"></span>
                <span>Single Family</span>
                <span class="count">62%</span>
              </div>
              <div class="list-item">
                <span class="dot" style="background: #10b981;"></span>
                <span>Condo</span>
                <span class="count">24%</span>
              </div>
              <div class="list-item">
                <span class="dot" style="background: #3b82f6;"></span>
                <span>Townhouse</span>
                <span class="count">9%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- PROPERTIES -->
        <div v-show="currentTab === 'properties'">
          <h1 class="page-title">Property Management</h1>
          <div class="panel">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Property</th>
                  <th>Location</th>
                  <th>Price</th>
                  <th>Type</th>
                  <th>Views</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>9219 S 30th Ave</td>
                  <td>Phoenix, AZ</td>
                  <td class="price">$420K</td>
                  <td>House</td>
                  <td>142</td>
                </tr>
                <tr>
                  <td>6587 N Palmeraie Blvd</td>
                  <td>Phoenix, AZ</td>
                  <td class="price">$2.8M</td>
                  <td>Condo</td>
                  <td>89</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentTab = ref('overview')
</script>

<style scoped>
.admin-page {
  display: flex;
  min-height: 100vh;
  background: #0c0c0c;
}

.admin-sidebar {
  width: 200px;
  background: #111;
  border-right: 1px solid rgba(255,255,255,0.06);
  display: flex;
  flex-direction: column;
}

.sidebar-logo {
  padding: 1.5rem;
  font-size: 1.1rem;
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
}

.nav-btn {
  width: 100%;
  padding: 0.75rem 1rem;
  margin-bottom: 0.25rem;
  background: transparent;
  border: none;
  color: #9ca3af;
  text-align: left;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.nav-btn:hover {
  background: rgba(255,255,255,0.05);
  color: #fff;
}

.nav-btn.active {
  background: rgba(212, 175, 55, 0.15);
  color: #D4AF37;
}

.back-link {
  padding: 1rem;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.85rem;
}

.back-link:hover {
  color: #D4AF37;
}

.admin-main {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.content-wrapper {
  max-width: 1400px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 2rem;
  font-family: Georgia, serif;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.stat-label {
  color: #9ca3af;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  font-family: Georgia, serif;
  margin-bottom: 0.25rem;
}

.stat-change {
  color: #10b981;
  font-size: 0.75rem;
}

.panel {
  background: #141414;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.panel h2 {
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 0.75rem;
  color: #6b7280;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.data-table td {
  padding: 0.75rem;
  color: #d1d5db;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}

.data-table tr:hover td {
  background: rgba(255,255,255,0.02);
}

.price {
  color: #D4AF37;
  font-weight: 700;
  font-family: Georgia, serif;
}

.badge {
  padding: 0.25rem 0.6rem;
  border-radius: 0.25rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
}

.badge-blue { background: rgba(59,130,246,0.15); color: #60a5fa; }
.badge-green { background: rgba(16,185,129,0.15); color: #34d399; }
.badge-gold { background: rgba(212,175,55,0.15); color: #D4AF37; }

.analytics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  color: #d1d5db;
}

.rank {
  color: #D4AF37;
  font-weight: 700;
  width: 24px;
}

.count {
  margin-left: auto;
  color: #6b7280;
  font-size: 0.85rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
</style>