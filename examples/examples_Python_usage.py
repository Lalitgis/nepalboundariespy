"""
nepalboundaries - Python Package Usage Examples

Installation:
    pip install nepalboundaries

Or from GitHub:
    pip install git+https://github.com/yourusername/nepalboundaries.git
"""

import nepalboundaries as nb
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# ========================================================================
# BASIC USAGE - GET BOUNDARIES AT DIFFERENT LEVELS
# ========================================================================

# Get country boundary
nepal = nb.get_country()
nepal.plot()
plt.title("Nepal Country Boundary")
plt.show()

# Get all provinces
provinces = nb.get_province()
provinces.plot(figsize=(12, 10), alpha=0.5, edgecolor='k')
plt.title("Provinces of Nepal")
plt.show()

# Get all districts
districts = nb.get_district()
districts.plot(figsize=(12, 10), alpha=0.5, edgecolor='gray')
plt.title("Districts of Nepal")
plt.show()

# Get all municipalities
municipalities = nb.get_municipality()
municipalities.plot(figsize=(12, 10), edgecolor='gray')
plt.title("Municipalities of Nepal")
plt.show()

# Get all wards
wards = nb.get_ward()
print(f"Total wards in Nepal: {len(wards)}")
print(wards.head())

# ========================================================================
# FILTERING BY PROVINCE
# ========================================================================

# Get a specific province
bagmati = nb.get_province("Bagmati")
bagmati.plot(figsize=(10, 8), alpha=0.7, color='lightblue', edgecolor='black')
plt.title("Bagmati Province")
plt.show()

# Get multiple provinces
provinces_list = nb.get_province(["Bagmati", "Gandaki"])
provinces_list.plot(figsize=(10, 8), alpha=0.5, edgecolor='black')
plt.title("Bagmati and Gandaki Provinces")
plt.show()

# Get districts in Bagmati province
bagmati_districts = nb.get_district(province="Bagmati")
bagmati_districts.plot(figsize=(10, 8), alpha=0.5, edgecolor='black')
plt.title("Districts in Bagmati Province")
plt.show()

print(f"Districts in Bagmati: {bagmati_districts['district_name'].unique()}")

# Get municipalities in Bagmati province
bagmati_municipalities = nb.get_municipality(province="Bagmati")
print(f"Municipalities in Bagmati: {len(bagmati_municipalities)}")
print(bagmati_municipalities[['municipality_name', 'district_name']])

# Get wards in Bagmati province
bagmati_wards = nb.get_ward(province="Bagmati")
print(f"Wards in Bagmati: {len(bagmati_wards)}")

# ========================================================================
# FILTERING BY DISTRICT
# ========================================================================

# Get a specific district
kathmandu_dist = nb.get_district("Kathmandu")
kathmandu_dist.plot(figsize=(10, 8), color='lightyellow', edgecolor='black')
plt.title("Kathmandu District")
plt.show()

# Get municipalities in Kathmandu District
kathmandu_mun = nb.get_municipality(district="Kathmandu")
print(f"Municipalities in Kathmandu District: {len(kathmandu_mun)}")
print(kathmandu_mun[['municipality_name']].drop_duplicates())

# Get wards in Kathmandu District
kathmandu_wards = nb.get_ward(district="Kathmandu")
print(f"Total wards in Kathmandu District: {len(kathmandu_wards)}")

# ========================================================================
# FILTERING BY MUNICIPALITY
# ========================================================================

# Get a specific municipality
kathmandu_metro = nb.get_municipality("Kathmandu")
print(f"Area of Kathmandu Metropolitan City: {kathmandu_metro['area_km2'].values[0]:.2f} km²")

# Plot Kathmandu Metro
kathmandu_metro.plot(figsize=(8, 8), color='lightcoral', edgecolor='black')
plt.title("Kathmandu Metropolitan City")
plt.show()

# Get wards in Kathmandu Metropolitan City
ktm_wards = nb.get_ward(municipality="Kathmandu")
print(f"Wards in Kathmandu Metro: {len(ktm_wards)}")
print(ktm_wards[['ward_number', 'ward_name']].head(10))

# Plot wards
fig, ax = plt.subplots(figsize=(10, 10))
ktm_wards.plot(ax=ax, alpha=0.5, edgecolor='black')
ktm_wards['ward_number'].astype(str).apply(lambda x: ax.text(0, 0, x))  # Add ward numbers
plt.title("Wards in Kathmandu Metropolitan City")
plt.show()

# ========================================================================
# SPATIAL ANALYSIS - CALCULATE AREAS
# ========================================================================

# Calculate area of all districts
districts['area_km2'] = districts.geometry.area / 1e6

# Find largest districts
largest_districts = (
    districts[['district_name', 'province_name', 'area_km2']]
    .sort_values('area_km2', ascending=False)
    .head(10)
)
print("Largest Districts in Nepal:")
print(largest_districts)

