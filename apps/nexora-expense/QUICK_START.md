# Nexora Expense Module - Quick Start Guide

## 🚀 Getting Started

### Backend Setup

1. **Install dependencies:**
   ```bash
   cd /workspaces/nexora-suite/apps/nexora-expense
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python app.py
   ```
   Server runs at: `http://localhost:5000`

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend runs at: `http://localhost:5173`

---

## 📚 Module Overview

### What's Included

✅ **3 Database Models**
- ExpenseReport (main entity)
- Category (classification)
- Attachment (file storage)

✅ **20 API Endpoints**
- Authentication (2)
- Items Management (5)
- Categories (4)
- Expenses (6)
- File Upload/Download (2)
- Health Check (1)

✅ **4 Frontend Pages**
- Expenses List
- Expense Form (Create/Edit)
- Expense Detail View
- Category Management

✅ **Full Features**
- User authentication with JWT
- Role-based access control
- File upload with validation
- Pagination & filtering
- Responsive UI design

---

## 🔌 API Quick Reference

### Authentication
```bash
# Register
POST /api/auth/register
Body: { username, email, password, role }

# Login
POST /api/auth/login
Body: { username, password }
```

### Expenses
```bash
# List (with filters)
GET /api/expenses?page=1&per_page=10&status=draft&category_id=1
Header: Authorization: Bearer <token>

# Get detail
GET /api/expenses/{id}
Header: Authorization: Bearer <token>

# Create
POST /api/expenses
Header: Authorization: Bearer <token>
Body: { title, amount, category_id, description, status }

# Update
PUT /api/expenses/{id}
Header: Authorization: Bearer <token>

# Delete
DELETE /api/expenses/{id}
Header: Authorization: Bearer <token>
```

### File Upload
```bash
# Upload file to expense
POST /api/expenses/{id}/upload
Header: Authorization: Bearer <token>
Body: multipart/form-data (file)

# Download file
GET /api/attachments/{id}

# Delete file
DELETE /api/attachments/{id}
Header: Authorization: Bearer <token>
```

### Categories
```bash
# List all
GET /api/categories

# Create
POST /api/categories
Body: { name, description }

# Update
PUT /api/categories/{id}
Body: { name, description }

# Delete
DELETE /api/categories/{id}
```

---

## 📱 Frontend Routes

| Page | Route | Purpose |
|------|-------|---------|
| Dashboard | `/dashboard` | Overview stats |
| Expenses | `/expenses` | List all expenses |
| Create Expense | `/expenses/new` | New expense form |
| Expense Detail | `/expenses/:id` | View details |
| Edit Expense | `/expenses/:id/edit` | Edit form |
| Categories | `/categories` | Manage categories |

---

## 📁 Project Structure

```
nexora-expense/
├── app.py                          # Flask application & models
├── requirements.txt                # Python deps
├── uploads/                        # File storage
├── EXPENSE_MODULE_README.md        # Full documentation
├── IMPLEMENTATION_CHECKLIST.md     # Features list
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Expenses.vue        # List & filter
    │   │   ├── ExpenseForm.vue     # Create/Edit
    │   │   ├── ExpenseDetail.vue   # View details
    │   │   ├── Categories.vue      # Manage categories
    │   │   └── ...
    │   │
    │   ├── services/
    │   │   ├── expenseService.js   # API calls
    │   │   └── api.js              # HTTP config
    │   │
    │   └── router/
    │       └── index.js            # Routes
    │
    └── package.json                # Dependencies
```

---

## 💾 Database Models

### ExpenseReport
| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary Key |
| title | String(255) | Required |
| amount | Decimal(12,2) | Required |
| date | DateTime | Auto: now() |
| description | Text | Optional |
| status | String(50) | draft/submitted/approved/rejected |
| category_id | Integer | FK to Category |
| created_by | Integer | FK to User |
| created_at | DateTime | Auto: now() |

### Category
| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary Key |
| name | String(120) | Unique, Required |
| description | Text | Optional |
| created_at | DateTime | Auto: now() |

### Attachment
| Field | Type | Notes |
|-------|------|-------|
| id | Integer | Primary Key |
| filename | String(255) | Original filename |
| filepath | String(1024) | Server path |
| mimetype | String(255) | File MIME type |
| expense_id | Integer | FK to ExpenseReport |
| uploaded_at | DateTime | Auto: now() |

---

## 🔐 Authentication

1. **Register** → Get user ID
2. **Login** → Get JWT token
3. **Use token** in Authorization header: `Bearer <token>`
4. **Token expires** in 24 hours

---

## 📤 File Upload Details

**Allowed Types:**
- Images: png, jpg, jpeg, gif
- Documents: pdf, doc, docx, xls, xlsx

**Limits:**
- Max size: 16 MB
- Multiple files per expense

**Storage:**
- Directory: `./uploads/`
- Naming: UUID-based (auto-generated)

---

## 🧪 Testing the API

### Using cURL

```bash
# 1. Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'

# 2. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# 3. Create category
TOKEN="your_token_here"
curl -X POST http://localhost:5000/api/categories \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Travel","description":"Travel expenses"}'

# 4. Create expense
curl -X POST http://localhost:5000/api/expenses \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Flight","amount":450.50,"category_id":1,"status":"draft"}'

# 5. Upload file
curl -X POST http://localhost:5000/api/expenses/1/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@receipt.pdf"

# 6. List expenses
curl -X GET "http://localhost:5000/api/expenses?page=1&per_page=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

## ⚙️ Configuration

**Environment Variables (.env):**
```
DATABASE_URL=sqlite:///app.db
JWT_SECRET=dev-secret-key-change-in-production
FLASK_ENV=development
```

**Frontend (.env):**
```
VITE_API_URL=http://localhost:5000/api
```

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm app.db
python app.py  # Creates fresh database
```

### Port Already in Use
```bash
# Backend (use different port)
python app.py  # Check app.py and change port=5000

# Frontend (Vite auto-finds port if 5173 busy)
npm run dev
```

### CORS Errors
- Check API_BASE_URL in frontend .env
- Ensure backend is running on correct port

### File Upload Fails
- Check `./uploads/` directory exists
- Verify file type is allowed
- Check file size < 16 MB

---

## 📚 Additional Resources

- **Full Docs:** See `EXPENSE_MODULE_README.md`
- **Checklist:** See `IMPLEMENTATION_CHECKLIST.md`
- **Flask Docs:** https://flask.palletsprojects.com/
- **Vue 3 Docs:** https://vuejs.org/
- **SQLAlchemy:** https://www.sqlalchemy.org/

---

## 🎉 You're Ready!

The expense module is fully implemented with:
- ✅ Complete backend API
- ✅ Database models
- ✅ File upload support
- ✅ Modern Vue.js frontend
- ✅ Full authentication
- ✅ Responsive UI

Start building! 🚀
