"""
Data Preparation Script for nepalboundaries Python Package

This script loads your boundary shapefiles/geojson files and prepares them
for distribution with the package.
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
import json

# ====================================================================
# CONFIGURATION - UPDATE THESE PATHS TO YOUR DATA FILES
# ====================================================================

# Path to your data files directory
DATA_INPUT_DIR = Path("/path/to/your/nepal/boundary/files")
DATA_OUTPUT_DIR = Path("nepalboundaries/data")

# Create output directory if it doesn't exist
DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ====================================================================
# LOAD DATA FROM YOUR FILES
# ====================================================================

print("Loading boundary data...")

# Load country boundary
# Update file paths and names based on your actual files
country = gpd.read_file(DATA_INPUT_DIR / "country_boundary.geojson")
province = gpd.read_file(DATA_INPUT_DIR / "province_boundary.geojson")
district = gpd.read_file(DATA_INPUT_DIR / "district_boundary.geojson")
municipality = gpd.read_file(DATA_INPUT_DIR / "municipality_boundary.geojson")
ward = gpd.read_file(DATA_INPUT_DIR / "ward_boundary.geojson")

# ====================================================================
# STANDARDIZE COLUMN NAMES AND DATA
# ====================================================================

print("Standardizing column names...")

# Convert all column names to lowercase
def standardize_columns(gdf):
    gdf.columns = gdf.columns.str.lower()
    return gdf

country = standardize_columns(country)
province = standardize_columns(province)
district = standardize_columns(district)
municipality = standardize_columns(municipality)
ward = standardize_columns(ward)

# Rename columns to match expected names
# ADJUST THESE BASED ON YOUR ACTUAL COLUMN NAMES!

province = province.rename(columns={
    'name': 'province_name',
    'code': 'province_code'  # if you have a code column
}).sort_values('province_name')

district = district.rename(columns={
    'name': 'district_name',
    'code': 'district_code',
    'province': 'province_name'  # adjust if needed
}).sort_values('district_name')

municipality = municipality.rename(columns={
    'name': 'municipality_name',
    'code': 'municipality_code',
    'district': 'district_name',
    'province': 'province_name'
}).sort_values('municipality_name')

ward = ward.rename(columns={
    'ward_id': 'ward_number',
    'name': 'ward_name',
    'municipality': 'municipality_name',
    'district': 'district_name',
    'province': 'province_name'
}).sort_values(['municipality_name', 'ward_number'])

# ====================================================================
# ADD USEFUL METADATA
# ====================================================================

print("Calculating statistics...")

# Add area in km²
for gdf in [country, province, district, municipality, ward]:
    if 'area_km2' not in gdf.columns:
        gdf['area_km2'] = gdf.geometry.area / 1e6

# ====================================================================
# ENSURE CRS IS CORRECT
# ====================================================================

print("Standardizing CRS...")

for gdf in [country, province, district, municipality, ward]:
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')

# ====================================================================
# VALIDATE DATA
# ====================================================================

print("\nData Summary:")
print(f"Country features: {len(country)}")
print(f"Province features: {len(province)}")
print(f"District features: {len(district)}")
print(f"Municipality features: {len(municipality)}")
print(f"Ward features: {len(ward)}")

print("\nProvince names:", province['province_name'].unique().tolist())
print("\nSample districts:", district['district_name'].unique()[:5].tolist())
print("\nSample municipalities:", municipality['municipality_name'].unique()[:5].tolist())

# Validate geometries
for name, gdf in [('country', country), ('province', province), 
                   ('district', district), ('municipality', municipality), 
                   ('ward', ward)]:
    invalid_count = (~gdf.geometry.is_valid).sum()
    if invalid_count > 0:
        print(f"WARNING: {invalid_count} invalid geometries in {name}")
        # Fix invalid geometries
        gdf['geometry'] = gdf['geometry'].buffer(0)
        print(f"Fixed geometries in {name}")

# ====================================================================
# SAVE DATA IN MULTIPLE FORMATS
# ====================================================================

print("\nSaving data...")

# Save as GeoJSON (human-readable, web-friendly)
country.to_file(DATA_OUTPUT_DIR / 'country.geojson', driver='GeoJSON')
province.to_file(DATA_OUTPUT_DIR / 'province.geojson', driver='GeoJSON')
district.to_file(DATA_OUTPUT_DIR / 'district.geojson', driver='GeoJSON')
municipality.to_file(DATA_OUTPUT_DIR / 'municipality.geojson', driver='GeoJSON')
ward.to_file(DATA_OUTPUT_DIR / 'ward.geojson', driver='GeoJSON')

print(f"✓ GeoJSON files saved to {DATA_OUTPUT_DIR}")

# Alternative: Save as GeoPackage (more efficient)
# Uncomment this section if you prefer GeoPackage format
'''
country.to_file(DATA_OUTPUT_DIR / 'country.gpkg', driver='GPKG')
province.to_file(DATA_OUTPUT_DIR / 'province.gpkg', driver='GPKG')
district.to_file(DATA_OUTPUT_DIR / 'district.gpkg', driver='GPKG')
municipality.to_file(DATA_OUTPUT_DIR / 'municipality.gpkg', driver='GPKG')
ward.to_file(DATA_OUTPUT_DIR / 'ward.gpkg', driver='GPKG')

print(f"✓ GeoPackage files saved to {DATA_OUTPUT_DIR}")
'''

# ====================================================================
# CREATE METADATA FILE
# ====================================================================

print("Creating metadata...")

metadata = {
    'package': 'nepalboundaries',
    'version': '0.1.0',
    'description': 'Administrative boundaries of Nepal',
    'levels': {
        'country': {
            'features': int(len(country)),
            'crs': str(country.crs),
            'columns': country.columns.tolist()
        },
        'province': {
            'features': int(len(province)),
            'crs': str(province.crs),
            'columns': province.columns.tolist()
        },
        'district': {
            'features': int(len(district)),
            'crs': str(district.crs),
            'columns': district.columns.tolist()
        },
        'municipality': {
            'features': int(len(municipality)),
            'crs': str(municipality.crs),
            'columns': municipality.columns.tolist()
        },
        'ward': {
            'features': int(len(ward)),
            'crs': str(ward.crs),
            'columns': ward.columns.tolist()
        }
    }
}

# Save metadata
with open(DATA_OUTPUT_DIR / 'metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"✓ Metadata saved to {DATA_OUTPUT_DIR / 'metadata.json'}")

print("\n" + "="*50)
print("Data preparation completed successfully!")
print("="*50)
print(f"\nOutput directory: {DATA_OUTPUT_DIR}")
print("\nYour data is ready for package distribution!")
