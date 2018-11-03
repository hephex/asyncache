from setuptools import find_packages, setup


setup(
    name="asyncache",
    version="0.1.0",
    url="https://github.com/hephex/asyncache",
    license="MIT",
    author="Hephex",
    description="Helpers to use cachetools with async functions",
    long_description=open("README.md").read(),
    keywords="cache caching memoize memoizing memoization async",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["cachetools>=2.1"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
