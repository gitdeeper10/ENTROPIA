# Contributing to ENTROPIA

Thank you for your interest in contributing to ENTROPIA! This framework represents a fundamental shift in how we understand digital system failures through the lens of thermodynamic information theory.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Research Contributions](#research-contributions)
- [Contact](#contact)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/entropia.git
cd entropia
```

Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
pre-commit install
```

Development Environment

Project Structure

```
entropia/
├── src/entropia/           # Main package
│   ├── core/               # Core thermodynamic equations
│   │   ├── entropy.py      # S_total, Boltzmann, Shannon
│   │   ├── parameters.py   # ρ, ρᴄ, Ψ, σ, τ_collapse
│   │   └── dynamics.py     # dS/dt, entropy production
│   ├── simulation/         # Monte Carlo engines
│   │   ├── env01.py        # Static closed-form network
│   │   ├── env02.py        # Dynamic streaming network
│   │   └── env03.py        # Adversarial stress test
│   ├── dashboard/          # Ψ-Dashboard
│   │   ├── app.py          # Flask/Dash application
│   │   └── metrics.py      # Real-time parameter computation
│   └── cli/                # Command-line interface
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
├── notebooks/              # Jupyter notebooks for analysis
└── examples/               # Usage examples
```

How to Contribute

Types of Contributions

1. Code Contributions
   · New features
   · Bug fixes
   · Performance improvements
   · Additional simulation environments
2. Research Contributions
   · Validation studies
   · New theoretical extensions
   · Case study analyses
   · Cross-domain applications
3. Documentation
   · API documentation
   · Tutorials
   · Examples
   · Translations
4. Testing
   · Unit tests
   · Integration tests
   · Benchmarking

Issue Tracking

· Check existing issues before creating new ones
· Use issue templates when available
· Provide detailed reproduction steps for bugs
· Include relevant ENTROPIA parameters when reporting issues

Pull Request Process

1. Create a Branch
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```
2. Make Changes
   · Write clean, documented code
   · Add tests for new functionality
   · Update documentation
3. Run Tests
   ```bash
   # Run all tests
   pytest tests/
   
   # Run specific test suite
   pytest tests/test_parameters.py
   
   # Run with coverage
   pytest --cov=entropia tests/
   ```
4. Format Code
   ```bash
   # Format with black
   black src/ tests/
   
   # Sort imports
   isort src/ tests/
   
   # Lint with flake8
   flake8 src/ tests/
   ```
5. Commit and Push
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```
6. Create Pull Request
   · Use PR template
   · Link related issues
   · Request review from maintainers

Coding Standards

Python Style

· Follow PEP 8
· Use Black for formatting
· Use isort for import sorting
· Type hints are required for all public functions

Docstrings

Use Google-style docstrings:

```python
def dissipation_coefficient(rho: float, rho_c: float, S_total: float, S_max: float) -> float:
    """
    Calculate the Dissipation Coefficient Ψ(ρ).
    
    Args:
        rho: Current data density (bits·s⁻¹·m⁻³)
        rho_c: Critical throughput threshold (bits·s⁻¹·m⁻³)
        S_total: Current total entropy (J/K)
        S_max: Maximum theoretical entropy (J/K)
    
    Returns:
        Ψ: Dissipation coefficient (dimensionless)
    
    Raises:
        ValueError: If ρ >= ρ_c (system in super-critical regime)
    
    Example:
        >>> psi = dissipation_coefficient(0.8e9, 1.0e9, 100, 150)
        >>> print(f"Ψ = {psi:.2f}")
        Ψ = 1.33
    """
    if rho >= rho_c:
        raise ValueError(f"System super-critical: ρ={rho} >= ρ_c={rho_c}")
    
    return (S_total / S_max) * (1 - (rho_c / rho)**2)**(-1)
```

Testing

Unit Tests

· Place tests in tests/ directory
· Use pytest framework
· Aim for >80% coverage

Simulation Tests

· Validate against theoretical predictions
· Reproduce manuscript figures
· Benchmark performance

Documentation

Building Documentation

```bash
cd docs
make html
```

API Documentation

· Document all public functions and classes
· Include mathematical equations in LaTeX
· Reference ENTROPIA parameters

Research Contributions

If you're contributing research:

1. Reproducibility: Include all code and data for reproducing results
2. Documentation: Document methodology and parameter choices
3. Validation: Validate against known cases (e.g., Meta 2021 outage)
4. Citation: Properly cite ENTROPIA framework

Contact

· Lead Author: Samir Baladi - gitdeeper@gmail.com
· GitHub Issues: github.com/gitdeeper10/entropia/issues
· Discussions: github.com/gitdeeper10/entropia/discussions

---

Thank you for contributing to ENTROPIA! Together, we're building the thermodynamic foundation for the digital age.

"When we learn to read entropy in our machines, we gain sovereignty over the digital world."
