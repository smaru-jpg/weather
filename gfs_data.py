import pygrib
import numpy as np
import pandas as pd
import math

def bilinear_interpolate(q11, q21, q12, q22, x, y, x1, x2, y1, y2):
    value_at_y1 = (x2 - x) / (x2 - x1) * q11 + (x - x1) / (x2 - x1) * q21
    value_at_y2 = (x2 - x) / (x2 - x1) * q12 + (x - x1) / (x2 - x1) * q22
    return (y2 - y) / (y2 - y1) * value_at_y1 + (y - y1) / (y2 - y1) * value_at_y2

def find_index(latitude, longitude):
    row = np.flatnonzero(
        np.isclose(lats[:, 0], latitude, atol=1e-6, rtol=0)
    )[0]
    col = np.flatnonzero(
        np.isclose(lons[0, :], longitude % 360, atol=1e-6, rtol=0)
    )[0]
    return row, col

grbs = pygrib.open("gfs_4_20260916_0000_000.grb2")

y = float(input("대상 위도를 입력하세요: "))
x = float(input("대상 경도를 입력하세요: "))

y1 = math.floor(y / 0.5) * 0.5
x1 = math.floor(x / 0.5) * 0.5
y2 = y1 + 0.5
x2 = x1 + 0.5

gh_list = grbs.select(name="Geopotential height", typeOfLevel="isobaricInhPa")
tmp = grbs.select(name='Temperature', typeOfLevel='isobaricInhPa')

lats, lons = gh_list[0].latlons()

idx_11 = find_index(y1, x1)
idx_21 = find_index(y1, x2)
idx_12 = find_index(y2, x1)
idx_22 = find_index(y2, x2)

for grb in gh_list:
    Q_11 = grb.values[idx_11]
    Q_21 = grb.values[idx_21]
    Q_12 = grb.values[idx_12]
    Q_22 = grb.values[idx_22]

    bilinear_value = bilinear_interpolate(Q_11,Q_21,Q_12,Q_22,x,y,x1,x2,y1,y2)
    print(f"{grb.level} hPa: {bilinear_value} m")
