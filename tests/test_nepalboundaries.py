"""
Unit tests for nepalboundaries.

Run with:
    pytest tests/ -v
or with coverage:
    pytest tests/ -v --cov=nepalboundaries --cov-report=term-missing
"""

import warnings
import pytest
import geopandas as gpd
import pandas as pd

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _has_data():
    """Return True if at least the 'district' GeoJSON file is present."""
    from pathlib import Path
    from nepalboundaries.core import DATA_DIR
    return (DATA_DIR / "district.geojson").exists()


skip_if_no_data = pytest.mark.skipif(
    not _has_data(),
    reason="GeoJSON data files not present — run scripts/data_preparation_python.py first",
)


# ---------------------------------------------------------------------------
# Import tests (always run, no data needed)
# ---------------------------------------------------------------------------

class TestImports:
    def test_package_imports(self):
        import nepalboundaries as nb
        assert nb.__version__ == "0.1.0"

    def test_public_functions_exposed(self):
        import nepalboundaries as nb
        for fn in [
            "get_country", "get_province", "get_district",
            "get_municipality", "get_ward", "get_multiple",
            "info", "list_levels", "clear_cache",
        ]:
            assert hasattr(nb, fn), f"Missing public function: {fn}"

    def test_aliases_exposed(self):
        import nepalboundaries as nb
        assert nb.get_prov is nb.get_province
        assert nb.get_dist is nb.get_district
        assert nb.get_mun is nb.get_municipality


# ---------------------------------------------------------------------------
# Data tests (skipped when GeoJSON files are missing)
# ---------------------------------------------------------------------------

@skip_if_no_data
class TestGetCountry:
    def test_returns_geodataframe(self):
        import nepalboundaries as nb
        result = nb.get_country()
        assert isinstance(result, gpd.GeoDataFrame)

    def test_single_row(self):
        import nepalboundaries as nb
        assert len(nb.get_country()) == 1

    def test_crs_is_wgs84(self):
        import nepalboundaries as nb
        assert nb.get_country().crs.to_epsg() == 4326


@skip_if_no_data
class TestGetProvince:
    def test_returns_all(self):
        import nepalboundaries as nb
        provinces = nb.get_province()
        assert isinstance(provinces, gpd.GeoDataFrame)
        assert len(provinces) == 7

    def test_filter_single_string(self):
        import nepalboundaries as nb
        result = nb.get_province("Bagmati")
        assert len(result) == 1
        assert result["province_name"].values[0] == "Bagmati"

    def test_filter_list(self):
        import nepalboundaries as nb
        result = nb.get_province(["Bagmati", "Gandaki"])
        assert len(result) == 2

    def test_warns_on_no_match(self):
        import nepalboundaries as nb
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = nb.get_province("NonExistentProvince")
            assert len(w) == 1
        assert result.empty

    def test_sorted_by_name(self):
        import nepalboundaries as nb
        names = nb.get_province()["province_name"].tolist()
        assert names == sorted(names)


@skip_if_no_data
class TestGetDistrict:
    def test_returns_all(self):
        import nepalboundaries as nb
        districts = nb.get_district()
        assert isinstance(districts, gpd.GeoDataFrame)
        assert len(districts) >= 77

    def test_filter_by_name(self):
        import nepalboundaries as nb
        result = nb.get_district("Bhaktapur")
        assert len(result) == 1
        assert result["district_name"].values[0] == "Bhaktapur"

    def test_filter_by_province(self):
        import nepalboundaries as nb
        result = nb.get_district(province="Bagmati")
        assert len(result) > 0
        assert all(result["province_name"] == "Bagmati")

    def test_combined_filter(self):
        import nepalboundaries as nb
        result = nb.get_district(district="Kathmandu", province="Bagmati")
        assert len(result) == 1


@skip_if_no_data
class TestGetMunicipality:
    def test_returns_all(self):
        import nepalboundaries as nb
        result = nb.get_municipality()
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) >= 700

    def test_filter_by_name(self):
        import nepalboundaries as nb
        result = nb.get_municipality("Kathmandu")
        assert len(result) == 1

    def test_filter_by_district(self):
        import nepalboundaries as nb
        result = nb.get_municipality(district="Bhaktapur")
        assert len(result) > 0
        assert all(result["district_name"] == "Bhaktapur")


@skip_if_no_data
class TestGetWard:
    def test_filter_by_municipality(self):
        import nepalboundaries as nb
        result = nb.get_ward(municipality="Kathmandu")
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) > 0

    def test_filter_by_ward_number(self):
        import nepalboundaries as nb
        result = nb.get_ward(ward=1, municipality="Kathmandu")
        assert len(result) >= 1

    def test_sorted_by_municipality_then_ward(self):
        import nepalboundaries as nb
        result = nb.get_ward(municipality="Kathmandu")
        ward_nums = result["ward_number"].astype(int).tolist()
        assert ward_nums == sorted(ward_nums)


@skip_if_no_data
class TestGetMultiple:
    def test_returns_dict(self):
        import nepalboundaries as nb
        result = nb.get_multiple(["province", "district"])
        assert isinstance(result, dict)
        assert set(result.keys()) == {"province", "district"}

    def test_invalid_level_raises(self):
        import nepalboundaries as nb
        with pytest.raises(ValueError, match="Invalid level"):
            nb.get_multiple(["province", "galaxy"])

    def test_default_levels(self):
        import nepalboundaries as nb
        result = nb.get_multiple()
        assert "province" in result and "district" in result


@skip_if_no_data
class TestInfo:
    def test_returns_dataframe(self):
        import nepalboundaries as nb
        result = nb.info("district")
        assert isinstance(result, pd.DataFrame)

    def test_invalid_level_raises(self):
        import nepalboundaries as nb
        with pytest.raises(ValueError):
            nb.info("country")

    def test_has_expected_columns(self):
        import nepalboundaries as nb
        result = nb.info("district")
        for col in ["level", "features", "crs"]:
            assert col in result.columns


@skip_if_no_data
class TestListLevels:
    def test_returns_dict_with_all_levels(self):
        import nepalboundaries as nb
        result = nb.list_levels()
        assert isinstance(result, dict)
        for level in ["country", "province", "district", "municipality", "ward"]:
            assert level in result

    def test_counts_are_ints_or_not_available(self):
        import nepalboundaries as nb
        for k, v in nb.list_levels().items():
            assert isinstance(v, (int, str)), f"Unexpected type for {k}: {type(v)}"


@skip_if_no_data
class TestClearCache:
    def test_clear_cache(self):
        import nepalboundaries as nb
        from nepalboundaries.core import _cache
        nb.get_province()
        assert len(_cache) > 0
        nb.clear_cache()
        assert len(_cache) == 0
