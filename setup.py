from setuptools import setup
import os

# Read README
readme = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

setup(
    name="entropia",
    version="1.0.0",
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="ENTROPIA: Thermodynamic framework for predicting digital system collapse",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://entropia-lab.netlify.app",
    license="MIT",
    packages=["entropia"],
    package_dir={"entropia": "entropia"},
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "entropia=entropia.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
