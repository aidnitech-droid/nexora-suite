# Nexora Suite - WordPress Integration Package

This document provides ready-to-use content for integrating Nexora Suite with your WordPress site at **aidniglobal.in**.

## Quick Setup Instructions

### 1. Create WordPress Pages

In WordPress Admin Dashboard:

1. **Pages → Add New**
2. Create these pages:
   - Page Title: "Nexora Suite"
   - Page Slug: "nexora-suite"
   - Content: [Copy from BETA_DEPLOYMENT.md - Landing Page Section]

3. **Pages → Add New**
   - Page Title: "Pricing"
   - Page Slug: "pricing"
   - Content: [Copy from BETA_DEPLOYMENT.md - Pricing Page Section]

4. **Pages → Add New**
   - Page Title: "Features"
   - Page Slug: "features"
   - Content: [Copy from BETA_DEPLOYMENT.md - Features Page Section]

### 2. Add Navigation Menu

In WordPress Admin:
1. **Appearance → Menus**
2. Create new menu: "Nexora Suite"
3. Add menu items:
   - Home → /
   - Nexora Suite → /nexora-suite
   - Pricing → /pricing
   - Features → /features
   - Docs → https://docs.nexora.com
   - Contact → /contact

### 3. Create Blog Post (Optional)

**Title**: "Announcing Nexora Suite - Free Until March 31, 2026"

```markdown
# Announcing Nexora Suite Beta - Free Business Management Platform

We're thrilled to announce the beta launch of **Nexora Suite** - a comprehensive 
business management platform with 25+ integrated modules, completely free until 
March 31, 2026.

## What is Nexora Suite?

Nexora Suite is a unified collection of smart cloud apps designed to empower SMEs 
with accounting, POS, payroll, team collaboration, inventory, and digital operations 
— all in one integrated ecosystem.

### The 25 Modules Include:

**Finance & Accounting:**
- Nexora Books - Professional accounting
- Nexora Invoice - Free invoicing
- Nexora Billing - Billing management
- Nexora Payments - Payment gateway

**Operations:**
- Nexora Inventory - Stock management
- Nexora Commerce - Online store
- Nexora POS - Retail system
- Nexora Checkout - Payment pages

**HR & Payroll:**
- Nexora Payroll - Payroll management
- Nexora Practice - Firm management
- Nexora Service - Customer service

**Sales & CRM:**
- Nexora CRM - Customer relationships
- Nexora Bigin - Pipeline CRM
- Nexora SalesIQ - Customer engagement
- Nexora RouteIQ - Route planning

**Productivity:**
- Nexora Bookings - Appointment scheduler
- Nexora Desk - Support tickets
- Nexora Assist - Remote support
- Nexora Sign - Digital signatures
- Nexora Forms - Form builder
- Nexora Lens - Analytics
- And more...

## Free Beta Offer

**Everything is 100% FREE until March 31, 2026.**

No credit card required. No hidden fees. No data limits.

## Key Features

✅ Multi-user team accounts
✅ Role-based access control
✅ Enterprise-grade security
✅ API ready
✅ Mobile friendly
✅ Demo mode for safe testing

## Who Should Use Nexora Suite?

- Small businesses getting started
- Growing companies scaling operations
- Enterprises needing unified management
- Consultancies building teams
- Retailers managing POS & inventory

## Getting Started

1. Sign up for free (no credit card)
2. Invite your team
3. Choose your modules
4. Start managing your business

[Get Started Free] [Schedule Demo]

---

**Special Beta Offer**: Sign up before March 31, 2026 and get 50% lifetime discount 
when premium features launch!

[Learn More About Nexora Suite](https://aidniglobal.in/nexora-suite)
```

### 4. Add WordPress Shortcodes

Add to WordPress `functions.php`:

