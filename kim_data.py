import os
from math import isfinite
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


KIM_POINT_URL = (
    "https://apihub.kma.go.kr/api/typ06/cgi-bin/url/nph-kim_nc_pt_txt2_std"
)
KIML_PRESSURE_LEVELS = frozenset({
    1000, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600,
    550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 70, 50,
})


def kim_data(
    latitude: float,
    longitude: float,
    *,
    tmfc: str = "2026112100",
    hf: int = 0,
    auth_key: str | None = None,
) -> str:
    """Return KIML temperature, U/V wind, and geopotential height as API text."""
    auth_key = auth_key or os.getenv("KMA_API_KEY")
    if not auth_key:
        raise ValueError("Set KMA_API_KEY or pass auth_key.")

    query = urlencode({
        "group": "KIML",
        "nwp": "L010",
        "data": "P",
        "name": "T,U,V,GPH",
        "tmfc": tmfc,
        "hf": hf,
        "disp": "A",
        "help": 1,
        "lat": latitude,
        "lon": longitude,
        "authKey": auth_key,
    })

    try:
        with urlopen(f"{KIM_POINT_URL}?{query}", timeout=30) as response:
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            try:
                return body.decode(charset)
            except (UnicodeDecodeError, LookupError):
                return body.decode("cp949")
    except HTTPError as error:
        raise RuntimeError(f"KMA API request failed (HTTP {error.code}).") from None
    except (URLError, TimeoutError):
        raise RuntimeError("Could not connect to the KMA API.") from None


class KimResponseFormatError(ValueError):
    """The response contains no recognizable pressure-level data."""


def parse_kim_levels(response: str) -> list[tuple[float, float, float, float, float]]:
    """Group KMA point records by pressure and return T, U, V, and GPH."""
    variables = ("T", "U", "V", "GPH")
    values_by_level = {}
    for line in response.splitlines():
        fields = line.partition("#")[0].split(maxsplit=5)
        if len(fields) != 6:
            continue
        _, _, _, level, value, name = fields
        variable = name.partition("(")[0].strip()
        if variable not in variables:
            continue
        try:
            pressure = float(level)
            value = float(value)
        except ValueError:
            continue
        if pressure not in KIML_PRESSURE_LEVELS:
            continue
        values_by_level.setdefault(pressure, {})[variable] = (
            value if isfinite(value) and value > -999 else float("nan")
        )

    if not values_by_level:
        raise KimResponseFormatError("KIM 응답에서 기압, T, U, V, GPH 데이터 행을 찾지 못했습니다.")
    missing_variables = set(variables).difference(
        variable for values in values_by_level.values() for variable in values
    )
    if missing_variables:
        missing = ", ".join(sorted(missing_variables))
        raise KimResponseFormatError(f"KIM 응답에 요청한 변수가 누락되었습니다 ({missing}).")

    missing_value = float("nan")
    return [
        (pressure, values.get("T", missing_value), values.get("U", missing_value),
         values.get("V", missing_value), values.get("GPH", missing_value))
        for pressure, values in values_by_level.items()
    ]
