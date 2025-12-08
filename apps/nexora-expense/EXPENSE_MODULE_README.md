# Nexora Expense Module

A complete expense management system with full CRUD API endpoints, file upload support, and a modern Vue.js frontend.

## Features

✅ **Expense Management**
- Create, read, update, and delete expense reports
- Filter and search expenses by title, status, and category
- Multiple status tracking (Draft, Submitted, Approved, Rejected)
- Pagination support

✅ **Category Management**
- Create and manage expense categories
- Assign expenses to categories
- Category CRUD operations

✅ **File Attachments**
- Upload multiple file types (images, PDFs, Office documents)
- Download and delete attachments
- File type validation
- Secure file storage

✅ **User Authentication**
- JWT-based authentication
- Role-based access control (admin, manager, user)
- Login and registration endpoints

✅ **Modern UI**
- Vue.js 3 frontend with Vite
- Responsive design
- Category management interface
- Expense list with filtering
- Detail view with attachments
- Form for creating/editing expenses

## Backend Setup

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

#### Expenses
- `GET /api/expenses` - List all expenses (paginated)
  - Query params: `page`, `per_page`, `status`, `category_id`
- `GET /api/expenses/<id>` - Get single expense details
- `POST /api/expenses` - Create new expense
- `PUT /api/expenses/<id>` - Update expense
- `DELETE /api/expenses/<id>` - Delete expense

#### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category
- `PUT /api/categories/<id>` - Update category
- `DELETE /api/categories/<id>` - Delete category

#### File Attachments
- `POST /api/expenses/<id>/upload` - Upload file to expense
- `GET /api/attachments/<id>` - Download attachment
- `DELETE /api/attachments/<id>` - Delete attachment

#### Health Check
- `GET /api/health` - Service health status

### Database Models

**User**
- id, username, email, password, role, is_active, created_at

**ExpenseReport**
- id, title, amount, date, description, status, category_id, created_by, created_at
- Relationships: category (Category), attachments (Attachment)

**Category**
- id, name, description, created_at

**Attachment**
- id, filename, filepath, mimetype, expense_id, uploaded_at

### Requirements

Install backend dependencies:
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:
```
DATABASE_URL=sqlite:///app.db
JWT_SECRET=your-secret-key-here
FLASK_ENV=development
```

### Running the Backend

```bash
python app.py
```

The API will be available at `http://localhost:5000/api`

## Frontend Setup

### Requirements

Install frontend dependencies:
```bash
cd frontend
npm install
```

### Environment Variables

Create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:5000/api
```

### Running the Frontend

Development server:
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

## File Upload Configuration

- **Allowed extensions**: png, jpg, jpeg, gif, pdf, doc, docx, xls, xlsx
- **Max file size**: 16 MB
- **Storage location**: `./uploads/` folder
- **File naming**: UUID-based to avoid conflicts

## Frontend Pages

### Dashboard
Overview of expense statistics

### Expenses List
- View all expenses with pagination
- Filter by title, status, and category
- Quick actions: view, edit, delete

### Expense Detail
- Full expense details
- Download attachments
- View related category
- Delete option

### Expense Form
- Create new expenses
- Edit existing expenses
- Multi-file upload
- Category selection
- Status management

### Categories
- Manage expense categories
- Create/edit/delete categories
- Modal-based interface

## API Usage Examples

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "password123",
    "role": "user"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "password123"
  }'
```

### Create Expense
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Flight Ticket",
    "amount": 450.50,
    "category_id": 1,
    "description": "Business trip to NYC",
    "status": "draft"
  }'
```

### Upload File
```bash
curl -X POST http://localhost:5000/api/expenses/1/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@receipt.pdf"
```

### List Expenses
```bash
curl -X GET 'http://localhost:5000/api/expenses?page=1&per_page=10&status=approved' \
  -H "Authorization: Bearer <token>"
```

## Architecture

```
nexora-expense/
├── app.py                 # Flask app with all endpoints and models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── frontend/             # Vue.js application
│   ├── src/
│   │   ├── pages/       # Vue pages (Expenses, Categories, etc)
│   │   ├── components/  # Vue components (Sidebar, etc)
│   │   ├── services/    # API service layer
│   │   ├── router/      # Vue Router configuration
│   │   └── App.vue      # Root component
│   ├── package.json     # Frontend dependencies
│   └── vite.config.js   # Vite configuration
└── uploads/             # File upload directory
```

## Security Notes

1. **JWT Secret**: Change the default JWT secret in production
2. **Database**: Use PostgreSQL instead of SQLite in production
3. **File Upload**: Only whitelisted file types are accepted
4. **CORS**: Configure CORS headers for production
5. **Password**: Should be hashed (update in production)
6. **Rate Limiting**: Should be implemented in production

## Testing

Run backend tests:
```bash
pytest tests.py
```

## Docker Deployment

Build image:
```bash
docker build -t nexora-expense .
```

Run container:
```bash
docker run -p 5000:5000 -e DATABASE_URL="postgresql://..." nexora-expense
```

## Development Notes

- Backend uses Flask with SQLAlchemy ORM
- Frontend uses Vue 3 with Vite bundler
- JWT tokens for API authentication
- Axios for HTTP requests
- Vue Router for navigation
- File uploads with Werkzeug

## License

MIT
