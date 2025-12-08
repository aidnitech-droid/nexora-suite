# Nexora Suite - Production Environment Configuration

## Environment Variables Template

Create `.env.production` with these settings:

```bash
# ==================== GENERAL ====================
FLASK_ENV=production
DEBUG=false
DEMO_MODE=false

# ==================== SECURITY ====================
# Generate secure secret key: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-very-secure-random-secret-key-here-change-this
JWT_SECRET=your-jwt-secret-key-here-change-this
NEXORA_HOME_SECRET=your-home-secret-key-here

# ==================== DATABASE ====================
# PostgreSQL (Recommended for production)
DATABASE_URL=postgresql://nexora_prod:secure_password_here@db.nexora.com:5432/nexora_production
SQLALCHEMY_DATABASE_URI=${DATABASE_URL}

# ==================== API CONFIGURATION ====================
API_VERSION=v1
API_HOST=api.nexora.com
API_PORT=443
API_PROTOCOL=https

# ==================== JWT CONFIGURATION ====================
JWT_SECRET_KEY=${JWT_SECRET}
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 hours in seconds
JWT_ALGORITHM=HS256

# ==================== CORS & SECURITY ====================
ALLOWED_ORIGINS=https://aidniglobal.in,https://app.nexora.com,https://admin.nexora.com
CORS_ENABLED=true
CORS_CREDENTIALS=true
CORS_ALLOW_HEADERS=Content-Type,Authorization
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,PATCH

# ==================== EMAIL CONFIGURATION ====================
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your-sendgrid-api-key-here
MAIL_DEFAULT_SENDER=noreply@nexora.com
SUPPORT_EMAIL=support@nexora.com

# ==================== PRICING & LICENSING ====================
FREE_UNTIL_DATE=2026-03-31
PRICING_ACTIVE_FROM=2026-04-01
SUBSCRIPTION_API_KEY=your-subscription-service-key-here

# ==================== LOGGING ====================
LOG_LEVEL=INFO
LOG_FILE=/var/log/nexora/app.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=10

# ==================== MONITORING ====================
SENTRY_DSN=https://your-sentry-key@sentry.io/your-project-id
NEWRELIC_LICENSE_KEY=your-newrelic-key-here
DATADOG_API_KEY=your-datadog-key-here

# ==================== STORAGE ====================
STORAGE_TYPE=s3
S3_BUCKET=nexora-prod-data
S3_REGION=us-east-1
S3_ACCESS_KEY=your-aws-access-key
S3_SECRET_KEY=your-aws-secret-key

# ==================== CACHE ====================
CACHE_TYPE=redis
REDIS_URL=redis://cache.nexora.com:6379/0
CACHE_DEFAULT_TIMEOUT=300

# ==================== RATE LIMITING ====================
RATELIMIT_ENABLED=true
RATELIMIT_DEFAULT=100/hour
RATELIMIT_API=1000/hour

# ==================== BACKUP ====================
BACKUP_ENABLED=true
BACKUP_SCHEDULE=daily
BACKUP_RETENTION_DAYS=30
BACKUP_LOCATION=s3://nexora-backups/

# ==================== FEATURES ====================
ENABLE_2FA=true
ENABLE_WEBHOOKS=true
ENABLE_API_KEYS=true
ENABLE_AUDIT_LOG=true
ENABLE_EMAIL_VERIFICATION=true

# ==================== PERFORMANCE ====================
DATABASE_POOL_SIZE=20
DATABASE_POOL_RECYCLE=3600
DATABASE_POOL_PRE_PING=true
MAX_CONTENT_LENGTH=52428800  # 50MB

# ==================== BUSINESS SETTINGS ====================
COMPANY_NAME=Nexora Inc
COMPANY_WEBSITE=https://nexora.com
COMPANY_SUPPORT_URL=https://support.nexora.com
COMPANY_DOCS_URL=https://docs.nexora.com

# ==================== WORDPRESS INTEGRATION ====================
WORDPRESS_SITE_URL=https://aidniglobal.in
WORDPRESS_API_URL=https://aidniglobal.in/wp-json/v2
WORDPRESS_API_KEY=your-wordpress-api-key-here
WORDPRESS_EMBED_ENABLED=true
```

---

## Environment Variables by Service

