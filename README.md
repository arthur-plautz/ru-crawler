# RU Crawler

Let's do this.

## Setup

### Virtual Environment
```bash
virtualenv -p python3.7 venv
source venv/bin/activate
```

### Requirements
```bash
pip install -r requirements.txt
```

## Running

Create your `.env` file based on `.env.example`, then source it.
```bash
source .env
```

Then you can run via Python like this:
```bash
python -m src.scripts.make_reservation $meal $enablescreenshot
```
Script takes two parameters:
1. The Meal (`Almoço` or `Jantar`)
2. The Screenshot Flag, that you can set to anything, if you want a image of the status report.
