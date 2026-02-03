[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/7ws4c2Dp)
# Food Project

<img src="figures/DS205_2526WT_favicon_128px.png" alt="DS205 Banner" width="128px" style="display:inline-block;vertical-align:middle;border-radius:50%;box-shadow:0 2px 8px 0 rgba(24, 24, 32, 0.13);margin-bottom:1em;" />

**Note:** This is a student repository for DS205 Problem Set 1. See the [assignment page](https://lse-dsi.github.io/DS205/2025-2026/winter-term/assessments/problem-set-1.html) for full instructions.

**AUTHOR:** [YOUR NAME](https://github.com/<your-github-username>)

## Project Structure

```
├── scraper/           # Your web scraper (Part A)
│   └── README.md
├── api/               # Your FastAPI application (Part B)
│   └── README.md
├── data/
│   ├── raw/           # Scraped data
│   └── processed/     # Enriched data with NOVA classifications
├── environment.yml
├── CONTRIBUTING.md
└── README.md
```

## Environment Setup

Create the conda environment:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate food
```

If `environment.yml` changes, update your environment:

```bash
conda env update -f environment.yml --prune
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for collaboration guidelines developed during the course.
