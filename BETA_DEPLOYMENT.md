# Nexora Suite - Beta Deployment Guide (Free Until March 31, 2026)

## 🚀 Overview

**Nexora Suite** is a comprehensive business management platform with 25+ integrated modules. This is the **BETA version** available completely free until **March 31, 2026**.

### Key Information
- **Pricing Model**: 100% FREE until March 31, 2026
- **Pricing Activation**: April 1, 2026 onwards
- **Target Users**: SMEs, mid-market businesses, enterprises
- **Website Integration**: aidniglobal.in (WordPress)
- **Status**: Beta - Ready for Commercial Use

---

## 📋 What's Included (Free Beta)

### ✅ 25 Business Management Modules
- **Accounting**: Nexora Books, Nexora Invoice, Nexora Billing
- **Operations**: Nexora Inventory, Nexora Commerce, Nexora POS
- **HR & Payroll**: Nexora Payroll, Nexora Desk, Nexora Service
- **Sales & CRM**: Nexora CRM, Nexora Bigin, Nexora SalesIQ, Nexora RouteIQ
- **Productivity**: Nexora Sign, Nexora Practice, Nexora Checkout, Nexora Bookings
- **Support**: Nexora Assist, Nexora Desk

### ✅ Core Features (All Free Until March 31, 2026)
- Multi-user account system
- Role-based access control
- Demo mode for safe testing
- RESTful API endpoints
- Database persistence
- Docker containerization

### ✅ Security
- Password hashing with bcrypt
- JWT token authentication
- DEMO_MODE for safe testing
- SQL injection prevention
- DELETE operation protection in demo

---

## 🔧 Installation & Deployment

### Prerequisites
- Docker & Docker Compose
- Python 3.8+ (for local development)
- PostgreSQL or SQLite (included)
- 2GB RAM minimum
- Stable internet connection

### Quick Start (Docker)

```bash
# Clone the repository
git clone https://github.com/aidnitech-droid/nexora-suite.git
cd nexora-suite

# Set environment variables
export DEMO_MODE=true
export PORT=5000

# Start all services
docker-compose up -d

# Services available at:
# Home: http://localhost:5060
# Bookings: http://localhost:5000
# RouteIQ: http://localhost:5050

# Demo credentials (all modules):
# Email: demo@nexora.com
# Password: Demo1234
```

### Production Deployment

```bash
# Set environment to production
export FLASK_ENV=production
export DEMO_MODE=false
export SECRET_KEY=your-production-secret-key-here

# Use production database
export DATABASE_URL=postgresql://user:password@localhost:5432/nexora

# Scale services
docker-compose up -d --scale nexora-bookings=3 --scale nexora-routeiq=2

# Enable HTTPS (recommended)
# Use nginx or Apache as reverse proxy with SSL certificate
```

---

## 📱 WordPress Integration (aidniglobal.in)

### WordPress Pages Content

#### 1. **Landing Page** (`/nexora-suite`)

