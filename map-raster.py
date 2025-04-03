#!/usr/bin/env python3

import simplekml
from geopy.distance import geodesic

def generate_grid_kml(center_lat, center_lon, grid_width, grid_height, rows, cols, square_size, output_file="grid.kml"):
    kml = simplekml.Kml()

    # Berechnung der Zellengröße (inkl. Leerraum)
    cell_width = grid_width / cols
    cell_height = grid_height / rows

    for r in range(rows):
        for c in range(cols):
            # Berechnung der Zellmitte relativ zum Mittelpunkt
            offset_north = (r - (rows - 1) / 2) * cell_height
            offset_east = (c - (cols - 1) / 2) * cell_width
            cell_center = geodesic(meters=offset_north).destination((center_lat, center_lon), bearing=0)
            cell_center = geodesic(meters=offset_east).destination((cell_center.latitude, cell_center.longitude), bearing=90)

            # Berechnung der vier Ecken des Quadrats (zentriert in der Zelle)
            half_size = square_size / 2
            top_left = geodesic(meters=-half_size).destination((cell_center.latitude, cell_center.longitude), bearing=0)
            top_left = geodesic(meters=-half_size).destination((top_left.latitude, top_left.longitude), bearing=90)

            top_right = geodesic(meters=square_size).destination((top_left.latitude, top_left.longitude), bearing=90)
            bottom_left = geodesic(meters=square_size).destination((top_left.latitude, top_left.longitude), bearing=180)
            bottom_right = geodesic(meters=square_size).destination((top_right.latitude, top_right.longitude), bearing=180)

            # Füge ein Polygon hinzu
            pol = kml.newpolygon(
                name=f"Cell {r},{c}",
                outerboundaryis=[
                    (top_left.longitude, top_left.latitude),
                    (top_right.longitude, top_right.latitude),
                    (bottom_right.longitude, bottom_right.latitude),
                    (bottom_left.longitude, bottom_left.latitude),
                    (top_left.longitude, top_left.latitude),  # Abschluss des Polygons
                ]
            )
            pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.blue)  # Transparente blaue Füllung

    kml.save(output_file)
    print(f"KML-Datei gespeichert: {output_file}")

# Beispielaufruf: 12x12 Quadrate (20m Kantenlänge) in einem 2000x2000m Raster, zentriert auf die Koordinaten
generate_grid_kml(center_lat=47.568111, center_lon=9.370741, grid_width=2000, grid_height=2000, rows=12, cols=12, square_size=20)
