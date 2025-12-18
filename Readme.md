# Craigslist "For Sale" Task Generator

## Overview

This script generates **100 curated task/URL pairs** for testing the Craigslist URL verifier. The tasks cover the **4 most complex "For Sale" subsections** on Craigslist:

1. **cars+trucks** (30 tasks) - Most filter options available
2. **motorcycles** (25 tasks)
3. **rvs+camp** (23 tasks)
4. **boats** (22 tasks)

Each task consists of a natural language search query and its corresponding ground truth URL with the correct filters applied.

---

## Prerequisites

```bash
# Python 3.7+ required
# No external dependencies needed - uses only standard library
```

---

## Quick Start

```bash
# Generate dataset with default settings (SF Bay Area)
python craigslist_100_tasks.py

# Output: dataset_100.csv
```

---

## Command Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output` | `-o` | `dataset_100.csv` | Output CSV filename |
| `--region` | `-r` | `sfbay` | Craigslist region |

### Available Regions

| Region | Location |
|--------|----------|
| `sfbay` | San Francisco, CA |
| `losangeles` | Los Angeles, CA |
| `newyork` | New York, NY |
| `seattle` | Seattle, WA |
| `chicago` | Chicago, IL |

### Examples

```bash
# Generate for Los Angeles
python craigslist_100_tasks.py --region losangeles

# Generate with custom output filename
python craigslist_100_tasks.py --output my_tasks.csv

# Generate for New York with custom filename
python craigslist_100_tasks.py -r newyork -o newyork_tasks.csv
```

---

## Output Format

The script generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `task_id` | Unique identifier (e.g., `navi_bench/craigslist/cars_trucks/0`) |
| `task_generation_config_json` | JSON config containing task, URL, ground truth URLs |
| `env` | Environment (`real`) |
| `domain` | Domain (`craigslist`) |
| `l1_category` | Level 1 category (`marketplace`) |
| `l2_category` | Level 2 category (e.g., `cars_trucks`, `motorcycles`) |
| `suggested_difficulty` | Task difficulty (`easy`, `medium`, `hard`) |
| `suggested_hint` | Hint for the task (`null`) |
| `suggested_max_steps` | Max steps (`0`) |
| `suggested_split` | Data split (`validation`) |
| `metadata_json` | Additional metadata (`null`) |

### Sample Row (JSON config expanded)

```json
{
  "_target_": "navi_bench.craigslist.craigslist_url_match.generate_task_config",
  "url": "https://sfbay.craigslist.org/search/cta",
  "task": "Find Toyota cars with images priced under $15,000.",
  "location": "San Francisco, CA, United States",
  "timezone": "America/Los_Angeles",
  "gt_urls": [["https://sfbay.craigslist.org/search/cta?auto_make_model=toyota&hasPic=1&max_price=15000#search=2~gallery~0"]]
}
```

---

## Filter Coverage

### 1. Cars + Trucks (30 tasks)

| Filter Type | Parameter | Values | Tasks |
|-------------|-----------|--------|-------|
| Make/Model | `auto_make_model` | Text search | 8 |
| Transmission | `auto_transmission` | 1=auto, 2=manual | 3 |
| Fuel Type | `auto_fuel_type` | 1=gas, 2=diesel, 3=hybrid, 4=electric | 4 |
| Body Type | `auto_bodytype` | 2=convertible, 3=coupe, 7=pickup, 8=sedan, 9=truck, 10=SUV | 4 |
| Drivetrain | `auto_drivetrain` | 1=FWD, 2=RWD, 3=4WD | 3 |
| Title Status | `srchType` / `auto_title_status` | T=clean, 2=salvage | 2 |
| Year | `min_auto_year` / `max_auto_year` | Year range | 3 |
| Mileage | `max_auto_miles` | Max odometer | 2 |
| Color | `auto_paint` | 1=black, 10=white, etc. | 2 |
| Condition | `condition` | 10=new, 20=like new, 30=excellent | - |
| Price | `min_price` / `max_price` | Price range | Most |
| Seller | `purveyor` | owner, dealer | Several |
| Sort | `sort` | priceasc, pricedesc, date | 2 |
| Has Image | `hasPic` | 1 | Most |

### 2. Motorcycles (25 tasks)

| Filter Type | Parameter | Tasks |
|-------------|-----------|-------|
| Make/Model | `auto_make_model` | 6 |
| Year Range | `min_auto_year` / `max_auto_year` | 3 |
| Mileage | `max_auto_miles` | 2 |
| Condition | `condition` | 3 |
| Type Query | `query` (sport bike, cruiser, touring, dirt bike) | 5 |
| Sorting | `sort` | 2 |
| Complex | Multiple filters | 4 |

