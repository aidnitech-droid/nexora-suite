<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/" class="brand">
          <span class="logo">📦</span>
          <span>Nexora</span>
        </router-link>
      </div>
      <ul class="navbar-menu">
        <li><router-link to="/">Dashboard</router-link></li>
      </ul>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <footer class="footer">
      <p>&copy; 2025 Nexora Suite. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
    'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  background: white;
  padding: 15px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand {
  color: #007bff;
  text-decoration: none;
  font-size: 20px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo {
  font-size: 24px;
}

.navbar-menu {
  display: flex;
  list-style: none;
  gap: 30px;
}

.navbar-menu a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.navbar-menu a:hover,
.navbar-menu a.router-link-active {
  color: #007bff;
}

.main-content {
  flex: 1;
  padding: 0;
}

.footer {
  background: white;
  padding: 20px;
  text-align: center;
  color: #999;
  border-top: 1px solid #ddd;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .navbar-menu {
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }
}
</style>
