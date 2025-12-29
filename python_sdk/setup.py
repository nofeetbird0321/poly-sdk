"""Setup script for polymarket-sdk package."""

from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    package_data={
        "polymarket_sdk": ["py.typed"],
    },
)
