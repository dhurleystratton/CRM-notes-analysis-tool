from setuptools import setup, find_packages

setup(
    name='crm-notes-analysis-tool',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.24.0',
        'python-dateutil>=2.8.0',
        'tqdm>=4.65.0',
        'click>=8.1.0',
    ],
)