### 3. RVs + Camp (23 tasks)

| Filter Type | Parameter | Tasks |
|-------------|-----------|-------|
| RV Type | `query` (Class A/B/C, travel trailer, fifth wheel, etc.) | 8 |
| Brand | `query` (Airstream, Winnebago, Jayco, etc.) | 5 |
| Condition | `condition` | 3 |
| Sorting | `sort` | 2 |
| Complex | Multiple filters | 5 |

### 4. Boats (22 tasks)

| Filter Type | Parameter | Tasks |
|-------------|-----------|-------|
| Boat Type | `query` (fishing, sailboat, pontoon, bass boat, etc.) | 8 |
| Small Watercraft | `query` (kayak, canoe, jet ski, paddleboard) | 4 |
| Brand | `query` (Boston Whaler, Sea Ray, Bayliner) | 3 |
| Condition | `condition` | 2 |
| Sorting | `sort` | 2 |
| Complex | Multiple filters | 3 |

---

## Difficulty Distribution

| Difficulty | Count | Percentage | Criteria |
|------------|-------|------------|----------|
| Easy | 1 | 1% | Single basic filter |
| Medium | 32 | 32% | 2-3 filters, common combinations |
| Hard | 67 | 67% | 3+ filters, complex combinations |

---

## Integration with navi_bench

This dataset is designed to work with the existing Craigslist URL verifier:

```
navi_bench/craigslist/craigslist_url_match.py
```

### Usage in navi_bench

```python
from navi_bench.base import DatasetItem, instantiate
import pandas as pd

# Load the dataset
df = pd.read_csv("dataset_100.csv")

# Process each row
for _, row in df.iterrows():
    dataset_item = DatasetItem.model_validate(row.to_dict())
    task_config = dataset_item.generate_task_config()
    evaluator = instantiate(task_config.eval_config)
    
    # Use evaluator to verify agent's URL matches ground truth
    await evaluator.update(url=agent_generated_url)
    result = await evaluator.compute()
    print(f"Score: {result.score}")  # 1.0 = match, 0.0 = no match
```

---

## URL Structure Reference

### Base URLs by Category

| Category | URL Code | Base URL |
|----------|----------|----------|
| Cars + Trucks | `cta` | `https://{region}.craigslist.org/search/cta` |
| Motorcycles | `mca` | `https://{region}.craigslist.org/search/mca` |
| RVs + Camp | `rva` | `https://{region}.craigslist.org/search/rva` |
| Boats | `boa` | `https://{region}.craigslist.org/search/boa` |

### URL Format

```
https://{region}.craigslist.org/search/{category_code}?{params}#search=2~gallery~0
```

### Example URLs

```
# Cars: Toyota under $15,000 with images
https://sfbay.craigslist.org/search/cta?auto_make_model=toyota&hasPic=1&max_price=15000#search=2~gallery~0

# Motorcycles: Harley-Davidson from owners
https://sfbay.craigslist.org/search/mca?auto_make_model=harley&purveyor=owner#search=2~gallery~0

# RVs: Class A motorhomes under $60,000
https://sfbay.craigslist.org/search/rva?query=class%20a%20motorhome&hasPic=1&max_price=60000#search=2~gallery~0

# Boats: Fishing boats under $18,000
https://sfbay.craigslist.org/search/boa?query=fishing%20boat&hasPic=1&max_price=18000#search=2~gallery~0
```

---

## File Structure

```
.
├── craigslist_100_tasks.py    # Main generator script
├── dataset_100.csv            # Generated dataset (100 tasks)
└── README.md                  # This documentation
```

---

## Extending the Script

### Adding New Tasks

Edit the task lists in the generator functions:

```python
def generate_cars_trucks_tasks(region: str) -> List[TaskConfig]:
    car_tasks = [
        {
            "task": "Your natural language task description",
            "params": {"param1": "value1", "param2": "value2"},
            "difficulty": "easy|medium|hard"
        },
        # ... more tasks
    ]
```

### Adding New Regions

Add to the `REGIONS` dictionary:

```python
REGIONS = {
    "newregion": {
        "url_prefix": "https://newregion.craigslist.org",
        "location": "City, State, Country",
        "timezone": "America/Timezone"
    },
    # ...
}
```

---

## Validation

The script automatically validates that exactly 100 tasks are generated:

```python
assert len(all_tasks) == 100, f"Expected 100 tasks, got {len(all_tasks)}"
```

All URLs are programmatically generated using the `build_url()` function, ensuring consistent formatting and proper URL encoding.

---

## License

Part of the navi_bench project.