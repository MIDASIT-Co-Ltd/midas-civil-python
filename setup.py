from setuptools import setup,find_packages

with open('README.md','r') as f:
    description = f.read()


setup(name='midas_civil',
    version='1.1.7',
    description='Python library for MIDAS Civil NX',
    author='Sumit Shekhar',
    author_email='sumit.midasit@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'polars',
        'xlsxwriter',
        'requests',
        'scipy',
        'colorama',
        'openpyxl'
    ],          
    long_description= description,
    long_description_content_type='text/markdown',
    url='https://github.com/MIDASIT-Co-Ltd/midas-civil-python',
    keywords=['midas','civil','civil nx','bridge'],
    license='MIT',
    )