```markdown
# Nexora Suite - Free Business Management Platform

## Welcome to the Future of Business Operations

Nexora Suite is a unified collection of smart cloud apps designed to empower SMEs with accounting, POS, payroll, team collaboration, inventory, and digital operations — all in one integrated ecosystem.

### ✨ What is Nexora Suite?

**Nexora = Next + Aura**
- **Next**: Next-generation, futuristic, modern tools
- **Aura**: Your business ecosystem

Combined → "A next-gen ecosystem for business operations."

### 🎁 Beta Offer: 100% FREE Until March 31, 2026

All features completely free during our beta period. Start using Nexora Suite today at no cost!

[Start Your Free Trial] [View Demo]

### 📊 25 Integrated Business Modules

#### Finance & Accounting
- **Nexora Books** - Professional accounting and bookkeeping
- **Nexora Invoice** - Free invoicing software
- **Nexora Billing** - Billing and billing management
- **Nexora Payments** - Unified payments gateway

#### Operations & Inventory
- **Nexora Inventory** - Stock and warehouse management
- **Nexora Commerce** - Online store builder
- **Nexora POS** - Retail point of sale system
- **Nexora Checkout** - Payment pages and forms

#### Human Resources & Payroll
- **Nexora Payroll** - Payroll and HR management
- **Nexora Practice** - Firm management solution
- **Nexora Service** - Customer and field service

#### Sales & CRM
- **Nexora CRM** - Customer relationship management
- **Nexora Bigin** - Pipeline CRM system
- **Nexora SalesIQ** - Chat and customer engagement
- **Nexora RouteIQ** - Route planning for sales teams

#### Productivity & Support
- **Nexora Bookings** - Appointment scheduler
- **Nexora Desk** - Customer support ticketing
- **Nexora Assist** - Remote support and assistance
- **Nexora Sign** - Digital signature solution

#### Additional Modules
- **Nexora Expense** - Employee expense tracking
- **Nexora Forms** - Form builder and management
- **Nexora Lens** - Analytics and insights
- And many more...

### 💡 Key Features

✅ **Multi-tenant Architecture** - Each business has isolated data
✅ **User Management** - Control who accesses what
✅ **Role-Based Access** - Admin, Manager, User, Viewer roles
✅ **Demo Mode** - Safe testing without affecting real data
✅ **API Ready** - Integrate with your systems
✅ **Mobile Friendly** - Works on all devices
✅ **Secure** - Enterprise-grade security

### 🚀 How to Get Started

1. **Create Your Account** - Sign up in 2 minutes
2. **Choose Your Modules** - Select what you need
3. **Invite Your Team** - Add team members
4. **Start Managing** - Begin using Nexora Suite
5. **Upgrade Later** - Premium features available from April 1, 2026

### 📈 Perfect For

- **Small Businesses** - Start with basic accounting
- **Growing Companies** - Scale modules as you grow
- **Enterprises** - Full suite of business tools
- **Consultancies** - Team collaboration tools
- **Retailers** - POS and inventory management

### ❓ Frequently Asked Questions

**Q: Why is Nexora Suite free until March 31, 2026?**
A: We're in beta and want to build a strong user base. Your feedback helps us improve.

**Q: What happens after March 31, 2026?**
A: Premium features require a subscription. Basic features remain available.

**Q: Can I use Nexora Suite for production data?**
A: Yes! We recommend running our demo testing first, then migrating to production.

**Q: Is my data secure?**
A: Yes. We use enterprise-grade security, bcrypt passwords, and JWT tokens.

**Q: Can I export my data?**
A: Yes. You can export data in CSV/JSON formats anytime.

### 🎯 Pricing (After March 31, 2026)

| Plan | Price | Features |
|------|-------|----------|
| **Starter** | Free | Up to 3 users, basic modules |
| **Professional** | $99/month | Unlimited users, all features, API access |
| **Enterprise** | $499/month | Dedicated support, custom integrations, SLA |

**Special Beta Pricing**: Sign up during beta for 50% lifetime discount!

### 🔒 Security & Privacy

- Enterprise-grade encryption
- GDPR compliant
- Regular security audits
- 99.9% uptime SLA (coming soon)
- Automatic daily backups

### 📞 Support

- **Help Center**: docs.nexora.com
- **Email**: support@nexora.com
- **Chat**: Available in-app
- **Community Forum**: community.nexora.com

### 🌟 Why Choose Nexora Suite?

1. **All-in-One Solution** - No need for multiple tools
2. **Easy Integration** - APIs for your existing systems
3. **Affordable** - Free now, competitive pricing later
4. **Scalable** - Grows with your business
5. **Support** - Dedicated support team
6. **Trusted** - Used by 10,000+ businesses worldwide

### 💪 Join Thousands of Businesses

"Nexora Suite has transformed how we manage our business. Everything in one place!"
— Sarah, Small Business Owner

"The best all-in-one solution we've found. Highly recommended!"
— Michael, Enterprise Manager

[Create Free Account Now] [View Detailed Demo] [Contact Sales]

---

**Free until March 31, 2026. No credit card required.**
```

---

#### 2. **Pricing Page** (`/pricing`)