### nexora-home
```bash
PORT=5060
FLASK_ENV=production
SECRET_KEY=home-service-secret-key
DEMO_MODE=false
DATABASE_URL=postgresql://nexora_prod:password@db/nexora
```

### nexora-bookings
```bash
PORT=5000
FLASK_ENV=production
JWT_SECRET=bookings-jwt-secret
DATABASE_URL=postgresql://nexora_prod:password@db/nexora
DEMO_MODE=false
```

### nexora-routeiq
```bash
PORT=5050
FLASK_ENV=production
DEMO_MODE=false
```

---

## Kubernetes Deployment (Optional)

Create `k8s-deployment.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nexora-prod

---
apiVersion: v1
kind: Secret
metadata:
  name: nexora-secrets
  namespace: nexora-prod
type: Opaque
stringData:
  secret-key: "your-secret-key"
  jwt-secret: "your-jwt-secret"
  db-password: "your-db-password"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexora-home
  namespace: nexora-prod
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nexora-home
  template:
    metadata:
      labels:
        app: nexora-home
    spec:
      containers:
      - name: nexora-home
        image: nexora/home:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 5060
        env:
        - name: FLASK_ENV
          value: "production"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: nexora-secrets
              key: secret-key
        - name: DATABASE_URL
          value: "postgresql://nexora:password@postgres-svc:5432/nexora"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5060
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5060
          initialDelaySeconds: 10
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: nexora-home-svc
  namespace: nexora-prod
spec:
  selector:
    app: nexora-home
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5060

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexora-bookings
  namespace: nexora-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nexora-bookings
  template:
    metadata:
      labels:
        app: nexora-bookings
    spec:
      containers:
      - name: nexora-bookings
        image: nexora/bookings:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: nexora-secrets
              key: jwt-secret
        - name: DATABASE_URL
          value: "postgresql://nexora:password@postgres-svc:5432/nexora"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
apiVersion: v1
kind: Service
metadata:
  name: nexora-bookings-svc
  namespace: nexora-prod
spec:
  selector:
    app: nexora-bookings
  type: ClusterIP
  ports:
  - protocol: TCP
    port: 5000
    targetPort: 5000
```

Deploy with:
```bash
kubectl apply -f k8s-deployment.yaml
```

---

## Nginx Configuration for Production

Create `nginx-prod.conf`:

```nginx
# Main Nginx configuration for Nexora Suite production

upstream nexora_home {
    least_conn;
    server nexora-home:5060 max_fails=3 fail_timeout=30s;
    server nexora-home-2:5060 max_fails=3 fail_timeout=30s backup;
}

upstream nexora_bookings {
    least_conn;
    server nexora-bookings:5000 max_fails=3 fail_timeout=30s;
    server nexora-bookings-2:5000 max_fails=3 fail_timeout=30s;
    server nexora-bookings-3:5000 max_fails=3 fail_timeout=30s;
}

upstream nexora_routeiq {
    least_conn;
    server nexora-routeiq:5050 max_fails=3 fail_timeout=30s;
    server nexora-routeiq-2:5050 max_fails=3 fail_timeout=30s backup;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=general_limit:10m rate=50r/s;

# Cache settings
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=nexora_cache:10m max_size=1g inactive=60m;

# HTTPS redirect
server {
    listen 80;
    server_name *.nexora.com api.nexora.com nexora.com;
    return 301 https://$server_name$request_uri;
}

# Main HTTPS server
server {
    listen 443 ssl http2;
    server_name api.nexora.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/nexora.com.crt;
    ssl_certificate_key /etc/ssl/private/nexora.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5:!3DES;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

    # Logging
    access_log /var/log/nginx/nexora-access.log combined;
    error_log /var/log/nginx/nexora-error.log warn;

    # Body size limit
    client_max_body_size 50M;

    # Root location
    location = / {
        proxy_pass http://nexora_home/;
        proxy_redirect off;
    }

    # Home service
    location / {
        limit_req zone=general_limit burst=20 nodelay;
        proxy_pass http://nexora_home/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # Bookings API
    location /api/bookings/ {
        limit_req zone=api_limit burst=50 nodelay;
        proxy_pass http://nexora_bookings/api/bookings/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache nexora_cache;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        proxy_cache_valid 200 10m;
        proxy_cache_use_stale error timeout invalid_header updating;
    }

    # RouteIQ API
    location /api/routeiq/ {
        limit_req zone=api_limit burst=50 nodelay;
        proxy_pass http://nexora_routeiq/api/routeiq/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health checks
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    location /api/health {
        access_log off;
        proxy_pass http://nexora_bookings/api/health;
        add_header Content-Type application/json;
    }
}
```

