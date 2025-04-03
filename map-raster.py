#!/usr/bin/env python3

import simplekml
from geopy.distance import geodesic

# center point
center_lat=47.567988
center_lon=9.372969

# size of the grid
grid_width=18000
grid_height=18000

# number of cells in the grid
rows=11
cols=11

# cell size
square_size=50

# start index for naming (here we use two so that we can roll a double dice)
start_index=2



def generate_grid_kml(center_lat, center_lon, grid_width, grid_height, rows, cols, square_size, start_index=0, output_file="grid.kml"):
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

            # Placemark hinzufügen (Textlabel verschoben nach Süden)
            # Verschiebe das Textlabel um die halbe Quadratgröße nach Süden
            label_offset = geodesic(meters=square_size).destination((cell_center.latitude, cell_center.longitude), bearing=180)

            cell_name = f"Position {c+start_index},{r+start_index}"
            # Füge ein Polygon hinzu
            pol = kml.newpolygon(
                name=cell_name,
                outerboundaryis=[
                    (top_left.longitude, top_left.latitude),
                    (top_right.longitude, top_right.latitude),
                    (bottom_right.longitude, bottom_right.latitude),
                    (bottom_left.longitude, bottom_left.latitude),
                    (top_left.longitude, top_left.latitude),  # Abschluss des Polygons
                ]
            )
            pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.red)  # 180 = 70% Deckkraft

            # Placemark hinzufügen (Textlabel)
            placemark = kml.newpoint(
                name=f"{c+start_index},{r+start_index}",
                coords=[(label_offset.longitude, label_offset.latitude)]  # Textlabel verschoben nach Süden
            )
            placemark.style.labelstyle.color = simplekml.Color.red  # Textfarbe (optional)
            placemark.style.labelstyle.scale = 1.5  # Textgröße (optional)

    kml.save(output_file)
    print(f"KML-Datei gespeichert: {output_file}")

generate_grid_kml(center_lat, center_lon, grid_width, grid_height, rows, cols, square_size, start_index)
