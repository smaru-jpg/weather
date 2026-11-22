# 기상 연직 프로파일 비교

선택한 관측소의 라디오존데 자료와 GFS, KIM 국지모델의 등압면 자료를 한 그림에서 비교합니다.

## 기능

- 기온(K), 풍향(mil), 풍속(kt), 지위고도(gpm)를 기압(hPa)에 따라 표시합니다.
- 라디오존데 관측은 빨간색, GFS는 파란색, KIM은 초록색으로 표시합니다.
- 선택한 관측소 좌표로 KIM API에 조회하고 U·V 성분에서 풍향과 풍속을 계산합니다.

## 사용법

1. Python 환경에 필요한 패키지를 설치합니다.

   ```powershell
   python -m pip install matplotlib pandas numpy pygrib
   ```

2. 다음 입력 파일을 준비해 프로젝트 폴더에 둡니다. 다른 파일을 사용하려면 해당 소스의 파일명 자리에 실제 파일 경로를 입력하세요. Windows 전체 경로는 `C:/data/파일명.xls`처럼 적을 수 있습니다.

   | 파일 | 용도 |
   | --- | --- |
   | `gfs.t00z.pgrb2.0p25.f000` | GFS 등압면 자료 (`gfs_data2.py`) |
   | `OBS_SONDE_F00508_20261122154830.xls` | 라디오존데 관측 자료 (`obs_sonde_data.py`, CP949 탭 구분 파일) |

3. [기상청 API허브](https://apihub.kma.go.kr/)에서 KIM 표준화 자료 조회 권한이 있는 인증키를 준비합니다. `.kma-api-key.example`을 `.kma-api-key`로 복사하고 주석 아래에 인증키 값만 한 줄로 적습니다. 환경변수 `KMA_API_KEY`로도 지정할 수 있습니다. 실제 인증키 파일과 입력 자료는 Git에서 제외됩니다.

4. 프로젝트 폴더에서 아래 명령을 실행한 뒤 목록에 나온 관측소 이름을 입력합니다.

   ```powershell
   python plot_profiles.py
   ```

기본 KIM 분석시각은 **2026-11-21 00 UTC**, 예측시간은 0시간입니다. 같은 시각의 자료를 비교하려면 관측과 GFS 파일의 시각을 확인하고 필요에 따라 `kim_data.py`의 `tmfc` 기본값을 조정하세요.

참고
https://aim.koca.go.kr/eaipPub/Package/2023-09-21/html/eAIC/AIC%205-en-GB.pdf