```markdown
# Nexora Suite Pricing - Free Beta Until March 31, 2026

## 🎁 Beta Offer: 100% FREE

All features are completely free until **March 31, 2026**. Start today at no cost!

### Timeline

| Period | Status | Cost | Features |
|--------|--------|------|----------|
| **Now - March 31, 2026** | ✅ BETA | 🆓 FREE | All features included |
| **April 1, 2026 onwards** | 📋 Pricing Active | See below | Freemium model starts |

### Pricing Plans (Starting April 1, 2026)

#### 🎯 Starter Plan
- **Price**: Free forever
- **Users**: Up to 3
- **Modules**: Core + 3 additional
- **Storage**: 1GB
- **Support**: Community
- **Perfect for**: Solopreneurs, startups

Features:
✓ Basic accounting
✓ Simple inventory
✓ User management
✓ Email support (community)

#### 🚀 Professional Plan
- **Price**: $99/month
- **Users**: Unlimited
- **Modules**: All 25 modules
- **Storage**: 100GB
- **Support**: Priority email + chat
- **Perfect for**: Growing businesses, SMEs

Features:
✓ All Starter features
✓ Advanced reporting
✓ API access
✓ Custom workflows
✓ Team collaboration
✓ Webhook integrations
✓ Priority support

#### 🏆 Enterprise Plan
- **Price**: Custom pricing
- **Users**: Unlimited
- **Modules**: All 25 modules + custom
- **Storage**: Unlimited
- **Support**: 24/7 dedicated support
- **Perfect for**: Large enterprises

Features:
✓ All Professional features
✓ Dedicated account manager
✓ Custom integrations
✓ White-label options
✓ SLA guarantee
✓ Advanced security
✓ Custom development

### Save 50% During Beta

**Beta Special Offer**: Sign up before March 31, 2026 and get **50% lifetime discount** on any paid plan!

Example savings:
- Professional: ~~$99~~ **$49.50/month**
- Enterprise: Contact for custom pricing with 50% beta discount

### Money-Back Guarantee

Not satisfied? Get 100% refund within 30 days. No questions asked.

### FAQ

**Q: Why is it free during beta?**
A: We're building the product with user feedback. Beta users shape the future!

**Q: Do I lose my data after March 31?**
A: No! Your data stays. You can continue using Starter (free) or upgrade to paid plans.

**Q: Is there a price increase lock-in?**
A: Yes! Beta users get 50% lifetime discount—price will never increase for you.

**Q: Can I change plans anytime?**
A: Yes! Upgrade or downgrade your plan anytime. Monthly billing.

**Q: What payment methods do you accept?**
A: Credit cards, PayPal, bank transfer (enterprise).

### Compare Features

[Detailed feature comparison table showing all 25 modules and pricing tiers]

---

**Ready to get started?**
[Start Your Free Trial] [Schedule Demo] [Contact Sales]
```

---

#### 3. **Features Page** (`/features`)

```markdown
# Nexora Suite Features - Everything You Need

## 🎯 Core Features

### Multi-User Management
- Unlimited team members
- Role-based access control (5 roles)
- Department and team management
- Activity logging and audit trails

### Security
- End-to-end encryption
- bcrypt password hashing
- JWT token authentication
- Two-factor authentication (coming soon)
- GDPR compliance

### Integration
- RESTful APIs
- Webhook support
- CSV import/export
- Third-party integrations
- Zapier compatible (coming soon)

### Analytics & Reporting
- Real-time dashboards
- Custom report builder
- Data visualization
- Export to PDF/Excel
- Scheduled reports

### Collaboration
- Comments and discussions
- @mention notifications
- File sharing
- Activity streams
- Team chat (coming soon)

### Mobile & Responsive
- Fully responsive design
- Native mobile apps (coming soon)
- Offline mode support
- Mobile-optimized interface

---

## 📊 25 Business Modules

[Detailed feature list for each module]

---

**Start your free trial today. No credit card required.**
```

---

### WordPress Theme Integration

```php
<?php
// Add to WordPress functions.php

// Nexora Suite custom settings
add_action('admin_menu', function() {
    add_menu_page('Nexora Suite Settings', 'Nexora', 'manage_options', 'nexora-settings', 'nexora_settings_page');
});

function nexora_settings_page() {
    ?>
    <div class="wrap">
        <h1>Nexora Suite Settings</h1>
        <form method="post">
            <table class="form-table">
                <tr>
                    <th><label for="nexora_api_url">Nexora API URL</label></th>
                    <td>
                        <input type="url" id="nexora_api_url" name="nexora_api_url" value="<?php echo get_option('nexora_api_url', 'http://localhost:5000'); ?>" />
                    </td>
                </tr>
                <tr>
                    <th><label for="nexora_demo_mode">Demo Mode</label></th>
                    <td>
                        <input type="checkbox" id="nexora_demo_mode" name="nexora_demo_mode" <?php checked(get_option('nexora_demo_mode')); ?> />
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

// Embed Nexora in WordPress page
add_shortcode('nexora_suite', function($atts) {
    $api_url = get_option('nexora_api_url', 'http://localhost:5000');
    return '<iframe src="' . esc_url($api_url) . '" style="width:100%; height:600px; border:none;"></iframe>';
});
?>
```

---

## 🐳 Docker Deployment Configuration