```php
<?php
/**
 * Nexora Suite WordPress Integration
 */

// Register Nexora Suite settings
register_setting('nexora_settings', 'nexora_api_url');
register_setting('nexora_settings', 'nexora_demo_credentials');

// Add admin menu
add_action('admin_menu', function() {
    add_menu_page(
        'Nexora Suite',
        'Nexora Suite',
        'manage_options',
        'nexora-suite-settings',
        'nexora_settings_page',
        'dashicons-admin-generic',
        99
    );
});

// Settings page
function nexora_settings_page() {
    ?>
    <div class="wrap">
        <h1>Nexora Suite Settings</h1>
        <form method="post" action="options.php">
            <?php settings_fields('nexora_settings'); ?>
            <table class="form-table">
                <tr valign="top">
                    <th scope="row"><label for="nexora_api_url">Nexora API URL</label></th>
                    <td>
                        <input type="url" 
                               id="nexora_api_url" 
                               name="nexora_api_url" 
                               value="<?php echo esc_attr(get_option('nexora_api_url', 'http://localhost:5000')); ?>" 
                               class="regular-text" />
                        <p class="description">Base URL of your Nexora Suite deployment</p>
                    </td>
                </tr>
                <tr valign="top">
                    <th scope="row"><label for="nexora_demo_credentials">Demo Credentials</label></th>
                    <td>
                        <code><?php echo 'demo@nexora.com / Demo1234'; ?></code>
                        <p class="description">Use these credentials to test Nexora Suite</p>
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

// Shortcode: [nexora_pricing_table]
add_shortcode('nexora_pricing_table', function() {
    ob_start();
    ?>
    <div class="nexora-pricing-table">
        <style>
            .nexora-pricing-table { margin: 20px 0; }
            .nexora-pricing-tier { 
                border: 1px solid #ddd; 
                padding: 20px; 
                margin: 10px 0; 
                border-radius: 8px;
            }
            .nexora-pricing-tier h3 { margin-top: 0; }
            .nexora-pricing-price { font-size: 28px; font-weight: bold; margin: 10px 0; }
            .nexora-pricing-features { list-style: none; padding: 0; }
            .nexora-pricing-features li:before { content: "✓ "; color: green; font-weight: bold; }
            .nexora-pricing-features li { padding: 5px 0; }
        </style>
        
        <div class="nexora-pricing-tier">
            <h3>Starter - Free</h3>
            <div class="nexora-pricing-price">$0/month</div>
            <p>Perfect for solopreneurs</p>
            <ul class="nexora-pricing-features">
                <li>Up to 3 users</li>
                <li>Core + 3 modules</li>
                <li>1 GB storage</li>
                <li>Community support</li>
            </ul>
            <button class="button button-primary">Get Started</button>
        </div>

        <div class="nexora-pricing-tier" style="border: 2px solid #0073aa;">
            <h3>Professional - $99/month</h3>
            <div class="nexora-pricing-price">$99<span style="font-size:14px;">/month</span></div>
            <p>Recommended for growing businesses</p>
            <ul class="nexora-pricing-features">
                <li>Unlimited users</li>
                <li>All 25 modules</li>
                <li>100 GB storage</li>
                <li>Advanced reporting</li>
                <li>API access</li>
                <li>Priority support</li>
            </ul>
            <button class="button button-primary" style="background-color: #0073aa;">Start Free Trial</button>
        </div>

        <div class="nexora-pricing-tier">
            <h3>Enterprise - Custom</h3>
            <div class="nexora-pricing-price">Custom pricing</div>
            <p>For large organizations</p>
            <ul class="nexora-pricing-features">
                <li>Unlimited users</li>
                <li>All 25 modules + custom</li>
                <li>Unlimited storage</li>
                <li>Dedicated support</li>
                <li>SLA guarantee</li>
                <li>White-label options</li>
            </ul>
            <a href="#contact" class="button button-primary">Contact Sales</a>
        </div>
    </div>
    <?php
    return ob_get_clean();
});

// Shortcode: [nexora_modules]
add_shortcode('nexora_modules', function() {
    ob_start();
    $modules = array(
        array('icon' => '📚', 'name' => 'Books', 'desc' => 'Professional accounting'),
        array('icon' => '🧾', 'name' => 'Invoice', 'desc' => 'Free invoicing'),
        array('icon' => '📊', 'name' => 'Billing', 'desc' => 'Billing management'),
        array('icon' => '💳', 'name' => 'Payments', 'desc' => 'Payment gateway'),
        array('icon' => '📦', 'name' => 'Inventory', 'desc' => 'Stock management'),
        array('icon' => '🛒', 'name' => 'Commerce', 'desc' => 'Online store'),
        array('icon' => '🏪', 'name' => 'POS', 'desc' => 'Retail system'),
        array('icon' => '💰', 'name' => 'Payroll', 'desc' => 'Payroll management'),
        array('icon' => '👥', 'name' => 'CRM', 'desc' => 'Customer relations'),
        array('icon' => '📅', 'name' => 'Bookings', 'desc' => 'Appointment scheduling'),
    );
    ?>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
        <?php foreach($modules as $module): ?>
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center;">
            <div style="font-size: 40px; margin-bottom: 10px;"><?php echo $module['icon']; ?></div>
            <h4 style="margin: 10px 0;">Nexora <?php echo $module['name']; ?></h4>
            <p style="margin: 0; color: #666; font-size: 13px;"><?php echo $module['desc']; ?></p>
        </div>
        <?php endforeach; ?>
    </div>
    <?php
    return ob_get_clean();
});

// Shortcode: [nexora_cta]
add_shortcode('nexora_cta', function() {
    ?>
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; 
                border-radius: 8px; text-align: center; margin: 30px 0;">
        <h2 style="color: white; margin-top: 0;">Ready to Transform Your Business?</h2>
        <p style="font-size: 18px; margin: 20px 0;">
            Join thousands of businesses using Nexora Suite. 
            <strong>100% Free until March 31, 2026.</strong>
        </p>
        <a href="<?php echo esc_url(get_option('nexora_api_url', 'http://localhost:5000') . '/register'); ?>" 
           class="button" 
           style="background-color: white; color: #667eea; padding: 12px 30px; font-size: 16px; font-weight: bold;">
            Start Your Free Account Now
        </a>
        <p style="margin-top: 20px; font-size: 12px; opacity: 0.9;">No credit card required • No data limits • Full access to all features</p>
    </div>
    <?php
});

// Shortcode: [nexora_live]
add_shortcode('nexora_live', function($atts) {
    $atts = shortcode_atts(array(
        'height' => '600px',
        'src' => get_option('nexora_api_url', 'http://localhost:5000'),
    ), $atts, 'nexora_live');
    
    return '<iframe src="' . esc_url($atts['src']) . '" 
                    style="width:100%; height:' . esc_attr($atts['height']) . '; 
                    border:none; border-radius: 8px;" 
                    allow="encrypted-media"></iframe>';
});
?>
```

