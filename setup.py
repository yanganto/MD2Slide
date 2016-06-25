from setuptools import find_packages, setup

setup(
    name="md2slide",
    packages=find_packages(),
    version="0.0.1",
    description="",
    author="yanganto",
    author_email="yanganto@gmail.com",
    url="https://github.com/yanganto/MD2Slide",
    download_url="",
    keywords=["markdown", "slide"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers"
    ],
    entry_points={'console_scripts': [
        'md2slide = md2slide.__main__:main',
    ]},
    long_description="""\
Markdown to Slide package
-------------------------------------

Translate markdown file to web slide

This version requires Python 3.
"""
)
