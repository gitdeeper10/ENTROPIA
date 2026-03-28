# ENTROPIA Security Policy

## 📋 Supported Versions

| Version | Supported | Security Updates |
|---------|-----------|------------------|
| 1.0.x   | ✅ Yes    | Critical fixes only |
| < 1.0   | ❌ No     | End of life |

## 🔒 Security Model

ENTROPIA is a thermodynamic monitoring framework that processes system telemetry data. The security model is based on:

1. **Read-only Access**: ENTROPIA only reads system metrics, never modifies system state
2. **No Network Egress**: By default, the Ψ-Dashboard binds to localhost
3. **Isolated Computation**: All entropy calculations run in isolated processes

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability in ENTROPIA, please:

### Do NOT:
- Open a public GitHub issue
- Discuss the vulnerability in public channels
- Disclose details before a fix is available

### DO:
1. Email the maintainer: **gitdeeper@gmail.com**
2. Include detailed steps to reproduce
3. If possible, include a proof of concept
4. Allow up to **72 hours** for an initial response

## 🔐 Security Best Practices

### For Production Deployment

```bash
# Always use environment variables for secrets
export ENTROPIA_SECRET_KEY="your-secure-key"
export ENTROPIA_ALLOWED_ORIGINS="https://your-domain.com"

# Run with non-root user
docker run -u 1000:1000 entropia:latest

# Use read-only data mounts
docker run -v /data:/home/entropia/data:ro entropia:latest

# Enable HTTPS in production
entropia dashboard --https --cert /path/to/cert.pem --key /path/to/key.pem
```

Configuration Security

```yaml
# .env.production - Never commit to repository!
ENTROPIA_SECRET_KEY=change-this-to-a-secure-random-string
ENTROPIA_ALLOWED_ORIGINS=https://entropy.your-domain.com
ENTROPIA_LOG_LEVEL=WARNING
```

Network Security

· Bind dashboard to localhost when not behind reverse proxy:
  ```bash
  entropia dashboard --host 127.0.0.1 --port 8080
  ```
· Use firewall rules to restrict access:
  ```bash
  # Allow only localhost
  sudo ufw allow from 127.0.0.1 to any port 8080
  ```

📊 Data Sensitivity

ENTROPIA processes telemetry data that may include:

· CPU utilization
· Memory pressure
· Network I/O rates
· Cache hit ratios

This data may be sensitive in production environments. Always:

· Encrypt data at rest
· Use secure channels for data transmission
· Implement access controls

🔄 Security Updates

Security updates are published through:

· PyPI: pip install --upgrade entropia
· Docker Hub: docker pull gitdeeper10/entropia:latest
· GitHub Releases: github.com/gitdeeper10/entropia/releases

📝 Vulnerability Disclosure Timeline

Phase Duration
Report Received Day 0
Initial Response Within 72 hours
Fix Development 7-14 days
Patch Release Day 14
Public Disclosure Day 21

🌟 Responsible Disclosure Recognition

We thank the following researchers for responsibly disclosing security issues:

This list will be updated as contributions are made.

---

⚠️ Disclaimer

ENTROPIA is a predictive framework and should not be used as the sole decision-making mechanism for critical infrastructure. Always maintain human oversight and redundant safety systems.

---

For non-security issues, please open a GitHub Issue.

"When we learn to read entropy in our machines, we gain sovereignty over the digital world."
