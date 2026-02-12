## Your GitHub Learning Lab Repository for Intro to HTML

Welcome to your repository for your GitHub Learning Lab course. This repository will be used during the different activities that I will be guiding you through.

Oh! I haven't introduced myself...

I'm the GitHub Learning Lab bot and I'm here to help guide you in your journey to learn and master the various topics covered in this course. I will be using Issue and Pull Request comments to communicate with you. In fact, I already added an issue for you to check out.

![issue tab](https://lab.github.com/public/images/issue_tab.png)

I'll meet you over there, can't wait to get started!

This repository is licensed under [MIT](LICENSE) (c) 2019 GitHub, Inc.
Photo by [Kelli Tungay](https://unsplash.com/photos/Sj0nhVIb4eY) on [Unsplash](https://unsplash.com/)

## ERA5/ERA5-LAND 下载脚本（2021-2025）

仓库新增脚本 `download_era5_2021_2025.py`，用于下载你现有文件对应的 2021-2025 数据：

- `ERA5_daily_tmin_<year>.nc`
- `ERA5_daily_tmax_<year>.nc`
- `ERA5_daily_pr_<year>.nc`
- `ERA5_month_t2m_2021_2025.nc`
- `ERA5_month_tp_2021_2025.nc`
- `ERA5_annual_t2m_tp_<year>.nc`

### 使用方法

```bash
pip install cdsapi
python download_era5_2021_2025.py
```

> 运行前请确保你已配置 `~/.cdsapirc`（Copernicus CDS API key）。
