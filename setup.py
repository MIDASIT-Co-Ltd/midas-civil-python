from setuptools import setup,find_packages

with open('README.md','r') as f:
    description = f.read()


setup(name='midas_civil',
    version='0.1.3',
    description='Python library for MIDAS Civil NX',
    author='Sumit Shekhar',
    author_email='sumit.midasit@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'polars',
        'xlsxwriter',
        'requests'
    ],          
    long_description= description,
    long_description_content_type='text/markdown'
    )