# Find smallest districts
smallest_districts = (
    districts[['district_name', 'province_name', 'area_km2']]
    .sort_values('area_km2')
    .head(5)
)
print("\nSmallest Districts in Nepal:")
print(smallest_districts)

# ========================================================================
# VISUALIZATION WITH MATPLOTLIB
# ========================================================================

# Plot districts colored by area
fig, ax = plt.subplots(figsize=(14, 12))
districts.plot(column='area_km2', ax=ax, legend=True, 
               cmap='YlOrRd', edgecolor='white', linewidth=0.5)
plt.title('Nepal Districts by Area', fontsize=16, fontweight='bold')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()

# Plot multiple levels
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# Provinces
provinces.plot(ax=axes[0, 0], alpha=0.5, edgecolor='black')
axes[0, 0].set_title("Provinces of Nepal", fontweight='bold')

# Districts
districts.plot(ax=axes[0, 1], alpha=0.5, edgecolor='gray')
axes[0, 1].set_title("Districts of Nepal", fontweight='bold')

# Municipalities
municipalities.plot(ax=axes[1, 0], edgecolor='gray', alpha=0.3)
axes[1, 0].set_title("Municipalities of Nepal", fontweight='bold')

# Wards (sample - all wards is too dense)
bagmati_wards.plot(ax=axes[1, 1], edgecolor='gray', alpha=0.3)
axes[1, 1].set_title("Wards in Bagmati Province (Sample)", fontweight='bold')

plt.tight_layout()
plt.show()

# ========================================================================
# COMBINING MULTIPLE LEVELS
# ========================================================================

# Get multiple levels at once
levels = nb.get_multiple(['province', 'district'])

# Plot both together
fig, ax = plt.subplots(figsize=(14, 12))
levels['province'].plot(ax=ax, alpha=0, edgecolor='red', linewidth=2, label='Provinces')
levels['district'].plot(ax=ax, alpha=0, edgecolor='blue', linewidth=0.5, label='Districts')
plt.title("Nepal: Provinces and Districts", fontsize=14, fontweight='bold')
plt.legend()
plt.show()

# ========================================================================
# DATA EXPLORATION
# ========================================================================

# Get summary information
print("Available administrative levels:")
print(nb.list_levels())

# Get info about a level
print("\nDistrict Information:")
print(nb.info('district'))

# Explore data
print("\nSample districts:")
print(districts[['district_name', 'province_name', 'area_km2']].head(10))

# Get unique provinces
print("\nUnique provinces:")
print(districts['province_name'].unique())

# Get data statistics
print("\nDistribution of districts by province:")
print(districts['province_name'].value_counts().sort_index())

print("\nDistribution of municipalities by province:")
municipalities_dist = nb.get_municipality()
print(municipalities_dist['province_name'].value_counts().sort_index())

# ========================================================================
# DATA EXPORT
# ========================================================================

# Save as shapefile
districts.to_file('nepal_districts.shp')

# Save as GeoJSON
municipalities.to_file('nepal_municipalities.geojson', driver='GeoJSON')

# Save as GeoPackage
provinces.to_file('nepal_provinces.gpkg', driver='GPKG')

# Save attribute data as CSV
districts[['district_name', 'province_name', 'area_km2']].to_csv(
    'nepal_districts.csv', index=False
)

print("Data exported successfully!")

# ========================================================================
# SPATIAL OPERATIONS
# ========================================================================

# Find which district contains a point (Kathmandu coordinates)
point = Point(85.3240, 27.7172)
sample_point = gpd.GeoDataFrame({'geometry': [point]}, crs='EPSG:4326')

# Spatial join
result = gpd.sjoin(sample_point, districts, how='left', predicate='within')
print(f"\nPoint at {point.x}, {point.y} is in {result['district_name'].values[0]} district")

# Find districts that touch Kathmandu District
kathmandu_district = districts[districts['district_name'] == 'Kathmandu'].iloc[0]
adjacent = districts[districts.touches(kathmandu_district.geometry)]
print(f"\nDistricts adjacent to Kathmandu: {adjacent['district_name'].tolist()}")

# Calculate distances between district centroids
print("\nCentroid of Kathmandu District:")
print(kathmandu_district.geometry.centroid)

# ========================================================================
# INTERACTIVE VISUALIZATION (OPTIONAL)
# ========================================================================

# Install: pip install folium
try:
    import folium
    
    # Create interactive map
    m = folium.Map(
        location=[28.3949, 84.1240],  # Center of Nepal
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add districts
    for idx, row in districts.iterrows():
        folium.GeoJson(
            row['geometry'],
            popup=row['district_name'],
            style_function=lambda x: {'color': 'blue', 'weight': 1}
        ).add_to(m)
    
    # Save map
    m.save('nepal_districts_map.html')
    print("\nInteractive map saved to 'nepal_districts_map.html'")
except ImportError:
    print("Install folium for interactive maps: pip install folium")

# ========================================================================
# CLEAR CACHE (If needed to free memory after working with large datasets)
# ========================================================================

# nb.clear_cache()
