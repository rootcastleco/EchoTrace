"""Setup script for EchoTrace."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="echotrace",
    version="0.1.0",
    author="EchoTrace Contributors",
    description="System behavior monitoring through sound signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rootcastleco/EchoTrace",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Monitoring",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "echotrace=echotrace.__main__:main",
        ],
    },
)
