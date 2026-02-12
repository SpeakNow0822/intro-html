"""下载 ERA5/ERA5-LAND 2021-2025 年数据。

用途：
1) 下载与已有文件一致的 ERA5-LAND 日尺度变量（tmin/tmax/pr），按年份输出：
   - ERA5_daily_tmin_<year>.nc
   - ERA5_daily_tmax_<year>.nc
   - ERA5_daily_pr_<year>.nc
2) 下载 t2m/tp 的月尺度数据（2021-2025）：
   - ERA5_month_t2m_2021_2025.nc
   - ERA5_month_tp_2021_2025.nc
3) 额外按年输出 t2m+tp（如你已有 ERA5_annual_t2m_tp_2020.nc 的命名方式）：
   - ERA5_annual_t2m_tp_<year>.nc

使用前准备：
- pip install cdsapi
- 配置 ~/.cdsapirc（Copernicus Climate Data Store API key）
- 如需限制区域，请修改 AREA；若为 None 则下载全球。
"""

from __future__ import annotations

from pathlib import Path

import cdsapi

# 下载年份
YEARS = [str(y) for y in range(2021, 2026)]

# 输出目录
OUT_DIR = Path("data_2021_2025")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 区域 [North, West, South, East]
# 例如中国可用 [55, 70, 15, 140]
AREA = None

MONTHS = [f"{m:02d}" for m in range(1, 13)]
DAYS = [f"{d:02d}" for d in range(1, 32)]
TIME = ["00:00"]



def with_area(request: dict) -> dict:
    """按需附加 area 参数。"""
    if AREA is not None:
        request["area"] = AREA
    return request



def download_daily_variable(
    client: cdsapi.Client,
    variable: str,
    short_name: str,
    daily_statistic: str,
) -> None:
    """下载 ERA5-LAND 日统计变量，按年输出。"""
    for year in YEARS:
        target = OUT_DIR / f"ERA5_daily_{short_name}_{year}.nc"
        request = with_area(
            {
                "variable": variable,
                "year": year,
                "month": MONTHS,
                "day": DAYS,
                "daily_statistic": daily_statistic,
                "time_zone": "utc+00:00",
                "frequency": "1_hourly",
            }
        )
        print(f"Downloading {target.name} ...")
        client.retrieve("derived-era5-land-daily-statistics", request, str(target))



def download_monthly_t2m_tp(client: cdsapi.Client) -> None:
    """下载 2021-2025 的月尺度 t2m / tp（分别成文件）。"""
    base_request = with_area(
        {
            "product_type": "monthly_averaged_reanalysis",
            "year": YEARS,
            "month": MONTHS,
            "time": TIME,
            "data_format": "netcdf",
            "download_format": "unarchived",
        }
    )

    t2m_request = dict(base_request)
    t2m_request["variable"] = "2m_temperature"
    t2m_target = OUT_DIR / "ERA5_month_t2m_2021_2025.nc"
    print(f"Downloading {t2m_target.name} ...")
    client.retrieve("reanalysis-era5-land-monthly-means", t2m_request, str(t2m_target))

    tp_request = dict(base_request)
    tp_request["variable"] = "total_precipitation"
    tp_target = OUT_DIR / "ERA5_month_tp_2021_2025.nc"
    print(f"Downloading {tp_target.name} ...")
    client.retrieve("reanalysis-era5-land-monthly-means", tp_request, str(tp_target))



def download_annual_like_t2m_tp(client: cdsapi.Client) -> None:
    """按年输出 t2m+tp（月平均集合），文件名对齐 ERA5_annual_t2m_tp_<year>.nc。"""
    for year in YEARS:
        target = OUT_DIR / f"ERA5_annual_t2m_tp_{year}.nc"
        request = with_area(
            {
                "product_type": "monthly_averaged_reanalysis",
                "variable": ["2m_temperature", "total_precipitation"],
                "year": year,
                "month": MONTHS,
                "time": TIME,
                "data_format": "netcdf",
                "download_format": "unarchived",
            }
        )
        print(f"Downloading {target.name} ...")
        client.retrieve("reanalysis-era5-land-monthly-means", request, str(target))



def main() -> None:
    client = cdsapi.Client()

    # 1) 先下载日尺度（与已有 daily 文件对应）
    download_daily_variable(client, "2m_temperature", "tmin", "daily_minimum")
    download_daily_variable(client, "2m_temperature", "tmax", "daily_maximum")
    download_daily_variable(client, "total_precipitation", "pr", "daily_sum")

    # 2) 下载月尺度 2021-2025（与 month_t2m/tp 文件对应）
    download_monthly_t2m_tp(client)

    # 3) 额外按年生成 t2m+tp（与 annual_t2m_tp_<year> 命名对应）
    download_annual_like_t2m_tp(client)

    print("Done. All requested files are queued/downloaded.")


if __name__ == "__main__":
    main()
