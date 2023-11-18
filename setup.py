from setuptools import setup, find_packages

setup(
    name="mangas",
    version="0.0.1",
    author="p1atdev",
    description="A python library for downloading mangas",
    package_dir={"": "src"},
    packages=find_packages("src"),
    license="MIT License",
    install_requires=[
        "requests",
        "tqdm",
        "pydantic",
        "feedparser",
        "beautifulsoup4",
        "lxml",
    ],
    entry_points={},
    python_requires=">=3.10.0",
)
