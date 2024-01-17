# Requirements

## Python 
Install latest python version from [here](https://www.python.org/downloads/)

## Virtual Environment
Create a virtual environment to isolate the project's dependencies. You can use `venv` or `conda` to do this. Here's how you can create a virtual environment using `venv`:

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

## Dependencies
Install dependencies using pip

```bash
pip install scrapy scrapy_splash
```

## Run scraper
If you encounter issues installing Scrapy, refer to the Scrapy [installation guide](https://docs.scrapy.org/en/latest/intro/install.html#intro-install-platform-notes).

```bash
git clone https://github.com/xkazm04/vesting-sc
```
```bash
cd vesting-sc
cd sc
```

Export generates csv file
```bash
scrapy crawl bsc -O vesting.csv
```