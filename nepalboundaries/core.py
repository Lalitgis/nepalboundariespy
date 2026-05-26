"""
core.py
-------

Core functions for the nepalboundaries package.

All functions return ``geopandas.GeoDataFrame`` objects in WGS84 (EPSG:4326).
Data is loaded lazily and cached in memory after the first access.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Union

import geopandas as gpd
import pandas as pd

# ---------------------------------------------------------------------------
# Package-level constants
# ---------------------------------------------------------------------------

PACKAGE_DIR: Path = Path(__file__).parent
DATA_DIR: Path = PACKAGE_DIR / "data"

VALID_LEVELS: List[str] = ["country", "province", "district", "municipality", "ward"]

# In-memory cache keyed by level name
_cache: Dict[str, gpd.GeoDataFrame] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_data_path(level: str) -> Path:
    """Return the GeoJSON path for *level*, raising a clear error if missing."""
    path = DATA_DIR / f"{level}.geojson"
    if not path.exists():
        raise FileNotFoundError(
            f"Data file '{path.name}' not found in {DATA_DIR}.\n"
            "Run scripts/data_preparation_python.py to generate the data files, "
            "or download them from the project releases page:\n"
            "  https://github.com/Lalitgis/nepalboundaries/releases"
        )
    return path


def _load_data(level: str) -> gpd.GeoDataFrame:
    """Load *level* data from disk (with in-memory caching)."""
    if level in _cache:
        return _cache[level].copy()

    path = _get_data_path(level)
    gdf = gpd.read_file(path)

    # Normalise to WGS84
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    elif gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs("EPSG:4326")

    _cache[level] = gdf
    return gdf.copy()


def _to_list(value: Optional[Union[str, int, List]]) -> Optional[List]:
    """Coerce a scalar or list to a list, or return None unchanged."""
    if value is None:
        return None
    return [value] if isinstance(value, (str, int)) else list(value)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_country() -> gpd.GeoDataFrame:
    """
    Return Nepal's national boundary.

    Returns
    -------
    geopandas.GeoDataFrame
        Single-row GeoDataFrame with the country outline.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> nepal = nb.get_country()
    >>> nepal.plot()
    """
    return _load_data("country")


def get_province(
    province: Optional[Union[str, List[str]]] = None,
) -> gpd.GeoDataFrame:
    """
    Return Nepal's provincial boundaries.

    Parameters
    ----------
    province : str or list of str, optional
        One or more province names to filter.  When *None* (default) all
        seven provinces are returned.

    Returns
    -------
    geopandas.GeoDataFrame
        Provincial boundaries sorted by ``province_name``.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> all_provinces = nb.get_province()
    >>> bagmati = nb.get_province("Bagmati")
    >>> two = nb.get_province(["Bagmati", "Gandaki"])
    """
    data = _load_data("province")

    names = _to_list(province)
    if names is not None:
        data = data[data["province_name"].isin(names)]
        if data.empty:
            warnings.warn(f"No provinces matched: {names}", stacklevel=2)

    return data.sort_values("province_name").reset_index(drop=True)


def get_district(
    district: Optional[Union[str, List[str]]] = None,
    province: Optional[Union[str, List[str]]] = None,
) -> gpd.GeoDataFrame:
    """
    Return Nepal's district boundaries.

    Parameters
    ----------
    district : str or list of str, optional
        District name(s) to filter.
    province : str or list of str, optional
        Restrict results to districts within these province(s).

    Returns
    -------
    geopandas.GeoDataFrame
        District boundaries sorted by ``district_name``.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> all_districts = nb.get_district()
    >>> bhaktapur = nb.get_district("Bhaktapur")
    >>> bagmati_districts = nb.get_district(province="Bagmati")
    """
    data = _load_data("district")

    prov_names = _to_list(province)
    if prov_names is not None:
        data = data[data["province_name"].isin(prov_names)]

    dist_names = _to_list(district)
    if dist_names is not None:
        data = data[data["district_name"].isin(dist_names)]
        if data.empty:
            warnings.warn("No districts matched the given criteria.", stacklevel=2)

    return data.sort_values("district_name").reset_index(drop=True)


def get_municipality(
    municipality: Optional[Union[str, List[str]]] = None,
    district: Optional[Union[str, List[str]]] = None,
    province: Optional[Union[str, List[str]]] = None,
) -> gpd.GeoDataFrame:
    """
    Return Nepal's municipality boundaries.

    Parameters
    ----------
    municipality : str or list of str, optional
        Municipality name(s) to filter.
    district : str or list of str, optional
        Restrict results to municipalities within these district(s).
    province : str or list of str, optional
        Restrict results to municipalities within these province(s).

    Returns
    -------
    geopandas.GeoDataFrame
        Municipality boundaries sorted by ``municipality_name``.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> all_mun = nb.get_municipality()
    >>> kathmandu = nb.get_municipality("Kathmandu")
    >>> bhakt_mun = nb.get_municipality(district="Bhaktapur")
    """
    data = _load_data("municipality")

    prov_names = _to_list(province)
    if prov_names is not None:
        data = data[data["province_name"].isin(prov_names)]

    dist_names = _to_list(district)
    if dist_names is not None:
        data = data[data["district_name"].isin(dist_names)]

    mun_names = _to_list(municipality)
    if mun_names is not None:
        data = data[data["municipality_name"].isin(mun_names)]
        if data.empty:
            warnings.warn("No municipalities matched the given criteria.", stacklevel=2)

    return data.sort_values("municipality_name").reset_index(drop=True)


def get_ward(
    ward: Optional[Union[str, int, List[Union[str, int]]]] = None,
    municipality: Optional[Union[str, List[str]]] = None,
    district: Optional[Union[str, List[str]]] = None,
    province: Optional[Union[str, List[str]]] = None,
) -> gpd.GeoDataFrame:
    """
    Return Nepal's ward boundaries.

    Parameters
    ----------
    ward : int, str, or list, optional
        Ward number(s) to filter.
    municipality : str or list of str, optional
        Restrict results to wards within these municipality(ies).
    district : str or list of str, optional
        Restrict results to wards within these district(s).
    province : str or list of str, optional
        Restrict results to wards within these province(s).

    Returns
    -------
    geopandas.GeoDataFrame
        Ward boundaries sorted by ``municipality_name`` then ``ward_number``.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> ktm_wards = nb.get_ward(municipality="Kathmandu")
    >>> ward_1 = nb.get_ward(ward=1, municipality="Kathmandu")
    """
    data = _load_data("ward")

    prov_names = _to_list(province)
    if prov_names is not None:
        data = data[data["province_name"].isin(prov_names)]

    dist_names = _to_list(district)
    if dist_names is not None:
        data = data[data["district_name"].isin(dist_names)]

    mun_names = _to_list(municipality)
    if mun_names is not None:
        data = data[data["municipality_name"].isin(mun_names)]

    if ward is not None:
        ward_vals = _to_list(ward)
        # Normalise to strings for comparison
        ward_strs = [str(w) for w in ward_vals]
        data = data[data["ward_number"].astype(str).isin(ward_strs)]
        if data.empty:
            warnings.warn("No wards matched the given criteria.", stacklevel=2)

    return data.sort_values(["municipality_name", "ward_number"]).reset_index(drop=True)


def get_multiple(
    levels: List[str] = None,
) -> Dict[str, gpd.GeoDataFrame]:
    """
    Return boundaries for multiple administrative levels in one call.

    Parameters
    ----------
    levels : list of str, optional
        Any subset of ``['country', 'province', 'district', 'municipality', 'ward']``.
        Defaults to ``['province', 'district']``.

    Returns
    -------
    dict
        Mapping of level name → GeoDataFrame.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> data = nb.get_multiple(["province", "district", "municipality"])
    >>> data["district"].plot()
    """
    if levels is None:
        levels = ["province", "district"]

    invalid = set(levels) - set(VALID_LEVELS)
    if invalid:
        raise ValueError(
            f"Invalid level(s): {invalid}.  "
            f"Choose from: {VALID_LEVELS}"
        )

    _fn_map = {
        "country": get_country,
        "province": get_province,
        "district": get_district,
        "municipality": get_municipality,
        "ward": get_ward,
    }
    return {level: _fn_map[level]() for level in levels}


def info(level: str = "district") -> pd.DataFrame:
    """
    Return a one-row summary for the given administrative level.

    Parameters
    ----------
    level : str
        One of ``'province'``, ``'district'``, ``'municipality'``, ``'ward'``.

    Returns
    -------
    pandas.DataFrame
        Summary with columns: level, features, columns, crs.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> nb.info("district")
    >>> nb.info("municipality")
    """
    valid = [v for v in VALID_LEVELS if v != "country"]
    if level not in valid:
        raise ValueError(f"Invalid level '{level}'.  Choose from: {valid}")

    gdf = _load_data(level)
    return pd.DataFrame(
        {
            "level": [level],
            "features": [len(gdf)],
            "columns": [", ".join(gdf.columns.tolist())],
            "crs": [str(gdf.crs)],
        }
    )


def list_levels() -> Dict[str, Union[int, str]]:
    """
    Report available administrative levels and their feature counts.

    Returns
    -------
    dict
        ``{level_name: feature_count}`` where the count is the string
        ``'Not available'`` if the data file is missing.

    Examples
    --------
    >>> import nepalboundaries as nb
    >>> nb.list_levels()
    {'country': 1, 'province': 7, 'district': 77, 'municipality': 753, 'ward': 6743}
    """
    result: Dict[str, Union[int, str]] = {}
    for level in VALID_LEVELS:
        try:
            result[level] = len(_load_data(level))
        except FileNotFoundError:
            result[level] = "Not available"
    return result


def clear_cache() -> None:
    """Clear the in-memory data cache to free RAM."""
    global _cache
    _cache.clear()


# ---------------------------------------------------------------------------
# Convenience aliases
# ---------------------------------------------------------------------------

get_prov = get_province
get_dist = get_district
get_mun = get_municipality
