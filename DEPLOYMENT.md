# Deployment Guide

## Quick Start

### Local Development
```bash
# Option 1: Automatic
run.bat          # Windows
bash run.sh      # Linux/Mac

# Option 2: Manual
python app.py                # Backend (port 5000)
cd frontend && npm start     # Frontend (port 3000)
```

## Docker Deployment

### Using Docker Compose
```bash
docker-compose up --build
```

**Access**:
- Frontend: http://localhost:3001
- Backend: http://localhost:5000
- Nginx Proxy: http://localhost

### Individual Containers
```bash
# Backend
docker build -f Dockerfile.backend -t anomaly-backend .
docker run -p 5000:5000 anomaly-backend

# Frontend
docker build -f Dockerfile.frontend -t anomaly-frontend ./frontend
docker run -p 3001:80 anomaly-frontend
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, AKS, EKS, GKE)
- kubectl configured

### Deploy
```bash
kubectl apply -f k8s-deployment.yaml
```

### Access
```bash
# Get service URL
kubectl get services
```

### Features
- Auto-scaling (2-5 replicas)
- Resource limits (CPU/Memory)
- Health checks
- Rolling updates

## Environment Configuration

### Required Variables
```bash
# Create .env file
NVIDIA_API_KEY=nvapi-your-key-here
FLASK_ENV=production
```

### Optional Variables
```bash
MAX_FILE_SIZE=52428800      # 50MB
UPLOAD_FOLDER=uploads
```

## Production Considerations

### Security
- Use HTTPS (configure nginx with SSL certificates)
- Secure NVIDIA_API_KEY (use secrets management)
- Enable CORS only for trusted domains
- Implement rate limiting

### Performance
- Use Gunicorn workers (configured in backend)
- Enable nginx caching
- Set appropriate resource limits in K8s

### Monitoring
- Check `/health` endpoint
- Monitor `/api/metrics`
- Set up logging aggregation

## Troubleshooting

### Backend won't start
```bash
pip install -r requirements.txt
python -c "from backend.services.generator import ReportGenerator"
```

### Frontend build fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Docker issues
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

## Scaling

### Horizontal Scaling (K8s)
```yaml
replicas: 5  # Increase in k8s-deployment.yaml
```

### Vertical Scaling
Adjust resource limits:
```yaml
resources:
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

---

For AI setup, see **AI_SETUP_GUIDE.md**
