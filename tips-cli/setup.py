from setuptools import setup, find_packages

# Get version from the package __init__.py
version = {}
with open("tips/__init__.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tips-cli-tool",
    version=version["__version__"],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple CLI tool for creating temporary notes that are automatically deleted after editing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tips-cli-tool", # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYAML",
    ],
    entry_points={
        'console_scripts': [
            'tips=tips.main:main',
        ],
    },
)