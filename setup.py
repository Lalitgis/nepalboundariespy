"""
setup.py for nepalboundariespy
"""

from pathlib import Path
from setuptools import find_packages, setup

HERE = Path(__file__).parent
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="nepalboundariespy",
    version="0.1.1",
    author="Lalit",
    author_email="lalitiaas@gmail.com",
    description="Administrative boundaries of Nepal at country, province, district, municipality, and ward level",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lalitgis/nepalboundariespy",
    project_urls={
        "Bug Tracker": "https://github.com/Lalitgis/nepalboundariespy/issues",
        "Source Code": "https://github.com/Lalitgis/nepalboundariespy",
    },
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.8",
    install_requires=[
        "geopandas>=0.10.0",
        "shapely>=1.8.0",
        "pandas>=1.0.0",
    ],
    extras_require={
        "viz": [
            "matplotlib>=3.3.0",
            "folium>=0.12.0",
        ],
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "isort",
        ],
    },
    include_package_data=True,
    package_data={
        "nepalboundaries": [
            "data/*.geojson",
            "data/*.json",
        ],
    },
    zip_safe=False,
)
