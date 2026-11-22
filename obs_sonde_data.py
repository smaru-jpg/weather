import pandas as pd

def zonde(station_name="백령도"):
    OUTPUT_COLUMNS = [
        "일시(UTC)",
        "기압(hPa)",
        "고도(gpm)",
        "풍향(deg)",
        "풍속(knot)",
        "기온(°C)",
    ]

    source = "OBS_SONDE_F00508_20261122154830.xls"
    try:
        table = pd.read_csv(source, sep="\t", encoding="cp949") #한글은 CP949로 인코딩 되어있음.
    except (ImportError, OSError, ValueError) as exc:
        raise SystemExit(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {exc}") from None

    table.columns = table.columns.str.strip()
    required_columns = ["지점명", *OUTPUT_COLUMNS]
    missing_columns = [column for column in required_columns if column not in table.columns]
    if missing_columns:
        raise SystemExit(f"엑셀에 필요한 열이 없습니다: {', '.join(missing_columns)}")

    observed_at = pd.to_datetime(table["일시(UTC)"], errors="coerce")
    station_matches = table["지점명"].astype("string").str.strip().eq(station_name)
    midnight = observed_at.eq(observed_at.dt.normalize())
    pressure = pd.to_numeric(table["기압(hPa)"], errors="coerce")
    selected = station_matches & midnight & pressure.gt(0)

    result = table.loc[selected, OUTPUT_COLUMNS].copy()
    if result.empty:
        print(f"{station_name} 00:00 UTC 등압면 관측 자료가 없습니다.")
        raise SystemExit(0)

    result["일시(UTC)"] = observed_at.loc[selected]
    result["기압(hPa)"] = pressure.loc[selected]
    result = result.sort_values(["일시(UTC)", "기압(hPa)"], ascending=[True, True])
    result["일시(UTC)"] = result["일시(UTC)"].dt.strftime("%Y-%m-%d %H:%M:%S")
    print(result.to_string(index=False, na_rep="-"))
    return result
