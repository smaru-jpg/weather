import matplotlib.pyplot as plt
import pandas as pd
import os
from getpass import getpass

from obs_sonde_data import zonde
from gfs_data2 import gfs_data, wind_direction_speed
from kim_data import KimResponseFormatError, kim_data, parse_kim_levels


# (관측 파일의 지점명, 위도, 경도)
STATIONS = [
    ("백령도", 37.9740, 124.7124),
    ("북강릉", 37.8046, 128.8553),
    ("추풍령", 36.220, 127.995),
    ("포항", 36.0326, 129.3796),
    ("창원", 35.1702, 128.5728),
    ("흑산도", 34.6872, 125.4510),
    ("국가태풍센터", 33.3315, 126.6784),
    ("덕적북리", 37.2645, 126.1030),
]


def plot_comparison_profiles(observations, results, station_name="백령도", *, kim_text=None):
    pressure_column = "기압(hPa)"
    gfs = pd.DataFrame(results).sort_values(pressure_column)
    kim = None
    if kim_text is not None:
        kim_rows = []
        for pressure, temperature, u, v, height in parse_kim_levels(kim_text):
            direction, speed = wind_direction_speed(u, v)
            kim_rows.append({
                pressure_column: pressure,
                "기온(°C)": temperature - 273.15,
                "풍향(deg)": direction,
                "풍속(m/s)": speed,
                "고도(gpm)": height,
            })
        kim = pd.DataFrame(kim_rows).sort_values(pressure_column)
    model_names = "GFS vs KIM" if kim is not None else "GFS"
    panels = [
        ("기온(°C)", "기온(°C)", "Temperature (K)"),
        ("풍향(deg)", "풍향(deg)", "Wind direction (mil)"),
        ("풍속(knot)", "풍속(m/s)", "Wind speed (kt)"),
        ("고도(gpm)", "고도(gpm)", "Geopotential height (gpm)"),
    ]

    for observed_at, profile in observations.groupby("일시(UTC)", sort=True):
        profile = profile.sort_values(pressure_column)
        figure, axes = plt.subplots(1, 4, sharey=True, figsize=(14, 6), layout="constrained")
        figure.suptitle(
            f"{station_name} | Radiosonde ({observed_at} UTC) vs {model_names}",
            fontfamily="Malgun Gothic",
        )

        axes[0].set_ylabel("Pressure (hPa)")
        axes[0].invert_yaxis()
        for axis, (sonde_column, gfs_column, label) in zip(axes, panels):
            sonde_values = pd.to_numeric(profile[sonde_column], errors="coerce")
            gfs_values = pd.to_numeric(gfs[gfs_column], errors="coerce")
            scale = 1
            offset = 0
            if gfs_column == "기온(°C)":
                offset = 273.15
                sonde_values = sonde_values + offset
            elif gfs_column == "풍향(deg)":
                scale = 6400 / 360
                sonde_values = sonde_values * scale
                axis.set_xticks([0, 1600, 3200, 4800, 6400])
                axis.set_xlim(0, 6400)
            elif gfs_column == "풍속(m/s)":
                scale = 3600 / 1852

            line_style = "none" if gfs_column == "풍향(deg)" else "-"
            axis.plot(
                sonde_values, profile[pressure_column],
                marker="o", linestyle=line_style, linewidth=0.7,
                color="red", markersize=4, label="Radiosonde", zorder=3,
            )
            axis.plot(
                gfs_values * scale + offset, gfs[pressure_column],
                marker="^", linestyle=line_style, linewidth=0.7,
                color="blue", markersize=4, label="GFS",
            )
            if kim is not None:
                kim_values = pd.to_numeric(kim[gfs_column], errors="coerce")
                axis.plot(
                    kim_values * scale + offset, kim[pressure_column],
                    marker="s", linestyle=line_style, linewidth=0.7,
                    color="green", markersize=4, label="KIM",
                )
            axis.set_xlabel(label)
            axis.grid(alpha=0.3)

        axes[0].legend()


def main():
    coordinates_by_name = {name: (lat, lon) for name, lat, lon in STATIONS}
    print("선택 가능한 지점: " + ", ".join(coordinates_by_name))
    station_name = input("출력할 지점명을 입력하세요: ").strip()
    if station_name not in coordinates_by_name:
        raise SystemExit(f"등록되지 않은 지점입니다: {station_name}")

    latitude, longitude = coordinates_by_name[station_name]
    auth_key = os.getenv("KMA_API_KEY", "").strip()
    if not auth_key:
        key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".kma-api-key")
        if os.path.isfile(key_file):
            with open(key_file, encoding="utf-8-sig") as key_input:
                auth_key = next(
                    (line for line in map(str.strip, key_input) if line and not line.startswith("#")),
                    "",
                )
    if not auth_key:
        auth_key = getpass("기상청 API 인증키를 입력하세요: ").strip()
    if not auth_key:
        raise SystemExit("KIM 자료를 조회하려면 기상청 API 인증키가 필요합니다.")
    kim_text = kim_data(latitude, longitude, auth_key=auth_key)
    observations = zonde(station_name)
    results = gfs_data(latitude, longitude)
    try:
        plot_comparison_profiles(observations, results, station_name, kim_text=kim_text)
    except KimResponseFormatError as error:
        lines = kim_text.replace(auth_key, "[인증키 숨김]").strip().splitlines()
        preview = "\n".join(lines[:16])[:1600]
        raise SystemExit(f"{error}\n기상청 응답 앞부분:\n{preview}") from None
    plt.show()


if __name__ == "__main__":
    main()
