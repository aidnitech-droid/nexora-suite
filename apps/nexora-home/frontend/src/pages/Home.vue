<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>Nexora Suite</h1>
        <p>The Complete Business Management Platform for SMEs</p>
        <p class="subtext">All-in-one solution for accounting, CRM, inventory, HR, and more. 100% FREE until March 31, 2026.</p>
        <div class="cta-buttons">
          <router-link to="/modules" class="btn btn-primary">Explore Modules</router-link>
          <router-link to="/login" class="btn btn-secondary">Get Started</router-link>
        </div>
      </div>
    </section>

    <!-- Pricing Banner -->
    <section class="pricing-banner">
      <div class="banner-content">
        <span class="banner-icon">🎉</span>
        <div>
          <h3>Free Until March 31, 2026</h3>
          <p>Access all premium features at no cost during our beta period. Upgrade after March 31, 2026 for continued access.</p>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <h2>Why Choose Nexora Suite?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">⚡</div>
          <h3>All-in-One</h3>
          <p>25+ integrated modules for every business need - no need for multiple tools</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔒</div>
          <h3>Secure</h3>
          <p>Enterprise-grade security with encryption, authentication, and compliance standards</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📱</div>
          <h3>Cloud-Based</h3>
          <p>Access from anywhere, on any device. No installation required</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">👥</div>
          <h3>Team Collaboration</h3>
          <p>Built-in collaboration tools for seamless team communication and workflow</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Advanced Analytics</h3>
          <p>Real-time dashboards and reports to track business performance</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🚀</div>
          <h3>Easy Integration</h3>
          <p>API-first architecture for seamless integration with your existing tools</p>
        </div>
      </div>
    </section>

    <!-- Modules Section -->
    <section class="modules-preview">
      <h2>Featured Modules</h2>
      <p>Explore our comprehensive suite of business management tools</p>
      <div class="modules-grid">
        <div v-for="module in featuredModules" :key="module.id" class="module-card">
          <div class="module-icon">{{ module.icon }}</div>
          <h3>{{ module.name }}</h3>
          <p>{{ module.description }}</p>
        </div>
      </div>
      <router-link to="/modules" class="btn btn-outline">View All 25 Modules →</router-link>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <h2>Ready to Transform Your Business?</h2>
      <p>Join thousands of businesses using Nexora Suite to streamline operations and boost productivity</p>
      <router-link to="/login" class="btn btn-primary btn-large">Start Free Trial Now</router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      featuredModules: [
        {
          id: 1,
          icon: '📚',
          name: 'Nexora Books',
          description: 'Complete accounting and bookkeeping solution'
        },
        {
          id: 2,
          icon: '🏪',
          name: 'Nexora Inventory',
          description: 'Track stock, manage warehouses, and optimize supply chain'
        },
        {
          id: 3,
          icon: '👥',
          name: 'Nexora CRM',
          description: 'Manage customers, sales pipelines, and relationships'
        },
        {
          id: 4,
          icon: '📅',
          name: 'Nexora Bookings',
          description: 'Appointment scheduling and resource management'
        },
        {
          id: 5,
          icon: '💰',
          name: 'Nexora Payroll',
          description: 'Automate payroll, HR, and employee management'
        },
        {
          id: 6,
          icon: '🛒',
          name: 'Nexora Commerce',
          description: 'Build and manage your online store'
        }
      ]
    };
  }
};
</script>

<style scoped>
.home {
  padding: 0;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  padding: 100px 20px;
  text-align: center;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  max-width: 800px;
}

.hero h1 {
  font-size: 52px;
  margin: 0 0 20px 0;
  font-weight: bold;
}

.hero p {
  font-size: 20px;
  margin: 10px 0;
  line-height: 1.6;
}

.subtext {
  font-size: 16px !important;
  opacity: 0.9;
  margin: 20px 0 40px 0;
}

.cta-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 30px;
}

.btn {
  padding: 12px 30px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  display: inline-block;
  transition: all 0.3s;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background: white;
  color: #007bff;
}

.btn-primary:hover {
  background: #f0f0f0;
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: #007bff;
}

.btn-outline {
  border: 2px solid #007bff;
  color: #007bff;
  background: white;
}

.btn-outline:hover {
  background: #f0f8ff;
}

.btn-large {
  padding: 15px 40px;
  font-size: 18px;
}

/* Pricing Banner */
.pricing-banner {
  background: #fff3cd;
  border-bottom: 2px solid #ffc107;
  padding: 20px;
  text-align: center;
}

.banner-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.banner-icon {
  font-size: 32px;
}

.pricing-banner h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.pricing-banner p {
  margin: 0;
  color: #666;
}

/* Features Section */
.features {
  padding: 80px 20px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.features h2 {
  font-size: 36px;
  margin: 0 0 50px 0;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 50px;
}

.feature-card {
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.feature-card h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 20px;
}

.feature-card p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

/* Modules Section */
.modules-preview {
  padding: 80px 20px;
  background: #f9f9f9;
  text-align: center;
}

.modules-preview h2 {
  font-size: 36px;
  margin: 0 0 10px 0;
  color: #333;
}

.modules-preview > p {
  color: #666;
  margin: 0 0 50px 0;
  font-size: 18px;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto 40px;
}

.module-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.module-card:hover {
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-3px);
}

.module-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.module-card h3 {
  margin: 10px 0;
  color: #333;
  font-size: 16px;
}

.module-card p {
  margin: 0;
  color: #666;
  font-size: 13px;
  line-height: 1.5;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.cta-section h2 {
  font-size: 36px;
  margin: 0 0 20px 0;
}

.cta-section p {
  font-size: 18px;
  margin: 0 0 30px 0;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 36px;
  }

  .hero p {
    font-size: 16px;
  }

  .features h2,
  .modules-preview h2,
  .cta-section h2 {
    font-size: 28px;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .cta-buttons .btn {
    width: 100%;
  }

  .banner-content {
    flex-direction: column;
    text-align: center;
  }
}
</style>
