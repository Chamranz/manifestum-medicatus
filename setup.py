"""
Setup script for manifestum-medicatus.
"""
from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="manifestum-medicatus",
    version="0.1.0",
    author="Kamran",
    author_email="kamran@example.com",
    description="A tool for automating configuration manifest merging and generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamran/manifestum-medicatus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.9',
    install_requires=[
        "pydantic>=2.0.0",
        "PyYAML>=6.0",
        "python-dotenv>=1.0.0"
    ],
    extras_require={
        "develop": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "manifestum=manifestum_medicatus.cli:main",
        ],
    },
)