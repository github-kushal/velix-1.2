from setuptools import setup, find_packages

setup(
    name="velix",
    version="1.2",
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open('requirements.txt').readlines() 
        if line.strip() and not line.startswith('#')
    ],
    python_requires='>=3.8',
)
