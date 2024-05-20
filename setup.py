from setuptools import setup, find_packages
from src.godork import __version__

setup(
    name='godork',
    version=__version__,
    author='Thunder (@thd3r)',
    author_email='thd3r@proton.me',
    description='Scrape Google search quickly',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'asyncio',
        'requests',
        'bs4',
    ],
    entry_points={
        'console_scripts': [
            'godork = src.godork:main'
        ]
    },
    license='MIT',
    url='https://github.com/thd3r/godork',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['godork', 'google dorks', 'google dork', 'google dorking']
)