#!/usr/bin/env python3

"""ENTROPIA Upload v1.0.0 - Thermodynamic Framework for Digital Systems"""

import requests
import hashlib
import os
import glob

TOKEN = "YOUR_PYPI_TOKEN_HERE"

print("="*60)
print("ENTROPIA v1.0.0 Upload - PyPI")
print("Statistical Dynamics of Information Dissipation")
print("="*60)

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
print(f"README.md: {len(readme)} characters")

wheel_files = glob.glob("dist/*.whl")
tar_files = glob.glob("dist/*.tar.gz")

if not wheel_files and not tar_files:
    print("\nNo distribution files found. Building package...")
    os.system("python -m build")
    wheel_files = glob.glob("dist/*.whl")
    tar_files = glob.glob("dist/*.tar.gz")

print(f"\nFiles:")
for f in wheel_files + tar_files:
    print(f"   • {os.path.basename(f)}")

for filepath in wheel_files + tar_files:
    filename = os.path.basename(filepath)
    print(f"\nUploading: {filename}")

    if filename.endswith('.tar.gz'):
        filetype = 'sdist'
        pyversion = 'source'
    else:
        filetype = 'bdist_wheel'
        pyversion = 'py3'

    with open(filepath, 'rb') as f:
        content = f.read()
    md5_hash = hashlib.md5(content).hexdigest()
    sha256_hash = hashlib.sha256(content).hexdigest()

    data = {
        ':action': 'file_upload',
        'metadata_version': '2.1',
        'name': 'entropia',
        'version': '1.0.0',
        'filetype': filetype,
        'pyversion': pyversion,
        'md5_digest': md5_hash,
        'sha256_digest': sha256_hash,
        'description': readme,
        'description_content_type': 'text/markdown',
        'author': 'Samir Baladi',
        'author_email': 'gitdeeper@gmail.com',
        'license': 'MIT',
        'summary': 'ENTROPIA: Thermodynamic framework for predicting digital system collapse through unified Boltzmann-Shannon entropy',
        'home_page': 'https://entropia-lab.netlify.app',
        'project_urls': 'Documentation,https://entropia-lab.netlify.app/docs;Source,https://github.com/gitdeeper10/entropia;Issues,https://github.com/gitdeeper10/entropia/issues;Research Paper,https://entropia-lab.netlify.app/paper',
        'requires_python': '>=3.11',
        'keywords': 'entropy, thermodynamics, information-theory, phase-transition, system-failure, collapse-prediction, statistical-mechanics, digital-infrastructure, AI-resilience, Boltzmann-entropy, Shannon-entropy'
    }

    with open(filepath, 'rb') as f:
        response = requests.post(
            'https://upload.pypi.org/legacy/',
            files={'content': (filename, f, 'application/octet-stream')},
            data=data,
            auth=('__token__', TOKEN),
            timeout=60,
            headers={'User-Agent': 'ENTROPIA-Uploader/1.0'}
        )

    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        print("   SUCCESS!")
    else:
        print(f"   ERROR: {response.text[:200]}")

print("\n" + "="*60)
print("https://pypi.org/project/entropia/1.0.0/")
print("https://entropia-lab.netlify.app")
print("="*60)
