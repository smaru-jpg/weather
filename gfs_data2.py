import pygrib
import numpy as np
import pandas as pd
import math

def bilinear_interpolate(q11, q21, q12, q22, x, y, x1, x2, y1, y2):
    value_at_y1 = (x2 - x) / (x2 - x1) * q11 + (x - x1) / (x2 - x1) * q21
    value_at_y2 = (x2 - x) / (x2 - x1) * q12 + (x - x1) / (x2 - x1) * q22
    return (y2 - y) / (y2 - y1) * value_at_y1 + (y - y1) / (y2 - y1) * value_at_y2

def wind_direction_speed(u, v):
    speed = math.hypot(u, v)
    direction = (math.degrees(math.atan2(-u, -v)) % 360) if speed else None
    return direction, speed

def find_index(latitude, longitude, lats, lons):
    row = np.flatnonzero(
        np.isclose(lats[:, 0], latitude, atol=1e-6, rtol=0)
    )[0]
    col = np.flatnonzero(
        np.isclose(lons[0, :], longitude % 360, atol=1e-6, rtol=0)
    )[0]
    return row, col

def gfs_data(latitude=None, longitude=None):

    grbs = pygrib.open("gfs.t00z.pgrb2.0p25.f000")

    y = latitude if latitude is not None else float(input("대상 위도를 입력하세요: "))
    x = longitude if longitude is not None else float(input("대상 경도를 입력하세요: "))

    y1 = math.floor(y / 0.5) * 0.5
    x1 = math.floor(x / 0.5) * 0.5
    y2 = y1 + 0.5
    x2 = x1 + 0.5

    gh_list = grbs.select(name="Geopotential height", typeOfLevel="isobaricInhPa")
    tmp = grbs.select(name="Temperature", typeOfLevel="isobaricInhPa")
    rh = grbs.select(name="Relative humidity", typeOfLevel="isobaricInhPa")
    u = grbs.select(name="U component of wind", typeOfLevel="isobaricInhPa")
    v = grbs.select(name="V component of wind", typeOfLevel="isobaricInhPa")

    tmp_by_level = {grb.level: grb for grb in tmp}
    rh_by_level = {grb.level: grb for grb in rh}
    u_by_level = {grb.level: grb for grb in u}
    v_by_level = {grb.level: grb for grb in v}

    lats, lons = gh_list[0].latlons()

    idx_11 = find_index(y1, x1, lats, lons)
    idx_21 = find_index(y1, x2, lats, lons)
    idx_12 = find_index(y2, x1, lats, lons)
    idx_22 = find_index(y2, x2, lats, lons)

    profiles = []
    for grb in gh_list:
        level = grb.level
        fields = (
            ("GH", grb),
            ("T", tmp_by_level.get(level)),
            ("RH", rh_by_level.get(level)),
            ("U", u_by_level.get(level)),
            ("V", v_by_level.get(level)),
        )

        interpolated = {}
        for name, field in fields:
            if field is None:
                continue

            values = field.values
            Q_11 = values[idx_11]
            Q_21 = values[idx_21]
            Q_12 = values[idx_12]
            Q_22 = values[idx_22]

            interpolated[name] = bilinear_interpolate(Q_11, Q_21, Q_12, Q_22, x, y, x1, x2, y1, y2)

        results = []
        for name, unit in (("GH", "m"), ("T", "K"), ("RH", "%")):
            value = interpolated.get(name)
            results.append(f"{name} {value} {unit}" if value is not None else f"{name} 결측")

        if "U" in interpolated and "V" in interpolated:
            direction, speed = wind_direction_speed(interpolated["U"], interpolated["V"])
            direction_text = f"{direction:.2f}°" if direction is not None else "없음(무풍)"
            results.extend((f"풍향 {direction_text}", f"풍속 {speed:.2f} m/s"))
        else:
            direction, speed = None, None
            results.extend(("풍향 결측", "풍속 결측"))

        print(f"{level} hPa: {', '.join(results)}")

        temperature = interpolated.get("T")
        profiles.append({
            "기압(hPa)": level,
            "기온(°C)": temperature - 273.15 if temperature is not None else None,
            "풍향(deg)": direction,
            "풍속(m/s)": speed,
            "고도(gpm)": interpolated.get("GH"),
        })

    return profiles
