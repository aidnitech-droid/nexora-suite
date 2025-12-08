<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>📋 Module</h2>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/dashboard" class="nav-link">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/crm" class="nav-link">
        <span>🤝</span> CRM
      </router-link>
      <router-link to="/crm/leads" class="nav-link">
        <span>📥</span> Leads
      </router-link>
      <router-link to="/crm/contacts" class="nav-link">
        <span>👥</span> Contacts
      </router-link>
      <router-link to="/crm/deals" class="nav-link">
        <span>💼</span> Deals
      </router-link>
      <router-link to="/crm/tasks" class="nav-link">
        <span>✅</span> Tasks
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  height: 100vh;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
}

.sidebar-nav {
  padding: 20px 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: white;
  text-decoration: none;
  transition: background 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: #34495e;
}

.nav-link span {
  margin-right: 10px;
  font-size: 18px;
}
</style>
