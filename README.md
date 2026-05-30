# NP nepalboundaries.py

**Administrative boundaries of Nepal for Python** — country, province, district, municipality, and ward level, all in a single `pip install`.

<p align="center">
  <img src="logo.png" width="180"/>
</p>

<p align="center">


[![PyPI version](https://badge.fury.io/py/nepalboundaries.svg)](https://pypi.org/project/nepalboundaries/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/Lalitgis/nepalboundaries)](https://github.com/Lalitgis/nepalboundaries/issues)

Inspired by [rgeoboundaries](https://github.com/wmgeolab/rgeoboundaries) but tailored specifically for Nepal — standardised column names, WGS84 projection, and hierarchical filtering baked in.

[logo]

---

## Installation

```bash
# From GitHub (latest)
pip install git+https://github.com/Lalitgis/nepalboundariespy.git

# From PyPI (when published)
pip install nepalboundariespy

# With visualisation extras (matplotlib + folium)
pip install nepalboundariespy[viz]
```

**Requirements:** Python ≥ 3.8, geopandas ≥ 0.10, shapely ≥ 1.8, pandas ≥ 1.0

---

## Quick start

```python
import nepalboundariespy as nb

# All 7 provinces
provinces = nb.get_province()
provinces.plot(figsize=(12, 8), edgecolor="black", alpha=0.6)

# All 77 districts
districts = nb.get_district()

# Districts in one province
bagmati = nb.get_district(province="Bagmati")

# Wards in Kathmandu
ktm_wards = nb.get_ward(municipality="Kathmandu")
print(f"Kathmandu has {len(ktm_wards)} wards")

# Check what's available
nb.list_levels()
# {'country': 1, 'province': 7, 'district': 77, 'municipality': 753, 'ward': 6743}
```

---

## API reference

### Boundary functions

| Function | Description |
|---|---|
| `get_country()` | Nepal national boundary |
| `get_province(province=None)` | Provincial boundaries (7 total) |
| `get_district(district=None, province=None)` | District boundaries (77 total) |
| `get_municipality(municipality=None, district=None, province=None)` | Municipality boundaries (753 total) |
| `get_ward(ward=None, municipality=None, district=None, province=None)` | Ward boundaries (6 743 total) |
| `get_multiple(levels=['province','district'])` | Fetch multiple levels at once → `dict` |

All functions accept a **single string** or a **list of strings** for each filter parameter.

### Utility functions

| Function | Description |
|---|---|
| `list_levels()` | Feature counts for all levels |
| `info(level)` | One-row summary (count, columns, CRS) |
| `clear_cache()` | Free in-memory cache |

### Convenience aliases

`get_prov` → `get_province`  ·  `get_dist` → `get_district`  ·  `get_mun` → `get_municipality`

---

## Examples

### Filtering

```python
import nepalboundariespy as nb

# Single filter
bhaktapur = nb.get_district("Bhaktapur")

# Multiple at once
two_provinces = nb.get_province(["Bagmati", "Gandaki"])

# Hierarchical filter — municipalities inside a specific district
patan_mun = nb.get_municipality(district="Lalitpur")

# All wards in province 3 (Bagmati)
bagmati_wards = nb.get_ward(province="Bagmati")
```

### Plotting

```python
import matplotlib.pyplot as plt
import nepalboundariespy as nb

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

nb.get_province().plot(ax=axes[0], edgecolor="black", alpha=0.6)
axes[0].set_title("Provinces of Nepal")

nb.get_district(province="Bagmati").plot(ax=axes[1], edgecolor="black", alpha=0.6)
axes[1].set_title("Districts in Bagmati Province")

plt.tight_layout()
plt.show()
```

### Interactive map with Folium

```python
import folium
import nepalboundariespy as nb

m = folium.Map(location=[28.3949, 84.1240], zoom_start=7)

folium.GeoJson(
    nb.get_district().to_json(),
    name="Districts",
    tooltip=folium.GeoJsonTooltip(fields=["district_name", "province_name"]),
).add_to(m)

folium.LayerControl().add_to(m)
m.save("nepal_districts.html")
```

### Spatial analysis

```python
import geopandas as gpd
from shapely.geometry import Point
import nepalboundariespy as nb

# Point-in-polygon: which district contains Kathmandu Durbar Square?
point = gpd.GeoDataFrame(
    {"geometry": [Point(85.3157, 27.7044)]}, crs="EPSG:4326"
)
match = gpd.sjoin(point, nb.get_district(), how="left", predicate="within")
print(match["district_name"].values[0])   # → Kathmandu

# Neighbouring districts
ktm = nb.get_district("Kathmandu").iloc[0]
neighbours = nb.get_district()[nb.get_district().touches(ktm.geometry)]
print(neighbours["district_name"].tolist())
```

### Export data

```python
import nepalboundariespy as nb

districts = nb.get_district()

districts.to_file("nepal_districts.geojson", driver="GeoJSON")
districts.to_file("nepal_districts.gpkg", driver="GPKG")
districts.to_file("nepal_districts.shp")

# Attribute table only (no geometry)
districts.drop(columns="geometry").to_csv("nepal_districts.csv", index=False)
```

---

## Data structure

```
Nepal (Country)
└── 7 Provinces
    └── 77 Districts
        └── 753 Municipalities / Rural Municipalities + Procted Areas of Nepal
            └── 6743 Wards
```

All data is projected to **WGS84 (EPSG:4326)**.

### Column names by level

| Level | Key columns |
|---|---|
| country | `geometry` |
| province | `province_name`, `province_code`, `area_km2`, `geometry` |
| district | `district_name`, `district_code`, `province_name`, `area_km2`, `geometry` |
| municipality | `municipality_name`, `municipality_code`, `district_name`, `province_name`, `area_km2`, `geometry` |
| ward | `ward_number`, `municipality_name`, `district_name`, `province_name`, `geometry` |

---

## Preparing/updating the data

The package expects GeoJSON files in `nepalboundaries/data/`.  
Use the provided script to convert your raw boundary files:

```bash
# Edit the paths inside the script, then run:
python scripts/data_preparation_python.py
```

---

## Repository structure

```
nepalboundariespy/                  ← GitHub repo root
├── nepalboundariespy/              ← Python package
│   ├── __init__.py
│   ├── core.py
│   └── data/
│       ├── country.geojson
│       ├── province.geojson
│       ├── district.geojson
│       ├── municipality.geojson
│       └── ward.geojson
├── tests/
│   └── test_nepalboundaries.py
├── examples/
│   └── examples_Python_usage.py
├── scripts/
│   └── data_preparation_python.py
├── setup.py
├── MANIFEST.in
├── LICENSE
├── CHANGELOG.md
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Make your changes and add tests
4. Run the test suite: `pytest tests/ -v`
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Citation

```bibtex
@software{nepalboundariespy2026,
  title   = {nepalboundariespy: Administrative Boundaries of Nepal},
  author  = {BC Lalit},
  year    = {2026},
  url     = {https://github.com/Lalitgis/nepalboundariespy}
}
```

---

## Related resources

- [Nepal CBS](https://cbs.gov.np/) — Central Bureau of Statistics
- [HDX Nepal](https://data.humdata.org/dataset?tags=nepal) — Humanitarian Data Exchange
- [OpenStreetMap Nepal](https://wiki.openstreetmap.org/wiki/Nepal)
- [rgeoboundaries](https://github.com/wmgeolab/rgeoboundaries) — R package that inspired this
