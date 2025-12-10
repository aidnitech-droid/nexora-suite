# 🎯 Nexora Suite - USER GUIDE

**Welcome to Nexora Suite!** Your complete business management platform.

---

## 🚀 Getting Started in 5 Minutes

### Step 1: Start the Application
```bash
cd /workspaces/nexora-suite

# Set to demo mode
export DEMO_MODE=true
export FLASK_ENV=development

# Start all services
docker-compose up -d

# Wait 30-60 seconds for services to start
```

### Step 2: Open in Your Browser
Visit these URLs:
- **Home/Dashboard**: http://localhost:5060
- **Route Planning**: http://localhost:5050
- **Bookings**: http://localhost:5000

### Step 3: Login with Demo Account
- **Email**: demo@nexora.com
- **Password**: Demo1234

---

## 📋 What You Can Do Right Now

### 🏠 Nexora Home (Dashboard)
- View all 25 available modules
- See features and benefits
- Sign in to access modules
- Explore the complete product

**Pages:**
- Home (landing page with features)
- Modules (grid view of all 25 modules)
- Login (demo account pre-filled)

### 🗺️ Nexora RouteIQ (Route Planner)
- Plan routes for sales teams
- Add multiple waypoints
- Choose travel profile (driving, cycling, walking)
- Calculate distance and time
- Save routes for future use

**How to use:**
1. Go to "Plan Route" page
2. Enter origin location (latitude, longitude)
3. Enter destination location
4. (Optional) Add waypoints
5. Click "Plan Route"
6. View results and save if needed

### 📅 Nexora Bookings (Appointment Scheduler)
- Schedule customer appointments
- Manage time slots
- Send reminders
- Track bookings

### 🔧 Nexora Service (Field Service Management)
- Create job tickets for field work
- Assign technicians to jobs
- Track technician skills
- Monitor job status (open → assigned → in progress → completed)
- Set priority levels (low, medium, high)

**How to use:**
1. Go to Job Tickets
2. Click "+ New Job Ticket"
3. Fill in customer info and priority
4. Click "Create Ticket"
5. View in the Job Tickets list

### 👨‍🔧 Manage Technicians
- Add technicians with skills
- Track availability
- Assign to jobs

---

## 🎨 User-Friendly Features in Every Module

### ✅ Professional Design
- Clean, modern interface
- Responsive design (works on mobile!)
- Easy navigation
- Professional color scheme

### ✅ Intuitive Navigation
- Top navigation bar
- Back buttons on detail pages
- Breadcrumb trails
- Clear page titles

### ✅ Quick Actions
- "+ Create" buttons on list pages
- Action menus on each item
- Edit/Delete options
- View details options

### ✅ Filtering & Search
- Search by keywords
- Filter by status, category, type
- Sort results
- Pagination support

### ✅ Forms & Validation
- Clear labels on all fields
- Required field indicators (*)
- Input validation
- Success/error messages
- Form error handling

### ✅ Status Indicators
- Color-coded status badges
- Priority indicators
- Progress tracking
- Activity logs

---

## 📊 Sample Data You Can Try

### Nexora Service - Sample Job Tickets
```
Customer: Acme Corp
Job: AC Unit Repair
Priority: High
Status: Open

Customer: Tech Solutions Ltd
Job: Server Maintenance
Priority: Medium
Status: In Progress
```

### Nexora RouteIQ - Sample Coordinates
**New York City Route:**
- Origin: 40.7128, -74.0060 (NYC)
- Destination: 40.7580, -73.9855 (Empire State Building)
- Try adding waypoints for more complex routes!

### Nexora Bookings - Sample Appointments
```
Customer: John Doe
Service: Consultation
Date: Tomorrow at 2 PM
Duration: 1 hour
```

---

## 🔑 Demo Credentials

All modules use the same credentials:
```
Email:    demo@nexora.com
Password: Demo1234
Role:     demo
```

---

## 💡 Tips & Tricks

### 1️⃣ Create Sample Data
- Each module has a "Create" button
- Fill in the form
- Click submit
- Your data is saved immediately!

### 2️⃣ Edit & Update
- Click "Edit" on any item
- Modify the information
- Save changes
- Changes appear instantly

### 3️⃣ Delete (Be Careful!)
- Click "Delete" button
- Confirm deletion
- Item is removed from the system

