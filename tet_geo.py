from geopy.distance import geodesic

# Координаты двух точек (широта, долгота)
point_a = (53.396477, 58.977009)
point_b = (53.397429, 58.976927)

# Вычисление геодезического расстояния
distance = geodesic(point_a, point_b).meters

print(f"Расстояние между точками: {distance} метров")