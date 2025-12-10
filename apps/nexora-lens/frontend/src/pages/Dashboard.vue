<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Nexora Module Dashboard</h1>
      <p>Welcome to your module</p>
    </div>

    <div class="welcome-section">
      <div class="welcome-card">
        <h2>Getting Started</h2>
        <p>This is your module dashboard. Start by exploring the features available.</p>
        <ul>
          <li>📊 View your data and statistics</li>
          <li>➕ Create and manage items</li>
          <li>⚙️ Configure settings</li>
          <li>📈 Track performance</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0 0 5px 0;
}

.dashboard-header p {
  color: #666;
  margin: 0;
}

.welcome-section {
  margin-bottom: 30px;
}

.welcome-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.welcome-card h2 {
  margin: 0 0 15px 0;
  color: #333;
}

.welcome-card p {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.6;
}

.welcome-card ul {
  margin: 0;
  padding-left: 20px;
}

.welcome-card li {
  margin: 8px 0;
  color: #666;
}
</style>
