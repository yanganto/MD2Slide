from setuptools import find_packages, setup

setup(
    name="md2slide",
    packages=find_packages(),
    version="0.0.3",
    description="A web server serve markdown file to html slide",
    author="yanganto",
    author_email="yanganto@gmail.com",
    url="https://github.com/yanganto/MD2Slide",
    download_url="",
    keywords=["markdown", "slide"],
    license='MIT',
    include_package_data=True,
    package_data={
        'md2slide': ['*.js', '*.css', '*.md'],
    },
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
