# Nexora Suite - PythonAnywhere Deployment Guide

**Date**: December 8, 2025  
**Status**: Ready for Deployment  
**Free Until**: March 31, 2026

---

## 🚀 Quick Deployment Summary

Nexora Suite is now ready to deploy on PythonAnywhere with all these features:
- ✅ Pricing guard (FREE until March 31, 2026)
- ✅ Global pricing banner on all pages
- ✅ WordPress integration content
- ✅ Production configuration
- ✅ 25+ integrated business modules

---

## 📋 Pre-Deployment Checklist

- [ ] PythonAnywhere account created (free or paid)
- [ ] GitHub repository cloned
- [ ] Environment variables configured
- [ ] Database setup (if using PostgreSQL)
- [ ] SSL certificate (PythonAnywhere provides free)

---

## 🔧 Step 1: Clone Repository on PythonAnywhere

### Via PythonAnywhere Web Console:

```bash
# Log in to PythonAnywhere Bash Console

# Clone the repository
git clone https://github.com/aidnitech-droid/nexora-suite.git

# Navigate to directory
cd nexora-suite

# Check Python version
python --version  # Should be 3.8+
```

---

## 📦 Step 2: Create Virtual Environment

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.9 nexora

# Activate virtual environment
workon nexora

# Install dependencies
pip install -r apps/nexora-home/requirements.txt
pip install -r apps/nexora-bookings/requirements.txt
pip install -r apps/nexora-routeiq/requirements.txt

# Install additional dependencies for PythonAnywhere
pip install flask-cors
pip install python-dotenv
```

---

## ⚙️ Step 3: Configure Environment Variables

### Create `.env` file in `/home/username/nexora-suite/`

```bash
# Create the file
nano .env
```

**Paste this content:**

```bash
# ==================== GENERAL ====================
FLASK_ENV=production
DEBUG=false
DEMO_MODE=false

# ==================== SECURITY ====================
SECRET_KEY=your-super-secret-key-change-this-now
JWT_SECRET=your-jwt-secret-change-this-now
NEXORA_HOME_SECRET=your-home-secret-change-this-now

# ==================== DATABASE ====================
# For PythonAnywhere, use SQLite (default)
# DATABASE_URL=sqlite:///nexora.db
# OR use PostgreSQL if available
# DATABASE_URL=postgresql://user:password@db.example.com:5432/nexora

# ==================== PRICING ====================
FREE_UNTIL_DATE=2026-03-31
PRICING_ACTIVE_FROM=2026-04-01

# ==================== EMAIL (Optional) ====================
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@nexora.com

# ==================== LOGGING ====================
LOG_LEVEL=INFO
```

**Save**: Press `Ctrl+X`, then `Y`, then `Enter`

---

## 🌐 Step 4: Create Web App on PythonAnywhere

### Option A: Manual WSGI Configuration

1. Go to **Web** tab on PythonAnywhere
2. Click **Add a new web app**
3. Select **Manual configuration**
4. Choose **Python 3.9**
5. Click through to finish

### Option B: Using PythonAnywhere's Quick Start

1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose your domain (e.g., `yourusername.pythonanywhere.com`)
4. Select **Flask**
5. Choose **Python 3.9**

---

## 🔗 Step 5: Configure WSGI File

Edit the WSGI file (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
# ==================== WSGI Configuration ====================
import sys
import os
from pathlib import Path

# Add the project directory to the sys.path
project_folder = '/home/yourusername/nexora-suite'
sys.path.insert(0, project_folder)

# Load environment variables
from dotenv import load_dotenv
env_path = os.path.join(project_folder, '.env')
load_dotenv(env_path)

# Import and run the Flask app
from apps.nexora_home.app import app

# This is the WSGI application
application = app

# Error handling
if __name__ == "__main__":
    application.run()
```

**Replace `yourusername` with your actual PythonAnywhere username**

---

## 📁 Step 6: Configure Static Files & Media

In PythonAnywhere **Web** tab, scroll to **Static files**:

### Add these mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/nexora-suite/apps/nexora-home/static/` |
| `/js/` | `/home/yourusername/nexora-suite/apps/nexora-home/static/js/` |
| `/css/` | `/home/yourusername/nexora-suite/apps/nexora-home/static/css/` |

---

## 🔄 Step 7: Reload Web App

In PythonAnywhere **Web** tab, click the green **Reload** button at the top.

This will restart your application with the new configuration.

---

## ✅ Step 8: Verify Deployment

### Test the application:

```bash
# In PythonAnywhere Bash Console

# Test if app runs
cd ~/nexora-suite
workon nexora
python -c "from apps.nexora_home.app import app; print('App loaded successfully!')"

# Check pricing guard is loaded
python -c "from common.utils.pricing_guard import is_free_tier_active; print(f'Free tier active: {is_free_tier_active()}')"
```

### In Browser:

1. Visit: `https://yourusername.pythonanywhere.com`
2. You should see:
   - ✅ Nexora Suite homepage
   - ✅ **Green banner**: "Free until March 31, 2026"
   - ✅ Demo login link
   - ✅ Navigation menu

---

## 🔐 Step 9: Enable HTTPS/SSL

PythonAnywhere provides free HTTPS. In **Web** tab:

1. Scroll to **Security**
2. Click **Enable HTTPS**
3. Accept the free Let's Encrypt certificate

Your app is now secure: `https://yourusername.pythonanywhere.com`

---

## 📊 Step 10: Demo Credentials

The app includes built-in demo credentials:

