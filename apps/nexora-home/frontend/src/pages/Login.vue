<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>Welcome Back</h1>
          <p>Sign in to Nexora Suite</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label>Email Address</label>
            <input v-model="formData.email" type="email" placeholder="your@email.com" required>
          </div>

          <div class="form-group">
            <label>Password</label>
            <input v-model="formData.password" type="password" placeholder="••••••••" required>
          </div>

          <div class="remember-forgot">
            <label>
              <input v-model="formData.remember" type="checkbox">
              Remember me
            </label>
            <a href="#forgot">Forgot password?</a>
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            {{ loading ? 'Signing In...' : 'Sign In' }}
          </button>
        </form>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="demo-credentials">
          <h3>Demo Credentials</h3>
          <p><strong>Email:</strong> demo@nexora.com</p>
          <p><strong>Password:</strong> Demo1234</p>
          <button @click="useDemoCredentials" class="btn btn-secondary btn-block">
            Use Demo Account
          </button>
        </div>

        <div class="signup-link">
          <p>Don't have an account? <router-link to="/register">Sign Up</router-link></p>
        </div>
      </div>

      <div class="login-promo">
        <h2>Nexora Suite</h2>
        <p>Your Complete Business Management Platform</p>
        <ul>
          <li>✅ 25+ Integrated Modules</li>
          <li>✅ 100% FREE Until March 31, 2026</li>
          <li>✅ Enterprise-Grade Security</li>
          <li>✅ Cloud-Based & Mobile-Ready</li>
          <li>✅ 24/7 Customer Support</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      formData: {
        email: '',
        password: '',
        remember: false
      },
      loading: false,
      error: null
    };
  },
  methods: {
    handleLogin() {
      this.loading = true;
      this.error = null;

      // Simulate login - in production, would call API
      setTimeout(() => {
        if (this.formData.email && this.formData.password) {
          alert('Login successful!');
          this.$router.push('/dashboard');
        } else {
          this.error = 'Please enter both email and password';
        }
        this.loading = false;
      }, 1000);
    },
    useDemoCredentials() {
      this.formData.email = 'demo@nexora.com';
      this.formData.password = 'Demo1234';
    }
  }
};
</script>

<style scoped>
.login-page {
  padding: 40px 20px;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  max-width: 1000px;
  width: 100%;
  align-items: center;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 28px;
}

.login-header p {
  margin: 0;
  color: #666;
}

.login-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.remember-forgot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 14px;
}

.remember-forgot label {
  margin: 0;
  display: flex;
  align-items: center;
}

.remember-forgot input[type="checkbox"] {
  width: auto;
  margin-right: 6px;
}

.remember-forgot a {
  color: #007bff;
  text-decoration: none;
}

.remember-forgot a:hover {
  text-decoration: underline;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-block {
  width: 100%;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
}

.demo-credentials {
  background: #f0f8ff;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
  border: 1px solid #d1ecf1;
}

.demo-credentials h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 14px;
}

.demo-credentials p {
  margin: 5px 0;
  color: #666;
  font-size: 13px;
}

.signup-link {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.signup-link p {
  margin: 0;
  color: #666;
}

.signup-link a {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
}

.signup-link a:hover {
  text-decoration: underline;
}

.login-promo {
  color: white;
  text-align: center;
}

.login-promo h2 {
  font-size: 36px;
  margin: 0 0 10px 0;
}

.login-promo p {
  font-size: 18px;
  margin: 0 0 30px 0;
  opacity: 0.9;
}

.login-promo ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.login-promo li {
  margin: 15px 0;
  font-size: 16px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .login-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .login-promo {
    display: none;
  }

  .login-card {
    padding: 30px;
  }

  .login-header h1 {
    font-size: 24px;
  }
}
</style>