### 5. Add Custom CSS

Add to WordPress theme's `style.css`:

```css
/* Nexora Suite WordPress Styles */

.nexora-hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 80px 20px;
    text-align: center;
    border-radius: 8px;
    margin: 20px 0;
}

.nexora-hero h1 {
    font-size: 48px;
    margin: 0;
    color: white;
}

.nexora-hero p {
    font-size: 20px;
    margin: 20px 0;
    color: rgba(255,255,255,0.9);
}

.nexora-features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin: 40px 0;
}

.nexora-feature-card {
    border: 1px solid #ddd;
    padding: 30px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.nexora-feature-card:hover {
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transform: translateY(-5px);
}

.nexora-feature-icon {
    font-size: 40px;
    margin-bottom: 15px;
}

.nexora-pricing-badge {
    background-color: #28a745;
    color: white;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
    margin: 10px 0;
}

.nexora-banner {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 20px;
    margin: 20px 0;
    border-radius: 4px;
}

.nexora-banner strong {
    color: #856404;
}
```

### 6. Widget Code

Create a sidebar widget showing status:

```php
<?php
/**
 * Nexora Suite Status Widget
 */

class Nexora_Status_Widget extends WP_Widget {
    public function __construct() {
        parent::__construct(
            'nexora_status_widget',
            'Nexora Suite Status'
        );
    }

    public function widget($args, $instance) {
        echo $args['before_widget'];
        echo $args['before_title'] . 'Nexora Suite' . $args['after_title'];
        
        $api_url = get_option('nexora_api_url', 'http://localhost:5000');
        $free_until = '2026-03-31';
        $days_remaining = ceil((strtotime($free_until) - time()) / 86400);
        
        ?>
        <div style="padding: 15px; background: #f5f5f5; border-radius: 5px;">
            <p style="margin: 0 0 10px 0;">
                <strong>Status:</strong> <span style="color: green;">✓ Active</span>
            </p>
            <p style="margin: 0 0 10px 0;">
                <strong>Free Until:</strong> March 31, 2026
            </p>
            <p style="margin: 0 0 10px 0;">
                <strong>Days Remaining:</strong> <?php echo $days_remaining; ?> days
            </p>
            <a href="<?php echo esc_url($api_url . '/login'); ?>" class="button button-primary">Login</a>
            <a href="<?php echo esc_url($api_url . '/register'); ?>" class="button">Sign Up</a>
        </div>
        <?php
        
        echo $args['after_widget'];
    }
}

register_widget('Nexora_Status_Widget');
?>
```

---

## Template Pages Ready-to-Use

### Home Page Content Block