Deploy Nginx:
```bash
docker run -d \
  --name nexora-nginx \
  -p 80:80 \
  -p 443:443 \
  -v /path/to/nginx-prod.conf:/etc/nginx/nginx.conf:ro \
  -v /path/to/ssl:/etc/ssl:ro \
  -v /var/cache/nginx:/var/cache/nginx \
  nginx:alpine
```

---

## Monitoring & Alerting Setup

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: nexora-suite

scrape_configs:
  - job_name: 'nexora-home'
    static_configs:
      - targets: ['localhost:5060']

  - job_name: 'nexora-bookings'
    static_configs:
      - targets: ['localhost:5000']

  - job_name: 'nexora-routeiq'
    static_configs:
      - targets: ['localhost:5050']

  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:5432']
```

### Alert Rules

```yaml
# alerts.yml
groups:
  - name: nexora_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(flask_http_request_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"

      - alert: DatabaseConnectionPoolExhausted
        expr: db_connection_pool_available < 2
        for: 1m
        annotations:
          summary: "Database connection pool running low"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        annotations:
          summary: "Service {{ $labels.job }} is down"
```

---

## Backup & Recovery Procedures

### Automated Daily Backup Script

```bash
#!/bin/bash
# backup_nexora.sh - Run this daily via cron

BACKUP_DIR="/backups/nexora"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
PGPASSWORD=secure_password pg_dump \
  -h db.nexora.com \
  -U nexora_prod \
  -d nexora_production \
  | gzip > $BACKUP_DIR/nexora_db_${TIMESTAMP}.sql.gz

# Backup application files
tar -czf $BACKUP_DIR/nexora_app_${TIMESTAMP}.tar.gz \
  /apps/nexora-home \
  /apps/nexora-bookings \
  /apps/nexora-routeiq

# Upload to S3
aws s3 cp $BACKUP_DIR/nexora_db_${TIMESTAMP}.sql.gz s3://nexora-backups/database/
aws s3 cp $BACKUP_DIR/nexora_app_${TIMESTAMP}.tar.gz s3://nexora-backups/app/

# Clean old local backups
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed at $TIMESTAMP"
```

Add to crontab:
```bash
0 2 * * * /scripts/backup_nexora.sh >> /var/log/nexora_backup.log 2>&1
```

### Recovery Procedure

```bash
#!/bin/bash
# recover_nexora.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Stop services
docker-compose down

# Restore database
gunzip < $BACKUP_FILE | PGPASSWORD=password psql \
  -h db.nexora.com \
  -U nexora_prod \
  -d nexora_production

# Restart services
docker-compose up -d

echo "Recovery completed from $BACKUP_FILE"
```

---

## Health Check Endpoints

```bash
# Service health checks
curl -I http://localhost:5060/health
curl -I http://localhost:5000/api/health
curl -I http://localhost:5050/api/health

# Database connectivity
curl -s http://localhost:5060/api/db-status | jq .

# Full system status
curl -s http://localhost:5060/api/system-status | jq .
```

---

## Performance Tuning

### PostgreSQL Optimization

```sql
-- Connection pooling
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET work_mem = '10MB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';
ALTER SYSTEM SET random_page_cost = 1.1;

-- Apply changes
SELECT pg_reload_conf();
```

### Flask Application Tuning

```python
# config.py for production
class ProductionConfig:
    # Database
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_POOL_PRE_PING = True
    SQLALCHEMY_ECHO = False
    
    # Caching
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://cache:6379/0'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Sessions
    PERMANENT_SESSION_LIFETIME = 86400
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security
    JSON_SORT_KEYS = False
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
```

---

## Deployment Checklist

- [ ] All environment variables configured
- [ ] SSL certificates installed and valid
- [ ] Database backed up
- [ ] Monitoring systems active
- [ ] Nginx/reverse proxy configured
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Logging configured
- [ ] Alerting rules set
- [ ] Backup scripts scheduled
- [ ] Health checks verified
- [ ] Load testing passed
- [ ] Security audit completed
- [ ] Team trained on procedures

---

**Production deployment is now ready!**

For more information, see BETA_DEPLOYMENT.md
