from setuptools import setup

with open('README.md', 'r') as desc_file:
    long_description = desc_file.read()

setup(
    name='mieaa',
    description='miEAA command line interface and api wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.5',
    author='Chair for Clinical Bioinformatics at Saarland University',
    author_email='ccb.unisb@gmail.com',
    url='https://github.com/Xethic/miEAA-API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    packages=['mieaa'],
    install_requires=['requests>=2.19.*'],
    python_requires='>=3.5.*, <4',
    keywords='mirna bioinformatics',
    entry_points={
        'console_scripts': [
            'mieaa = mieaa.mieaa_cli:main'
        ],
    },
)
