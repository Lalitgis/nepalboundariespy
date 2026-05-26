"""
nepalboundaries
===============

A Python package for working with administrative boundaries of Nepal.
Provides easy access to country, provincial, district, municipal, and ward boundaries
as GeoDataFrames ready for spatial analysis and visualization.

Example usage
-------------
>>> import nepalboundaries as nb

>>> # All districts
>>> districts = nb.get_district()

>>> # Districts in Bagmati Province
>>> bagmati = nb.get_district(province="Bagmati")

>>> # Wards in Kathmandu municipality
>>> ktm_wards = nb.get_ward(municipality="Kathmandu")

>>> # Quick summary
>>> nb.list_levels()
{'country': 1, 'province': 7, 'district': 77, 'municipality': 753, 'ward': 6743}
"""

from .core import (
    get_country,
    get_province,
    get_district,
    get_municipality,
    get_ward,
    get_multiple,
    info,
    list_levels,
    clear_cache,
    # Convenience aliases
    get_prov,
    get_dist,
    get_mun,
)

__version__ = "0.1.0"
__author__ = "Lalit"
__email__ = "lalitiaas@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/Lalitgis/nepalboundaries"

__all__ = [
    "get_country",
    "get_province",
    "get_district",
    "get_municipality",
    "get_ward",
    "get_multiple",
    "info",
    "list_levels",
    "clear_cache",
    "get_prov",
    "get_dist",
    "get_mun",
]
