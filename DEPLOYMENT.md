# SignVerse AI - Complete Deployment Guide

Step-by-step guide to deploy the entire SignVerse AI system (Backend, ML Server, and Flutter App) to production.

## 📋 Table of Contents

- [Deployment Overview](#deployment-overview)
- [Local Development Setup](#local-development-setup)
- [Backend Deployment](#backend-deployment)
- [ML Server Deployment](#ml-server-deployment)
- [Flutter App Deployment](#flutter-app-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Monitoring & Maintenance](#monitoring--maintenance)

## 🎯 Deployment Overview

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Users                                │
├─────────────────────────────────────────────────────────┤
│                 Mobile App (Flutter)                    │
│  - Android (Google Play)                               │
│  - iOS (App Store)                                     │
│  - Web (Browser)                                       │
├─────────────────────────────────────────────────────────┤
│                Internet / Network                       │
├─────────────────────────────────────────────────────────┤
│         Cloud Server / Self-Hosted Server              │
│                                                         │
│  ┌─────────────────────────────────────────┐          │
│  │  Backend API (FastAPI)  - Port 8000    │          │
│  │  - Text-to-sign translation            │          │
│  │  - Sign animation delivery             │          │
│  │  - API routing                         │          │
│  └─────────────────────────────────────────┘          │
│                      │                                  │
│                      ▼                                  │
│  ┌─────────────────────────────────────────┐          │
│  │  ML Server (TensorFlow) - Port 8001    │          │
│  │  - Hand landmark extraction            │          │
│  │  - Sign recognition                   │          │
│  │  - Confidence scoring                 │          │
│  └─────────────────────────────────────────┘          │
│                      │                                  │
│                      ▼                                  │
│  ┌─────────────────────────────────────────┐          │
│  │  Storage                                │          │
│  │  - Models (.h5, .pkl)                 │          │
│  │  - Sign GIFs                          │          │
│  │  - Logs                               │          │
│  └─────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Local Development Setup

### Prerequisites

```bash
# System requirements
- Python 3.9+
- Node.js 16+ (optional, for web)
- Docker & Docker Compose (for containerized deployment)
- Git
- 2GB RAM minimum
- 1GB disk space

# Install Python dependencies
cd /path/to/Sign-Language
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend requirements
cd backend
pip install -r requirements.txt

# Install ML server requirements
cd ../ml_server
pip install -r requirements.txt  # Create if needed

# Install Flutter (if deploying mobile app)
# Visit https://flutter.dev/docs/get-started/install
```

### Quick Local Start

```bash
# From project root
python3 start_servers.py

# This starts:
# - Backend on http://localhost:8000
# - ML Server on http://localhost:8001

# In another terminal, test:
curl http://localhost:8000/api/health
curl http://localhost:8001/health
```

## 🐍 Backend Deployment

### Option 1: Standalone Server (Production)

**Using Gunicorn + Uvicorn**

```bash
cd backend

# Install production server
pip install gunicorn

# Create startup script
cat > run_production.sh << 'EOF'
#!/bin/bash
cd /path/to/Sign-Language/backend
source venv/bin/activate
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  app.main:app
EOF

chmod +x run_production.sh
./run_production.sh
```

### Option 2: Systemd Service (Linux)

```bash
# Create systemd service file
sudo nano /etc/systemd/system/signverse-backend.service

[Unit]
Description=SignVerse AI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/Sign-Language/backend
Environment="PATH=/var/www/Sign-Language/backend/venv/bin"
ExecStart=/var/www/Sign-Language/backend/venv/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable signverse-backend
sudo systemctl start signverse-backend

# Check status
sudo systemctl status signverse-backend

# View logs
sudo journalctl -u signverse-backend -f
```

### Option 3: PM2 (Node-like Process Manager)

```bash
# Install PM2
npm install -g pm2

# Create ecosystem config
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'signverse-backend',
      cwd: '/path/to/Sign-Language/backend',
      script: '/path/to/venv/bin/python',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 8000',
      instances: 4,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production'
      }
    }
  ]
};
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Environment Variables

Create `backend/.env`
```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# ML Server
ML_SERVER_URL=http://localhost:8001

# CORS
CORS_ORIGINS=["https://yourdomain.com","https://app.yourdomain.com"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/signverse/backend.log

# API
API_TITLE=SignVerse AI
API_VERSION=1.0.0
```

## 🤖 ML Server Deployment

### Option 1: Standalone Uvicorn (Production)

```bash
cd ml_server

# Run with multiple workers
python3 -m uvicorn main:app \
  --host 0.0.0.0 \
  --port 8001 \
  --workers 2 \
  --loop uvloop
```

### Option 2: Systemd Service (Linux)

```bash
# Create systemd service
sudo nano /etc/systemd/system/signverse-ml.service

[Unit]
Description=SignVerse AI ML Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/Sign-Language/ml_server
Environment="PATH=/var/www/Sign-Language/ml_server/venv_infer/bin"
ExecStart=/var/www/Sign-Language/ml_server/venv_infer/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable signverse-ml
sudo systemctl start signverse-ml

# Check status
sudo systemctl status signverse-ml
```

### Environment Variables

Create `ml_server/.env`
```env
# Server
HOST=0.0.0.0
PORT=8001
DEBUG=false

# Model
MODEL_PATH=./model/sign_model.h5
LABEL_MAP_PATH=./model/label_map.json
SCALER_PATH=./model/scaler.pkl

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/signverse/ml_server.log
```

## 📱 Flutter App Deployment

### Android Deployment (Google Play)

**Step 1: Build Release APK/Bundle**
```bash
cd sign_bridge

# Build App Bundle (recommended for Play Store)
flutter build appbundle --release

# Output: build/app/outputs/bundle/release/app-release.aab
```

**Step 2: Create Google Play Account**
- Go to https://play.google.com/console
- Create Developer account ($25 one-time fee)
- Create new app

**Step 3: Upload to Play Store**
1. Open Google Play Console
2. Select your app
3. Go to Release > Production
4. Click "Create release"
5. Upload `app-release.aab`
6. Fill app details:
   - Title, description
   - Screenshots (4-5 images)
   - Category, content rating
   - Privacy policy URL
7. Review and publish

**Step 4: Monitor Release**
```
- Initial review: 1-3 hours
- Full deployment: up to 24 hours
- Monitor: Play Console > Releases
```

### iOS Deployment (App Store)

**Step 1: Create Apple Developer Account**
- Go to https://developer.apple.com
- Enroll in Apple Developer Program ($99/year)
- Create Bundle ID: com.yourcompany.signverse

**Step 2: Build Release for App Store**
```bash
cd sign_bridge

# Build iOS app
flutter build ios --release

# Create IPA for submission
cd ios
xcodebuild -workspace Runner.xcworkspace \
  -scheme Runner \
  -configuration Release \
  -derivedDataPath build/ \
  -archivePath build/Runner.xcarchive archive

xcodebuild -exportArchive \
  -archivePath build/Runner.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/
```

**Step 3: Upload to App Store**
1. Open App Store Connect: https://appstoreconnect.apple.com
2. Create new app
3. Fill app information:
   - Name, subtitle, description
   - Keywords, category
   - Support URL, privacy policy
   - Screenshots, preview videos
4. Upload build via:
   - Xcode: Product > Archive > Distribute App
   - Or Transporter app (download from App Store)
5. Submit for review

**Step 4: Monitor Review**
```
- Review time: 24-48 hours typically
- May require additional info
- Monitor: App Store Connect > TestFlight or App Review
```

### Web Deployment

**Option 1: GitHub Pages (Free)**
```bash
cd sign_bridge

# Build web
flutter build web --release

# Create docs folder
mkdir -p docs
cp -r build/web/* docs/

# Push to GitHub
git add docs/
git commit -m "Deploy web app"
git push origin main

# Configure GitHub Pages
# Settings > Pages > Source > Deploy from branch > main/docs
# Your app is live at: https://yourusername.github.io/Sign-Language
```

**Option 2: Firebase Hosting**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize project
firebase init hosting

# Build and deploy
flutter build web --release
firebase deploy --only hosting
```

**Option 3: Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
flutter build web --release
netlify deploy --prod --dir=build/web
```

## 🐳 Docker Deployment

### Create Dockerfile for Backend

```dockerfile
# Dockerfile for backend
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY backend/app ./app
COPY backend/train_venv/lib/python3.*/site-packages ./venv/lib/python3.10/site-packages

# Expose port
EXPOSE 8000

# Run app
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Dockerfile for ML Server

```dockerfile
# Dockerfile for ML server
FROM tensorflow/tensorflow:latest

WORKDIR /app

# Install dependencies
COPY ml_server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and code
COPY ml_server/model ./model
COPY ml_server/main.py .

# Expose port
EXPOSE 8001

# Run app
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - ML_SERVER_URL=http://ml_server:8001
    depends_on:
      - ml_server
    volumes:
      - ./logs:/app/logs
    restart: always

  ml_server:
    build:
      context: .
      dockerfile: Dockerfile.ml
    ports:
      - "8001:8001"
    volumes:
      - ./logs:/app/logs
    restart: always

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - ml_server
    restart: always
```

**Deploy with Docker Compose**
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f ml_server

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment

### AWS Deployment (EC2 + RDS)

**1. Launch EC2 Instance**
```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install -y python3.10 python3-pip nginx

# Clone repository
git clone https://github.com/yourusername/Sign-Language.git
cd Sign-Language

# Setup virtual environments
python3 -m venv backend/venv
python3 -m venv ml_server/venv_infer

# Install packages
source backend/venv/bin/activate
pip install -r backend/requirements.txt

source ml_server/venv_infer/bin/activate
pip install -r ml_server/requirements.txt
```

**2. Configure Nginx Reverse Proxy**
```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/signverse

upstream backend {
    server 127.0.0.1:8000;
}

upstream ml_server {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ml/ {
        proxy_pass http://ml_server;
        proxy_set_header Host $host;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/signverse /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**3. Setup SSL (Free with Let's Encrypt)**
```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

### Google Cloud Deployment

**1. Create Cloud Run Services**
```bash
# Build and push backend to Container Registry
gcloud builds submit --tag gcr.io/your-project/backend backend/

# Deploy to Cloud Run
gcloud run deploy signverse-backend \
  --image gcr.io/your-project/backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars ML_SERVER_URL=https://signverse-ml-xyz.a.run.app

# Similar for ML server
gcloud builds submit --tag gcr.io/your-project/ml-server ml_server/
gcloud run deploy signverse-ml \
  --image gcr.io/your-project/ml-server \
  --platform managed \
  --region us-central1
```

### Heroku Deployment

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app" > backend/Procfile

# Login and deploy
heroku login
heroku create signverse-backend
heroku config:set ML_SERVER_URL=https://signverse-ml.herokuapp.com
git push heroku main

# View logs
heroku logs --tail
```

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Backend health
curl https://yourdomain.com/api/health

# ML Server health
curl https://yourdomain.com/ml/health

# Check response time
time curl https://yourdomain.com/api/health
```

### Monitoring Tools

**Option 1: New Relic**
```python
# In app.main:
from newrelic.agent import initialize
initialize('newrelic.ini')
```

**Option 2: Datadog**
```bash
# Install agent
pip install datadog-agent

# Configure in environment
export DD_API_KEY=your_key
export DD_SITE=datadoghq.com
```

**Option 3: Sentry (Error Tracking)**
```python
# In app.main:
import sentry_sdk
sentry_sdk.init("https://your-sentry-dsn@sentry.io/123456")
```

### Log Management

```bash
# View backend logs
tail -f /var/log/signverse/backend.log

# View ML server logs
tail -f /var/log/signverse/ml_server.log

# Rotate logs
cat > /etc/logrotate.d/signverse << 'EOF'
/var/log/signverse/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 640 www-data www-data
}
EOF
```

### Maintenance Scripts

```bash
#!/bin/bash
# maintenance.sh - Daily maintenance

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz /var/log/signverse/

# Clear old backups (keep last 30 days)
find . -name "logs_backup_*.tar.gz" -mtime +30 -delete

# Check disk space
df -h /var

# Restart services if needed
systemctl restart signverse-backend
systemctl restart signverse-ml
```

## 📋 Deployment Checklist

```
Pre-Deployment:
□ Update version numbers
□ Run tests: flutter test, pytest
□ Code review completed
□ Security audit passed
□ Database backups scheduled
□ SSL certificates ready
□ Domain DNS configured
□ API keys generated
□ Environment variables prepared

During Deployment:
□ Notify team
□ Monitor deployment process
□ Check health endpoints
□ Run smoke tests
□ Monitor error logs
□ Test critical features

Post-Deployment:
□ Verify all services running
□ Check app functionality
□ Monitor performance metrics
□ Monitor error rates
□ Review user feedback
□ Schedule post-deployment review
□ Document any issues
□ Update runbooks
```

## 🎯 Recommended Production Setup

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    │  (AWS ELB/ALB)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌────────┐           ┌────────┐          ┌────────┐
    │Backend │           │Backend │          │Backend │
    │Instance│           │Instance│          │Instance│
    │  (8000)│           │  (8000)│          │  (8000)│
    └────────┘           └────────┘          └────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  ML Server(s)   │
                    │  (Auto-scaling) │
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Database (RDS)  │
                    │ Cache (Redis)   │
                    │ Storage (S3)    │
                    └─────────────────┘
```

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0
