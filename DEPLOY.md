
# ENTROPIA Deployment Guide

## 📋 Deployment Overview

This guide covers deployment options for ENTROPIA in various environments:

- **Development**: Local testing and development
- **Production**: Scalable production deployment
- **Containerized**: Docker and Kubernetes
- **Cloud**: AWS, GCP, Azure

---

## 🚀 Quick Deployment

### Development Mode

```bash
# Clone repository
git clone https://github.com/gitdeeper10/entropia.git
cd entropia

# Install with development dependencies
pip install -e ".[dev]"

# Run dashboard locally
entropia dashboard --host 127.0.0.1 --port 8080
```

Production Mode (Simple)

```bash
# Install production version
pip install entropia

# Run with production settings
export ENTROPIA_ENV=production
export ENTROPIA_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
entropia dashboard --host 0.0.0.0 --port 8080 --workers 4
```

---

🐳 Docker Deployment

Basic Docker Run

```bash
# Pull image
docker pull gitdeeper10/entropia:latest

# Run container
docker run -d \
  --name entropia \
  -p 8080:8080 \
  -e ENTROPIA_ENV=production \
  -e ENTROPIA_SECRET_KEY=your-secret-key \
  -v entropia_data:/home/entropia/data \
  gitdeeper10/entropia:latest
```

Docker Compose

Create docker-compose.yml:

```yaml
version: '3.8'

services:
  entropia:
    image: gitdeeper10/entropia:latest
    container_name: entropia
    ports:
      - "8080:8080"
    environment:
      - ENTROPIA_ENV=production
      - ENTROPIA_SECRET_KEY=${ENTROPIA_SECRET_KEY}
      - ENTROPIA_LOG_LEVEL=INFO
      - ENTROPIA_METRICS_ENABLED=true
    volumes:
      - entropia_data:/home/entropia/data
      - entropia_logs:/home/entropia/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "entropia", "health-check"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: entropia-redis
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: entropia-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - entropia
    restart: unless-stopped

volumes:
  entropia_data:
  entropia_logs:
  redis_data:
```

Run:

```bash
docker-compose up -d
```

---

☁️ Cloud Deployment

AWS EC2 Deployment

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install -y python3.11 python3.11-pip git

# Clone and install
git clone https://github.com/gitdeeper10/entropia.git
cd entropia
pip3.11 install -r requirements.txt
pip3.11 install -e .

# Set up systemd service
sudo cat > /etc/systemd/system/entropia.service << 'EOF'
[Unit]
Description=ENTROPIA Dashboard
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/entropia
Environment="ENTROPIA_ENV=production"
Environment="ENTROPIA_SECRET_KEY=your-secret-key"
ExecStart=/usr/local/bin/entropia dashboard --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable entropia
sudo systemctl start entropia
```

AWS ECS (Fargate)

Create task-definition.json:

```json
{
  "family": "entropia",
  "networkMode": "awsvpc",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "entropia",
      "image": "gitdeeper10/entropia:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "ENTROPIA_ENV", "value": "production"},
        {"name": "ENTROPIA_LOG_LEVEL", "value": "INFO"}
      ],
      "secrets": [
        {"name": "ENTROPIA_SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:region:account:secret:entropia-secret"}
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "entropia health-check || exit 1"],
        "interval": 30,
        "timeout": 10,
        "retries": 3
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024"
}
```

---

🔧 Kubernetes Deployment

Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: entropia
  namespace: monitoring
spec:
  replicas: 3
  selector:
    matchLabels:
      app: entropia
  template:
    metadata:
      labels:
        app: entropia
    spec:
      containers:
      - name: entropia
        image: gitdeeper10/entropia:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENTROPIA_ENV
          value: "production"
        - name: ENTROPIA_LOG_LEVEL
          value: "INFO"
        envFrom:
        - secretRef:
            name: entropia-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: entropia
  namespace: monitoring
spec:
  selector:
    app: entropia
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: entropia
  namespace: monitoring
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - entropy.your-domain.com
    secretName: entropia-tls
  rules:
  - host: entropy.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: entropia
            port:
              number: 80
```

Deploy:

```bash
kubectl apply -f entropia-deployment.yaml
```

---

📊 Monitoring & Observability

Prometheus Metrics

ENTROPIA exposes metrics at /metrics endpoint:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'entropia'
    static_configs:
      - targets: ['entropia:8080']
    metrics_path: /metrics
```

Grafana Dashboard

Import dashboard ID: entropia-001 or use provided grafana-dashboard.json

---

🔒 Security Hardening

Production Checklist

· Set ENTROPIA_ENV=production
· Generate secure ENTROPIA_SECRET_KEY
· Enable HTTPS with valid SSL certificate
· Restrict allowed origins
· Use read-only data volumes
· Run as non-root user
· Enable rate limiting
· Configure firewall rules
· Set up audit logging
· Regular security updates

SSL Configuration (Nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name entropy.your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://entropia:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

🧪 Testing Deployment

```bash
# Health check
curl http://localhost:8080/health

# Get metrics
curl http://localhost:8080/metrics

# Verify Ψ-Dashboard
curl http://localhost:8080/dashboard
```

---

🔄 Updates & Rollbacks

Rolling Update (Kubernetes)

```bash
kubectl set image deployment/entropia entropia=gitdeeper10/entropia:1.1.0
kubectl rollout status deployment/entropia
kubectl rollout undo deployment/entropia  # Rollback if needed
```

Blue-Green Deployment (Docker)

```bash
# Blue (current)
docker run -d --name entropia-blue -p 8080:8080 entropia:1.0.0

# Green (new)
docker run -d --name entropia-green -p 8081:8080 entropia:1.1.0

# Test green
curl http://localhost:8081/health

# Switch
docker stop entropia-blue
docker run -d --name entropia-blue -p 8080:8080 entropia:1.1.0
```

---

📈 Scaling Considerations

Horizontal Scaling

· Stateless dashboard can scale horizontally
· Use Redis for session storage
· Load balancer for distribution

Vertical Scaling

· Increase CPU for complex simulations
· Add memory for large node counts
· GPU for JAX acceleration

---

🆘 Troubleshooting

Common Issues

Issue Solution
Port already in use Change port: --port 8081
Permission denied Run with --user or adjust permissions
Out of memory Reduce simulation size or increase RAM
Dashboard not loading Check firewall and network settings

Logs

```bash
# Docker logs
docker logs entropia

# Kubernetes logs
kubectl logs -f deployment/entropia

# Systemd logs
journalctl -u entropia -f
```

---

📚 Additional Resources

· ENTROPIA Documentation
· GitHub Repository
· Docker Hub
· Research Paper

---

For deployment support, contact: gitdeeper@gmail.com

"When we learn to read entropy in our machines, we gain sovereignty over the digital world."
