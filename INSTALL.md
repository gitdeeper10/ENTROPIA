# ENTROPIA Installation Guide

## 📋 System Requirements

### Minimum Requirements
- **OS:** Linux, macOS, or Windows (WSL2 recommended)
- **Python:** 3.11 or higher
- **RAM:** 4 GB (8 GB recommended)
- **Storage:** 2 GB free space
- **CPU:** 2 cores (4+ cores recommended for simulations)

### Recommended for Production
- **OS:** Ubuntu 22.04 LTS or Debian 12
- **Python:** 3.11
- **RAM:** 16 GB
- **Storage:** 10 GB SSD
- **CPU:** 8+ cores
- **GPU:** NVIDIA GPU with CUDA 11.8+ (for JAX acceleration)

---

## 🚀 Quick Install

### Using pip

```bash
# Install from PyPI
pip install entropia

# Verify installation
entropia --version
entropia health-check
```

Using Docker

```bash
# Pull from Docker Hub
docker pull gitdeeper10/entropia:latest

# Run container
docker run -p 8080:8080 gitdeeper10/entropia:latest dashboard
```

---

🔧 Detailed Installation

1. Install Python

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

macOS:

```bash
brew install python@3.11
```

Windows:
Download from python.org

2. Create Virtual Environment

```bash
python3.11 -m venv entropia-env
source entropia-env/bin/activate  # On Windows: entropia-env\Scripts\activate
```

3. Install from Source

```bash
# Clone repository
git clone https://github.com/gitdeeper10/entropia.git
cd entropia

# Install in development mode
pip install -e ".[dev]"

# Or install with all optional dependencies
pip install -e ".[all]"
```

4. Verify Installation

```bash
# Run tests
pytest tests/

# Run example
python examples/basic_prediction.py

# Launch dashboard
entropia dashboard
```

---

🐳 Docker Installation

Build Image

```bash
git clone https://github.com/gitdeeper10/entropia.git
cd entropia
docker build -t entropia:latest .
```

Run Container

```bash
# Basic run
docker run -p 8080:8080 entropia:latest

# With volume for data persistence
docker run -p 8080:8080 -v $(pwd)/data:/home/entropia/data entropia:latest

# With environment variables
docker run -p 8080:8080 \
  -e ENTROPIA_ENV=production \
  -e ENTROPIA_CRITICAL_PSI=2.0 \
  entropia:latest
```

Docker Compose

Create docker-compose.yml:

```yaml
version: '3.8'

services:
  entropia:
    image: gitdeeper10/entropia:latest
    ports:
      - "8080:8080"
    volumes:
      - ./data:/home/entropia/data
    environment:
      - ENTROPIA_ENV=production
      - ENTROPIA_LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "entropia", "health-check"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run:

```bash
docker-compose up -d
```

---

📦 Platform-Specific Notes

Linux (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt install build-essential libopenblas-dev libffi-dev

# Install ENTROPIA
pip install entropia
```

macOS

```bash
# Install via Homebrew
brew install openblas

# Install ENTROPIA
pip install entropia
```

Windows (WSL2)

```bash
# Install WSL2 first, then Ubuntu
wsl --install

# Inside WSL, follow Linux instructions
```

---

🔍 Verification

Check Installation

```python
import entropia
print(entropia.__version__)
print(entropia.__author__)

# Test core functions
from entropia.core import boltzmann_entropy, shannon_entropy
import numpy as np

microstates = 1e6
S_B = boltzmann_entropy(microstates)
print(f"Boltzmann Entropy: {S_B:.2e} J/K")

probabilities = np.array([0.5, 0.3, 0.2])
H = shannon_entropy(probabilities)
print(f"Shannon Entropy: {H:.2f} bits")
```

Run Benchmark

```bash
entropia benchmark --env E-ENV-03 --nodes 100000
```

---

🐛 Troubleshooting

Common Issues

Issue: ModuleNotFoundError: No module named 'entropia'

Solution: Ensure virtual environment is activated:

```bash
source entropia-env/bin/activate
pip install entropia
```

Issue: ImportError: libopenblas.so.0: cannot open shared object file

Solution: Install OpenBLAS:

```bash
# Ubuntu/Debian
sudo apt install libopenblas0

# macOS
brew install openblas
```

Issue: Dashboard fails to start

Solution: Check port availability:

```bash
# Change port
entropia dashboard --port 8081

# Check if port is in use
lsof -i :8080
```

---

✅ Next Steps

· Read the Research Paper
· Explore Examples
· Run Tutorials
· Join Discussions

---

"When we learn to read entropy in our machines, we gain sovereignty over the digital world."