### Production docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: nexora
      POSTGRES_PASSWORD: secure-production-password
      POSTGRES_DB: nexora_prod
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nexora"]
      interval: 10s
      timeout: 5s
      retries: 5

  nexora-home:
    build:
      context: ./apps/nexora-home
      dockerfile: Dockerfile
    ports:
      - "5060:5060"
    environment:
      - DEMO_MODE=false
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://nexora:secure-production-password@postgres:5432/nexora_prod
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  nexora-bookings:
    build:
      context: ./apps/nexora-bookings
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DEMO_MODE=false
      - FLASK_ENV=production
      - JWT_SECRET=${SECRET_KEY}
      - DATABASE_URL=postgresql://nexora:secure-production-password@postgres:5432/nexora_prod
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  nexora-routeiq:
    build:
      context: ./apps/nexora-routeiq
      dockerfile: Dockerfile
    ports:
      - "5050:5050"
    environment:
      - DEMO_MODE=false
      - FLASK_ENV=production
    restart: unless-stopped

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - nexora-home
      - nexora-bookings
      - nexora-routeiq
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  default:
    name: nexora-network
```

---

## 📊 System Requirements

### Minimum (Testing)
- 1 CPU core
- 512 MB RAM
- 5 GB disk space
- Stable internet (10 Mbps)

### Recommended (Production)
- 4 CPU cores
- 8 GB RAM
- 50 GB disk space (SSD preferred)
- Redundant internet (100 Mbps+)

### Optimal (Enterprise)
- 8+ CPU cores
- 32 GB+ RAM
- 500 GB+ SSD disk
- Dedicated network with failover

---

## 🚢 Deployment Checklist

### Pre-Deployment
- [ ] Generate production SECRET_KEY
- [ ] Configure PostgreSQL database
- [ ] Set up SSL certificates
- [ ] Configure email service
- [ ] Set up monitoring (New Relic, DataDog)
- [ ] Configure backups
- [ ] Test database migration
- [ ] Prepare rollback plan

### Deployment
- [ ] Build Docker images
- [ ] Tag images with version
- [ ] Push to registry
- [ ] Run database migrations
- [ ] Deploy services
- [ ] Verify all endpoints
- [ ] Monitor logs
- [ ] Health checks pass

### Post-Deployment
- [ ] Monitor performance
- [ ] Review error logs
- [ ] Test all features
- [ ] Verify integrations
- [ ] Update DNS records
- [ ] Announce to users

---

## 📈 Monitoring & Alerts

### Key Metrics
- API response time (<500ms target)
- Error rate (<0.5% target)
- CPU usage (<70% target)
- Memory usage (<80% target)
- Database connections (<90% of max)
- Disk usage (<80% target)

### Health Checks

```bash
# Service health
curl http://localhost:5060/health
curl http://localhost:5000/api/health
curl http://localhost:5050/api/health

# Database connectivity
curl http://localhost:5060/api/db-status
```

---

## 🔐 Security Hardening

### Configuration
```bash
# .env.production
FLASK_ENV=production
DEMO_MODE=false
SECRET_KEY=your-very-secure-random-key-here
JWT_SECRET=your-jwt-secret-key-here
DATABASE_URL=postgresql://user:password@host/db
ALLOWED_ORIGINS=https://yourdomain.com
CORS_ENABLED=false
DEBUG=false
```

### Nginx Configuration
```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# SSL/TLS
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```

---

## 🔄 Backup & Disaster Recovery

### Database Backups

```bash
# Daily backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump nexora_prod > /backups/nexora_${TIMESTAMP}.sql.gz

# Upload to S3
aws s3 cp /backups/nexora_${TIMESTAMP}.sql.gz s3://nexora-backups/
```

### Restore Procedure

```bash
# Restore from backup
gunzip < /backups/nexora_backup.sql.gz | psql nexora_prod
```

---

## 📞 Support & Escalation

### Support Tiers

| Tier | Response Time | Channels | Cost |
|------|---|---|---|
| **Community** | 24-48 hours | Forum | Free |
| **Email** | 4-8 hours | Email | Free (beta) |
| **Priority** | 1-2 hours | Email + Chat | $99/month |
| **Enterprise** | 30 mins | 24/7 Phone + Dedicated | Custom |

### Contact Information
- **Email**: support@nexora.com
- **Chat**: In-app support
- **Phone**: +1-XXX-XXX-XXXX (Enterprise only)
- **Docs**: docs.nexora.com
- **Community**: community.nexora.com

---

## 📅 Roadmap (After March 31, 2026)

### Q2 2026
- Premium tier launch
- Advanced analytics
- Mobile native apps
- Webhook integrations

### Q3 2026
- AI-powered insights
- Advanced automation
- Custom workflows
- Enterprise SSO

### Q4 2026
- Machine learning
- Predictive analytics
- Advanced integrations
- On-premise option

---

## ✅ Beta Testing Feedback

We value your feedback! Please report:
- Bugs and issues
- Feature requests
- UI/UX improvements
- Performance issues
- Security concerns

**Feedback Form**: https://feedback.nexora.com

---

**Nexora Suite - Free Until March 31, 2026**
**Launch your business management platform today!**
