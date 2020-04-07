from setuptools import setup

with open('README.rst', 'r') as desc_file:
    long_description = desc_file.read()

with open('./mieaa/_version.py') as version_file:
    exec(version_file.read().strip())

setup(
    name='mieaa',
    version=__version__,
    description='miEAA Command Line Interface and API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='MIT',
    author='Jeffrey Solomon',
    maintainer='Chair for Clinical Bioinformatics at Saarland University',
    maintainer_email='ccb.unisb@gmail.com',
    url='https://www.ccb.uni-saarland.de/mieaa2',
    download_url='https://pypi.org/project/mieaa/#files',
    project_urls={
        "Bug Tracker": 'https://github.com/Xethic/miEAA-API/issues',
        "Documentation": 'https://mieaa.readthedocs.io/en/latest/',
        "Source Code": 'https://github.com/Xethic/miEAA-API',
    },
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
