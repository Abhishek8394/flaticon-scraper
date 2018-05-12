# Introduction

Fetch icons from [Flaticon website](https://www.flaticon.com/)

## Setup

Run following command to setup dependecies, using a virtual environment or conda environment is recommended.

```bash
python -r requirements.txt
```

## Usage

#### 1. Fetch icons and save

In a file write your search terms, separated by new line. Refer to `example.txt` 

Run the following command

```bash
python icons_fetcher.py --inp-file example.txt --out-dir saved_images
```

```bash
usage: icons_fetcher.py [-h] --inp-file INP_FILE [--out-dir OUT_DIR]

optional arguments:
  -h, --help           show this help message and exit
  --inp-file INP_FILE  File containing search terms
  --out-dir OUT_DIR    Output directory
```