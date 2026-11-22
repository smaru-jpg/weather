"""수동으로 입력한 Nullschool 등압면 자료."""

# 키: (지점명, 함께 표시할 라디오존데 일시 UTC).
# 각 행: (기압 hPa, 기온 °C, 풍향 deg, 풍속 m/s, 지위고도 gpm)
# None을 실제 숫자로 바꾸세요. 화면 풍속이 kt이면 `풍속값 * 1852 / 3600`을 입력하세요.
# 기압 외의 값이 모두 None인 행은 플롯에서 생략합니다.
NULLSCHOOL_PROFILES = {
    ("백령도", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        # 풍속은 화면의 kt 값을 m/s로 변환합니다. 지위고도는 임의 값입니다.
        "rows": [
            (1000, 0.4, 320, 21 * 1852 / 3600, 110),
            (850, -11.4, 310, 20 * 1852 / 3600, 1470),
            (700, -22.3, 295, 26 * 1852 / 3600, 3020),
            (500, -34.9, 295, 49 * 1852 / 3600, 5580),
            (250, -50.7, 285, 82 * 1852 / 3600, 10400),
            (70, -58.9, 265, 60 * 1852 / 3600, 18500),
            (10, -39.2, 230, 43 * 1852 / 3600, 31000),
        ],
    },
    ("북강릉", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        "rows": [
            (1000, None, None, None, None),
            (850, None, None, None, None),
            (700, None, None, None, None),
            (500, None, None, None, None),
            (250, None, None, None, None),
            (70, None, None, None, None),
            (10, None, None, None, None),
        ],
    },
    ("추풍령", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        "rows": [
            (1000, None, None, None, None),
            (850, None, None, None, None),
            (700, None, None, None, None),
            (500, None, None, None, None),
            (250, None, None, None, None),
            (70, None, None, None, None),
            (10, None, None, None, None),
        ],
    },
    ("포항", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        "rows": [
            (1000, None, None, None, None),
            (850, None, None, None, None),
            (700, None, None, None, None),
            (500, None, None, None, None),
            (250, None, None, None, None),
            (70, None, None, None, None),
            (10, None, None, None, None),
        ],
    },
    ("창원", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        "rows": [
            (1000, None, None, None, None),
            (850, None, None, None, None),
            (700, None, None, None, None),
            (500, None, None, None, None),
            (250, None, None, None, None),
            (70, None, None, None, None),
            (10, None, None, None, None),
        ],
    },
    ("흑산도", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        "rows": [
            (1000, None, None, None, None),
            (850, None, None, None, None),
            (700, None, None, None, None),
            (500, None, None, None, None),
            (250, None, None, None, None),
            (70, None, None, None, None),
            (10, None, None, None, None),
        ],
    },
    ("국가태풍센터", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        "rows": [
            (1000, None, None, None, None),
            (850, None, None, None, None),
            (700, None, None, None, None),
            (500, None, None, None, None),
            (250, None, None, None, None),
            (70, None, None, None, None),
            (10, None, None, None, None),
        ],
    },
    ("덕적북리", "2026-11-21 00:00:00"): {
        "valid_at": "2026-11-21 00:00 UTC",
        "rows": [
            (1000, None, None, None, None),
            (850, None, None, None, None),
            (700, None, None, None, None),
            (500, None, None, None, None),
            (250, None, None, None, None),
            (70, None, None, None, None),
            (10, None, None, None, None),
        ],
    },
}
