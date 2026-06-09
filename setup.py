from setuptools import setup, find_packages

setup(
    name='pvacrank',
    version='0.1.0',
    description='Composite immunogenicity ranker for pVACtools',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.20.0',
        'scikit-learn>=1.0',
        'matplotlib>=3.5.0',
        'streamlit>=1.28.0',
    ],
    entry_points={
        'console_scripts': [
            'pvacseq-rank=pvacrank.cli:main',
            'pvacseq-benchmark=pvacrank.benchmark_all:main',
        ],
    },
    python_requires='>=3.8',
)
