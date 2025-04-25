import re

from setuptools import setup, find_packages

version = re.search(
    r'^CURRENT_VERSION\s*=\s*"(.*)"',
    open('src/godork/services/version.py').read(),
    re.M
).group(1)

setup(
    name='godork',
    version=version,
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
            'godork = godork.godork:main'
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
