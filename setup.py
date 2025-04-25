from setuptools import setup, find_packages
from src.godork.services.version import CURRENT_VERSION

setup(
    name='godork',
    version=CURRENT_VERSION,
    author='Thunder (@thd3r)',
    author_email='thd3r@proton.me',
    description='Advanced & Fast Google Dorking Tool',
    packages=find_packages(where='src'),
    package_dir={'godork': 'src/godork'},
    install_requires=[
        'bs4',
        'rich',
        'pydub',
        'psutil',
        'aiohttp',
        'asyncio',
        'selenium',
        'setuptools',
        'SpeechRecognition',
        'webdriver-manager',
        'undetected-chromedriver',
    ],
    entry_points={
        'console_scripts': [
            'godork = godorks.godork:main'
        ]
    },
    license='MIT',
    url='https://github.com/thd3r/godork',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['godork', 'google dorks', 'google dorking'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    )
)
