from setuptools import find_packages, setup

setup(
    name="egg_price_tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "temporalio>=1.5.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "aiohttp>=3.9.0",
        "beautifulsoup4>=4.12.0",
        "fake-useragent>=1.4.0",
    ],
    python_requires=">=3.8",
)