| Field | Value |
|-------|-------|
| **Email** | demo@nexora.com |
| **Password** | Demo1234 |

Try logging in to verify everything works!

---

## 🌍 Step 11: Custom Domain Setup

To use your own domain (e.g., nexora.aidniglobal.in):

### In PythonAnywhere Web Tab:

1. Go to **Web** → Your web app
2. Find **Web app name** → Click **Change domain**
3. Enter: `nexora.aidniglobal.in`
4. Click **Save**

### In Your Domain Provider (aidniglobal.in):

1. Log in to your domain provider
2. Find **DNS Settings**
3. Add a **CNAME** record:
   - **Name**: `nexora`
   - **Value**: `yourusername.pythonanywhere.com`
   - **TTL**: 3600

4. Wait 24-48 hours for DNS propagation

### Enable HTTPS for Custom Domain:

In PythonAnywhere **Web** tab:
1. Scroll to **Security**
2. Click **Add new certificate**
3. Select your custom domain
4. Get free Let's Encrypt certificate

---

## 📈 Monitoring & Logs

### View Application Logs:

In PythonAnywhere **Web** tab:
- **Error log**: Click the link to view errors
- **Server log**: View request logs
- **Access log**: View all HTTP requests

### Common Issues & Solutions:

**Issue**: ImportError: No module named 'app'
```bash
# Solution: Make sure WSGI path is correct
# Edit WSGI file and verify the import path
```

**Issue**: 502 Bad Gateway
```bash
# Solution: Check error log, reload web app
# Go to Web tab → Click Reload
```

**Issue**: Pricing banner not showing
```bash
# Solution: Verify pricing_guard.py is in common/utils/
cd ~/nexora-suite
ls -la common/utils/pricing_guard.py
```

---

## 🔄 Updating Code

When you make changes and push to GitHub:

```bash
# In PythonAnywhere Bash Console
cd ~/nexora-suite
git pull origin main
workon nexora
pip install -r apps/nexora-home/requirements.txt
```

Then click **Reload** in Web tab.

---

## 💾 Database Setup (Optional)

### For SQLite (Default - No Setup Needed):
- Database file created automatically at `/home/yourusername/nexora-suite/apps/nexora-home/nexora_home.db`
- Perfect for testing and small deployments

### For PostgreSQL:

1. Check if PostgreSQL is available on PythonAnywhere
2. Create database:
   ```bash
   createdb nexora_prod
   ```

3. Update `.env`:
   ```bash
   DATABASE_URL=postgresql://yourusername:password@localhost:5432/nexora_prod
   ```

4. Reload web app

---

## 📞 Support & Troubleshooting

### Common PythonAnywhere Issues:

1. **Module not found**: Reinstall requirements
   ```bash
   workon nexora
   pip install --upgrade -r apps/nexora-home/requirements.txt
   ```

2. **Path issues**: Verify web app directory
   - Go to Web tab → Check **Virtualenv path**
   - Should be: `/home/yourusername/.virtualenvs/nexora`

3. **Permission denied**: Fix file permissions
   ```bash
   chmod 755 ~/nexora-suite
   chmod 755 ~/nexora-suite/apps
   ```

4. **Pricing banner not showing**: Check templates
   ```bash
   ls -la apps/nexora-home/templates/base.html
   grep "March 31" apps/nexora-home/templates/base.html
   ```

---

## 🚀 Final Checklist Before Promoting

- [ ] App loads without errors
- [ ] Homepage displays correctly
- [ ] Pricing banner visible ("Free until March 31, 2026")
- [ ] Demo login works (demo@nexora.com / Demo1234)
- [ ] All navigation links work
- [ ] HTTPS enabled and valid
- [ ] Custom domain configured (if applicable)
- [ ] Logs show no errors
- [ ] Performance acceptable (fast load times)
- [ ] Mobile responsive

---

## 📢 Ready to Promote on Website

Once verified on PythonAnywhere, you can promote:

### Add to aidniglobal.in WordPress:

Use the content from **WORDPRESS_INTEGRATION.md**:

1. Create WordPress pages:
   - Landing page: `/nexora-suite`
   - Pricing: `/pricing`
   - Features: `/features`

2. Add shortcodes:
   ```
   [nexora_pricing_table]
   [nexora_modules]
   [nexora_cta]
   ```

3. Link to PythonAnywhere app:
   ```html
   <a href="https://nexora.aidniglobal.in/login">Login to Nexora Suite</a>
   <a href="https://nexora.aidniglobal.in/register">Sign Up Free</a>
   ```

---

## 🎉 Deployment Complete!

Your Nexora Suite is now live on PythonAnywhere and ready to promote on your website.

### Key Features Live:
✅ FREE until March 31, 2026  
✅ Global pricing banner on all pages  
✅ 25+ business modules  
✅ Demo mode for testing  
✅ Production-ready  
✅ WordPress integrated  

---

## 📝 Next Steps

1. **This week**: Deploy on PythonAnywhere ✓
2. **Next week**: Promote on aidniglobal.in WordPress
3. **Week 3**: Collect user feedback
4. **Week 4**: Plan roadmap improvements

---

## 💪 You're All Set!

Your Nexora Suite beta is production-ready and deployed!

**Free until March 31, 2026** 🎉

Questions? Check the other documentation files:
- `BETA_DEPLOYMENT.md` - Full deployment guide
- `WORDPRESS_INTEGRATION.md` - WordPress setup
- `PRODUCTION_CONFIG.md` - Advanced configuration

Good luck with your launch! 🚀