```markdown
## One Platform. Infinite Possibilities.

Nexora Suite brings together 25+ essential business apps in a single, 
integrated platform. Manage everything from accounting to customer support.

### ✨ Free Until March 31, 2026

All features completely free during our beta period.

[Explore All Features] [Get Started Free]

## Featured Modules

[nexora_modules]

## Why Choose Nexora?

### 🚀 Unified Platform
Stop juggling multiple tools. Everything you need in one place.

### 💰 Cost Effective
Pay once, get access to 25+ modules instead of paying for each separately.

### 🔐 Secure
Enterprise-grade security with encrypted data and secure authentication.

### 📱 Mobile Ready
Access your business on any device, anytime, anywhere.

### 🔗 Integrated
All modules work seamlessly together for maximum efficiency.

## Pricing

[nexora_pricing_table]

## What Our Users Say

> "Nexora Suite transformed how we manage our business. Best investment ever!"
> — Sarah Johnson, Small Business Owner

> "The integration between modules is seamless. Saves us hours every week."
> — Michael Chen, Operations Manager

> "Great support and continuous improvements. Highly recommended!"
> — Lisa Patel, Enterprise Manager

## Get Started Today

[nexora_cta]

---

### Quick Links
- [Documentation](https://docs.nexora.com)
- [Feature Tour](https://nexora.com/features)
- [Security](https://nexora.com/security)
- [Contact Us](https://aidniglobal.in/contact)
```

---

## SEO Optimization

Add to WordPress `header.php`:

```html
<!-- Nexora Suite SEO Tags -->
<meta name="description" content="Nexora Suite - Free business management platform with 25+ integrated modules. Accounting, POS, payroll, inventory, and more. 100% free until March 31, 2026.">
<meta name="keywords" content="business management software, accounting software, POS system, inventory management, payroll software, CRM system, Nexora Suite">
<meta property="og:title" content="Nexora Suite - Free Business Management Platform">
<meta property="og:description" content="All-in-one business management. 25+ integrated modules. 100% free until March 31, 2026.">
<meta property="og:type" content="website">
<meta property="og:image" content="https://aidniglobal.in/nexora-logo.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Nexora Suite - Business Management Made Easy">
<meta name="twitter:description" content="100% free business management software with 25+ modules. Free until March 31, 2026.">
```

---

## Analytics Tracking

Add Google Analytics for Nexora tracking:

```javascript
<!-- Nexora Suite Conversion Tracking -->
<script>
gtag('event', 'page_view', {
    'page_title': 'Nexora Suite Landing',
    'page_location': '/nexora-suite/'
});

// Track signup clicks
document.getElementById('nexora-signup-btn').addEventListener('click', function() {
    gtag('event', 'conversion', {
        'value': 0,
        'currency': 'USD',
        'transaction_id': 'nexora_signup_' + Date.now()
    });
});
</script>
```

---

## Email Campaign Template

**Subject**: 🚀 Introducing Nexora Suite - Free Business Management Platform

**Body**:
```
Hi [Name],

We're excited to announce Nexora Suite - a comprehensive business management 
platform with 25+ integrated modules, completely FREE until March 31, 2026.

## What You Get:
✅ Professional Accounting (Nexora Books)
✅ Point of Sale System (Nexora POS)
✅ Inventory Management (Nexora Inventory)
✅ Payroll & HR (Nexora Payroll)
✅ CRM System (Nexora CRM)
✅ Appointment Scheduling (Nexora Bookings)
✅ And 19 more powerful modules...

## Special Beta Offer:
Sign up now and get 50% LIFETIME DISCOUNT when premium features launch!

[Get Started Free - No Credit Card Required]

Questions? Our support team is here to help.

Best regards,
The Nexora Suite Team

---
Free until March 31, 2026 | Learn More at aidniglobal.in/nexora-suite
```

---

## Monthly Newsletter Template

```
NEXORA SUITE BETA UPDATE - [MONTH]

🎉 What's New This Month:

[Feature updates and improvements]

📊 By The Numbers:
- X users joined
- Y modules used
- Z data processed

💡 Feature Highlight:
[Spotlight on one important module/feature]

🐛 Fixes & Improvements:
- [List of improvements]

📅 Coming Next Month:
[Sneak preview of upcoming features]

🎁 Special Offer:
[Limited-time promotion for beta users]

---

Questions? Reply to this email or visit support.nexora.com
```

---

## Deployment Verification Checklist

- [ ] WordPress pages created
- [ ] Navigation menu updated
- [ ] Shortcodes tested
- [ ] Pricing table displays correctly
- [ ] CTA buttons link to correct API URL
- [ ] Mobile responsiveness verified
- [ ] SEO tags configured
- [ ] Analytics tracking working
- [ ] Email campaigns ready
- [ ] Backup created before deployment
- [ ] SSL certificate active
- [ ] 404 page customized
- [ ] Contact form working

---

**Your WordPress integration is ready!**

For more help, visit: https://docs.nexora.com/wordpress
