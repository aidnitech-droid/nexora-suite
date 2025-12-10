<template>
  <div class="modules-page">
    <div class="page-header">
      <h1>Nexora Suite - 25 Modules</h1>
      <p>Complete business management platform with integrated tools for every department</p>
    </div>

    <div class="filter-section">
      <input v-model="searchQuery" type="text" placeholder="Search modules...">
      <select v-model="selectedCategory">
        <option value="">All Categories</option>
        <option value="Finance">Finance & Accounting</option>
        <option value="Operations">Operations</option>
        <option value="HR">HR & Payroll</option>
        <option value="Sales">Sales & CRM</option>
        <option value="Productivity">Productivity</option>
      </select>
    </div>

    <div class="modules-grid">
      <div v-for="module in filteredModules" :key="module.id" class="module-item">
        <div class="module-header">
          <div class="module-icon">{{ module.icon }}</div>
          <h3>{{ module.name }}</h3>
        </div>
        <p class="module-description">{{ module.description }}</p>
        <div class="module-features">
          <span v-for="feature in module.features" :key="feature" class="feature-badge">
            {{ feature }}
          </span>
        </div>
        <div class="module-category">
          <span class="category-badge">{{ module.category }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modules',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      modules: [
        { id: 1, icon: '📚', name: 'Nexora Books', description: 'Complete accounting and bookkeeping', category: 'Finance', features: ['Invoicing', 'Expense Tracking', 'Reports'] },
        { id: 2, icon: '💰', name: 'Nexora Payroll', description: 'Payroll management and HR', category: 'HR', features: ['Salary', 'Benefits', 'Attendance'] },
        { id: 3, icon: '📊', name: 'Nexora Expense', description: 'Employee expense tracking', category: 'Finance', features: ['Reports', 'Approvals', 'Reimbursement'] },
        { id: 4, icon: '🧾', name: 'Nexora Invoice', description: 'Free invoicing tool', category: 'Finance', features: ['Invoice', 'Payment', 'Analytics'] },
        { id: 5, icon: '💳', name: 'Nexora Payments', description: 'Unified payments gateway', category: 'Finance', features: ['Multiple', 'Gateways', 'Security'] },
        { id: 6, icon: '🏪', name: 'Nexora Inventory', description: 'Stock and warehouse management', category: 'Operations', features: ['Tracking', 'Orders', 'Analytics'] },
        { id: 7, icon: '🛒', name: 'Nexora Commerce', description: 'Online store builder', category: 'Operations', features: ['Store', 'Products', 'Analytics'] },
        { id: 8, icon: '💵', name: 'Nexora Billing', description: 'Billing and cash register', category: 'Operations', features: ['POS', 'Billing', 'Reports'] },
        { id: 9, icon: '🎯', name: 'Nexora POS', description: 'Retail POS system', category: 'Operations', features: ['Transactions', 'Inventory', 'Reporting'] },
        { id: 10, icon: '👥', name: 'Nexora CRM', description: 'Customer relationship management', category: 'Sales', features: ['Contacts', 'Deals', 'Pipeline'] },
        { id: 11, icon: '📈', name: 'Nexora Bigin', description: 'Pipeline CRM system', category: 'Sales', features: ['Pipeline', 'Forecasting', 'Analytics'] },
        { id: 12, icon: '🗺️', name: 'Nexora RouteIQ', description: 'Route planning for sales teams', category: 'Sales', features: ['Planning', 'Optimization', 'Tracking'] },
        { id: 13, icon: '💬', name: 'Nexora SalesIQ', description: 'Chat and engagement platform', category: 'Sales', features: ['Messaging', 'Automation', 'Analytics'] },
        { id: 14, icon: '📅', name: 'Nexora Bookings', description: 'Appointment scheduling', category: 'Productivity', features: ['Scheduling', 'Reminders', 'Analytics'] },
        { id: 15, icon: '✍️', name: 'Nexora Sign', description: 'Digital signature tool', category: 'Productivity', features: ['Signatures', 'Documents', 'Compliance'] },
        { id: 16, icon: '📱', name: 'Nexora Checkout', description: 'Payment pages', category: 'Operations', features: ['Pages', 'Analytics', 'Security'] },
        { id: 17, icon: '🔧', name: 'Nexora Service', description: 'Field service management', category: 'Operations', features: ['Dispatch', 'Tracking', 'Billing'] },
        { id: 18, icon: '💼', name: 'Nexora Practice', description: 'Firm management', category: 'HR', features: ['Projects', 'Billing', 'Teams'] },
        { id: 19, icon: '🎓', name: 'Nexora Assist', description: 'Remote support', category: 'Productivity', features: ['Support', 'Ticketing', 'Chat'] },
        { id: 20, icon: '🎫', name: 'Nexora Desk', description: 'Customer support', category: 'Productivity', features: ['Ticketing', 'Routing', 'Analytics'] },
        { id: 21, icon: '📝', name: 'Nexora Forms', description: 'Form builder and surveys', category: 'Productivity', features: ['Forms', 'Surveys', 'Analytics'] },
        { id: 22, icon: '⚙️', name: 'Nexora FSM', description: 'Field service management', category: 'Operations', features: ['Dispatch', 'Tracking', 'Optimization'] },
        { id: 23, icon: '🔍', name: 'Nexora Lens', description: 'Analytics and insights', category: 'Analytics', features: ['Dashboards', 'Reports', 'Insights'] },
        { id: 24, icon: '🛣️', name: 'Nexora Route', description: 'Route optimization', category: 'Operations', features: ['Planning', 'Optimization', 'Analytics'] },
        { id: 25, icon: '🏠', name: 'Nexora Home', description: 'Dashboard and portal', category: 'Productivity', features: ['Dashboard', 'Hub', 'Analytics'] }
      ]
    };
  },
  computed: {
    filteredModules() {
      return this.modules.filter(module => {
        const matchesSearch = module.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                            module.description.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesCategory = !this.selectedCategory || module.category === this.selectedCategory;
        return matchesSearch && matchesCategory;
      });
    }
  }
};
</script>

<style scoped>
.modules-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 50px;
}

.page-header h1 {
  font-size: 36px;
  color: #333;
  margin: 0 0 10px 0;
}

.page-header p {
  font-size: 18px;
  color: #666;
  margin: 0;
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.filter-section input,
.filter-section select {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  flex: 1;
  min-width: 200px;
}

.filter-section input:focus,
.filter-section select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

.module-item {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.module-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.module-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.module-icon {
  font-size: 40px;
  line-height: 1;
}

.module-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.module-description {
  color: #666;
  margin: 0 0 15px 0;
  line-height: 1.5;
  flex-grow: 1;
}

.module-features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.feature-badge {
  background: #f0f0f0;
  color: #666;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.module-category {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.category-badge {
  background: #007bff;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .modules-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }

  .filter-section {
    flex-direction: column;
  }

  .filter-section input,
  .filter-section select {
    width: 100%;
  }
}
</style>