### 4️⃣ Filter & Search
- Use search boxes to find items quickly
- Use filter dropdowns to narrow results
- Combine filters for precise results

### 5️⃣ View Details
- Click "View" or "Details" to see full information
- Click back button to return to list
- Edit from detail page if needed

---

## 🆘 Troubleshooting

### Services Not Starting?
```bash
# Check if services are running
docker-compose ps

# View service logs
docker-compose logs nexora-home

# Restart services
docker-compose restart

# Complete restart
docker-compose down
docker-compose up -d
```

### Port Already in Use?
```bash
# Change ports in docker-compose.yml
# Or kill the process using the port
lsof -i :5060
kill -9 <PID>
```

### Can't Login?
- Use demo credentials: demo@nexora.com / Demo1234
- Make sure DEMO_MODE=true is set
- Check browser console for errors (F12)

### Slow Performance?
- Wait for services to fully start (60 seconds)
- Refresh the page (F5)
- Clear browser cache
- Check available RAM

---

## 📱 Mobile Access

All modules work on mobile devices!

### Access from Mobile:
1. Find your computer's IP address: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. On mobile, visit: `http://<your-ip>:5060`
3. Login with demo credentials
4. Enjoy Nexora Suite on the go!

---

## 🔒 Data & Security

### Demo Mode Safety
- In DEMO_MODE, DELETE operations are blocked
- This prevents accidental data loss
- Great for testing and learning!

### Your Data
- Created in SQLite (local database)
- Persisted in `./apps/<module>/app.db`
- Can be backed up easily
- Ready to migrate to production

---

## 🎓 Learning Paths

### For Beginners
1. Visit Home page
2. Explore Module grid
3. Read descriptions
4. Try creating sample data
5. Play with filters & search

### For Advanced Users
1. Check API endpoints
2. Integrate with your tools
3. Customize templates
4. Deploy to production
5. Configure settings

---

## 🔌 API Integration

Each module has a RESTful API:

```bash
# Example: Get all job tickets
curl http://localhost:5000/api/job-tickets

# Create a new job ticket
curl -X POST http://localhost:5000/api/job-tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Repair", "customer_name": "John"}'

# Get specific job ticket
curl http://localhost:5000/api/job-tickets/1

# Update job ticket
curl -X PUT http://localhost:5000/api/job-tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete job ticket
curl -X DELETE http://localhost:5000/api/job-tickets/1
```

---

## 📚 Module Descriptions

### Core Modules

**Nexora Home** - Dashboard & Portal
- Landing page for your platform
- Module directory
- User authentication

**Nexora Books** - Accounting
- Track income & expenses
- Generate financial reports
- Invoice management

**Nexora Payroll** - HR & Salary
- Manage employee payroll
- Track attendance
- Handle benefits

**Nexora Inventory** - Stock Management
- Track inventory levels
- Manage warehouse
- Process orders

**Nexora CRM** - Customer Management
- Store customer info
- Track interactions
- Manage sales pipeline

**Nexora Bookings** - Appointments
- Schedule appointments
- Send reminders
- Manage resources

**Nexora Service** - Field Service
- Create job tickets
- Assign technicians
- Track job status

**Nexora RouteIQ** - Route Planning
- Plan optimal routes
- Multiple waypoints
- Save favorite routes

---

## 💬 Need Help?

### Check Documentation
- README.md - Project overview
- PRODUCTION_CONFIG.md - Setup guide
- IMPLEMENTATION_COMPLETE.md - Features list
- BETA_DEPLOYMENT.md - Deployment guide

### Common Questions

**Q: Can I delete data?**
A: Yes! Click the Delete button. (In DEMO_MODE, this is blocked for safety)

**Q: Can I edit created data?**
A: Yes! Click Edit on any item, make changes, and save.

**Q: How do I change the port?**
A: Edit docker-compose.yml and change the port numbers.

**Q: Can I use this in production?**
A: Yes! Follow PRODUCTION_CONFIG.md for setup.

**Q: Is my data saved?**
A: Yes! Data is stored in SQLite database in each module folder.

---

## 🎉 You're All Set!

**Start exploring Nexora Suite now:**
1. Open http://localhost:5060
2. Login with demo@nexora.com / Demo1234
3. Try creating sample data
4. Explore all 25 modules
5. Customize for your business!

**Happy exploring! 🚀**

---

*Nexora Suite - Free until March 31, 2026*
