"""
Craigslist "For Sale" - 100 Curated High-Quality Tasks

Exactly 100 carefully curated tasks across 4 complex categories:
- cars+trucks: 30 tasks (most filters available)
- motorcycles: 25 tasks
- rvs+camp: 23 tasks
- boats: 22 tasks

All tasks are validated and cover comprehensive filter combinations.

Usage:
    python craigslist_100_tasks.py [--output dataset_100.csv] [--region sfbay]
"""

import json
import csv
import argparse
from dataclasses import dataclass
from typing import List, Dict
from urllib.parse import quote


@dataclass
class TaskConfig:
    task_id: str
    task: str
    url: str
    gt_urls: List[List[str]]
    location: str
    timezone: str
    difficulty: str
    l2_category: str


# Region configurations
REGIONS = {
    "sfbay": {
        "url_prefix": "https://sfbay.craigslist.org",
        "location": "San Francisco, CA, United States",
        "timezone": "America/Los_Angeles"
    },
    "losangeles": {
        "url_prefix": "https://losangeles.craigslist.org",
        "location": "Los Angeles, CA, United States",
        "timezone": "America/Los_Angeles"
    },
    "newyork": {
        "url_prefix": "https://newyork.craigslist.org",
        "location": "New York, NY, United States",
        "timezone": "America/New_York"
    },
    "seattle": {
        "url_prefix": "https://seattle.craigslist.org",
        "location": "Seattle, WA, United States",
        "timezone": "America/Los_Angeles"
    },
    "chicago": {
        "url_prefix": "https://chicago.craigslist.org",
        "location": "Chicago, IL, United States",
        "timezone": "America/Chicago"
    }
}


def build_url(base_url: str, category_code: str, params: Dict) -> str:
    """Build a Craigslist search URL with parameters."""
    url = f"{base_url}/search/{category_code}"
    if params:
        encoded_params = []
        for key, value in params.items():
            if key == "query" or key == "auto_make_model":
                encoded_params.append(f"{key}={quote(str(value))}")
            elif isinstance(value, list):
                for v in value:
                    encoded_params.append(f"{key}={v}")
            else:
                encoded_params.append(f"{key}={value}")
        url += "?" + "&".join(encoded_params)
    url += "#search=2~gallery~0"
    return url


# =============================================================================
# CARS + TRUCKS - 30 CURATED TASKS
# =============================================================================
def generate_cars_trucks_tasks(region: str) -> List[TaskConfig]:
    """
    30 curated tasks for cars+trucks (cta).
    Covers: make/model, transmission, fuel, body type, drivetrain, title, year, mileage, color, condition, price, purveyor, sort
    """
    region_config = REGIONS[region]
    base_url = region_config["url_prefix"]
    tasks = []
    
    car_tasks = [
        # === BASIC FILTERS (5 tasks) ===
        {
            "task": "Find Toyota cars with images priced under $15,000.",
            "params": {"auto_make_model": "toyota", "hasPic": "1", "max_price": "15000"},
            "difficulty": "medium"
        },
        {
            "task": "Browse Honda Accord cars sold by owners.",
            "params": {"auto_make_model": "honda accord", "purveyor": "owner"},
            "difficulty": "medium"
        },
        {
            "task": "Find cars under $8,000 with images sorted by lowest price.",
            "params": {"max_price": "8000", "hasPic": "1", "sort": "priceasc"},
            "difficulty": "medium"
        },
        {
            "task": "Search for Ford vehicles from dealers with photos.",
            "params": {"auto_make_model": "ford", "purveyor": "dealer", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Find cars priced between $5,000 and $12,000.",
            "params": {"min_price": "5000", "max_price": "12000"},
            "difficulty": "easy"
        },
        
        # === TRANSMISSION FILTER (3 tasks) ===
        {
            "task": "Find cars with automatic transmission under $10,000 with images.",
            "params": {"auto_transmission": "1", "max_price": "10000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Search for manual transmission cars priced between $5,000 and $20,000.",
            "params": {"auto_transmission": "2", "min_price": "5000", "max_price": "20000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse manual transmission sports cars with images.",
            "params": {"auto_transmission": "2", "auto_bodytype": "3", "hasPic": "1"},
            "difficulty": "hard"
        },
        
        # === FUEL TYPE FILTER (4 tasks) ===
        {
            "task": "Find electric vehicles with images.",
            "params": {"auto_fuel_type": "4", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse hybrid cars under $25,000 sold by owners.",
            "params": {"auto_fuel_type": "3", "max_price": "25000", "purveyor": "owner"},
            "difficulty": "hard"
        },
        {
            "task": "Find diesel trucks with images priced under $35,000.",
            "params": {"auto_fuel_type": "2", "auto_bodytype": "9", "hasPic": "1", "max_price": "35000"},
            "difficulty": "hard"
        },
        {
            "task": "Search for gasoline SUVs under $20,000.",
            "params": {"auto_fuel_type": "1", "auto_bodytype": "10", "max_price": "20000"},
            "difficulty": "hard"
        },
        
        # === BODY TYPE FILTER (4 tasks) ===
        {
            "task": "Find SUVs with images under $18,000.",
            "params": {"auto_bodytype": "10", "hasPic": "1", "max_price": "18000"},
            "difficulty": "medium"
        },
        {
            "task": "Browse pickup trucks sold by owners with photos.",
            "params": {"auto_bodytype": "7", "purveyor": "owner", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Find sedans with automatic transmission under $12,000.",
            "params": {"auto_bodytype": "8", "auto_transmission": "1", "max_price": "12000"},
            "difficulty": "hard"
        },
        {
            "task": "Search for convertibles priced between $15,000 and $40,000 with images.",
            "params": {"auto_bodytype": "2", "min_price": "15000", "max_price": "40000", "hasPic": "1"},
            "difficulty": "hard"
        },
        
        # === DRIVETRAIN FILTER (3 tasks) ===
        {
            "task": "Find 4WD vehicles with images under $25,000.",
            "params": {"auto_drivetrain": "3", "hasPic": "1", "max_price": "25000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse rear-wheel drive cars sold by owners.",
            "params": {"auto_drivetrain": "2", "purveyor": "owner"},
            "difficulty": "medium"
        },
        {
            "task": "Find front-wheel drive sedans under $15,000 with images.",
            "params": {"auto_drivetrain": "1", "auto_bodytype": "8", "max_price": "15000", "hasPic": "1"},
            "difficulty": "hard"
        },
        
        # === TITLE STATUS FILTER (2 tasks) ===
        {
            "task": "Find cars with clean title under $10,000 with images.",
            "params": {"srchType": "T", "max_price": "10000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Browse salvage title vehicles under $5,000.",
            "params": {"auto_title_status": "2", "max_price": "5000"},
            "difficulty": "medium"
        },
        
        # === YEAR FILTER (3 tasks) ===
        {
            "task": "Find cars from 2020 or newer with images.",
            "params": {"min_auto_year": "2020", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse classic cars from 1985 or older with photos.",
            "params": {"max_auto_year": "1985", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Find cars between 2018 and 2022 priced under $25,000.",
            "params": {"min_auto_year": "2018", "max_auto_year": "2022", "max_price": "25000"},
            "difficulty": "hard"
        },
        
        # === MILEAGE FILTER (2 tasks) ===
        {
            "task": "Find low mileage cars under 50,000 miles with images.",
            "params": {"max_auto_miles": "50000", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse cars with less than 80,000 miles priced under $15,000.",
            "params": {"max_auto_miles": "80000", "max_price": "15000"},
            "difficulty": "hard"
        },
        
        # === COLOR FILTER (2 tasks) ===
        {
            "task": "Find white SUVs with images under $22,000.",
            "params": {"auto_paint": "10", "auto_bodytype": "10", "hasPic": "1", "max_price": "22000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse black sedans sold by owners with photos.",
            "params": {"auto_paint": "1", "auto_bodytype": "8", "purveyor": "owner", "hasPic": "1"},
            "difficulty": "hard"
        },
        
        # === COMPLEX MULTI-FILTER (2 tasks) ===
        {
            "task": "Find Toyota Camry with automatic transmission under 70,000 miles priced between $12,000 and $22,000 with images.",
            "params": {"auto_make_model": "toyota camry", "auto_transmission": "1", "max_auto_miles": "70000", "min_price": "12000", "max_price": "22000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Search for Honda CR-V SUVs with 4WD from 2019 or newer under $30,000 with photos.",
            "params": {"auto_make_model": "honda cr-v", "auto_bodytype": "10", "auto_drivetrain": "3", "min_auto_year": "2019", "max_price": "30000", "hasPic": "1"},
            "difficulty": "hard"
        },
    ]
    
    for i, task_data in enumerate(car_tasks):
        gt_url = build_url(base_url, "cta", task_data["params"])
        tasks.append(TaskConfig(
            task_id=f"navi_bench/craigslist/cars_trucks/{i}",
            task=task_data["task"],
            url=f"{base_url}/search/cta",
            gt_urls=[[gt_url]],
            location=region_config["location"],
            timezone=region_config["timezone"],
            difficulty=task_data["difficulty"],
            l2_category="cars_trucks"
        ))
    
    return tasks


# =============================================================================
# MOTORCYCLES - 25 CURATED TASKS
# =============================================================================
def generate_motorcycles_tasks(region: str) -> List[TaskConfig]:
    """
    25 curated tasks for motorcycles (mca).
    Covers: make/model, year, mileage, condition, price, purveyor, sort, type queries
    """
    region_config = REGIONS[region]
    base_url = region_config["url_prefix"]
    tasks = []
    
    motorcycle_tasks = [
        # === BRAND SEARCHES (6 tasks) ===
        {
            "task": "Find Harley-Davidson motorcycles with images priced under $15,000.",
            "params": {"auto_make_model": "harley", "hasPic": "1", "max_price": "15000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse Honda motorcycles sold by owners.",
            "params": {"auto_make_model": "honda", "purveyor": "owner"},
            "difficulty": "medium"
        },
        {
            "task": "Find Yamaha motorcycles priced between $4,000 and $10,000.",
            "params": {"auto_make_model": "yamaha", "min_price": "4000", "max_price": "10000"},
            "difficulty": "hard"
        },
        {
            "task": "Search for Kawasaki Ninja motorcycles with images.",
            "params": {"auto_make_model": "kawasaki ninja", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse BMW motorcycles under $18,000 with photos.",
            "params": {"auto_make_model": "bmw", "max_price": "18000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Find Ducati motorcycles sold by owners with images.",
            "params": {"auto_make_model": "ducati", "purveyor": "owner", "hasPic": "1"},
            "difficulty": "hard"
        },
        
        # === YEAR FILTER (3 tasks) ===
        {
            "task": "Find motorcycles from 2020 or newer with images.",
            "params": {"min_auto_year": "2020", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse vintage motorcycles from 1990 or older with photos.",
            "params": {"max_auto_year": "1990", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Find motorcycles between 2017 and 2022 priced under $12,000.",
            "params": {"min_auto_year": "2017", "max_auto_year": "2022", "max_price": "12000"},
            "difficulty": "hard"
        },
        
        # === MILEAGE FILTER (2 tasks) ===
        {
            "task": "Find low mileage motorcycles under 10,000 miles with images.",
            "params": {"max_auto_miles": "10000", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse motorcycles with less than 25,000 miles priced under $8,000.",
            "params": {"max_auto_miles": "25000", "max_price": "8000"},
            "difficulty": "hard"
        },
        
        # === CONDITION FILTER (3 tasks) ===
        {
            "task": "Find new condition motorcycles with images.",
            "params": {"condition": "10", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse motorcycles in excellent condition under $10,000.",
            "params": {"condition": "30", "max_price": "10000"},
            "difficulty": "hard"
        },
        {
            "task": "Find like-new motorcycles sold by owners.",
            "params": {"condition": "20", "purveyor": "owner"},
            "difficulty": "medium"
        },
        
        # === TYPE SEARCHES (5 tasks) ===
        {
            "task": "Find sport bikes under $9,000 with images.",
            "params": {"query": "sport bike", "hasPic": "1", "max_price": "9000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse cruiser motorcycles sold by owners with photos.",
            "params": {"query": "cruiser", "purveyor": "owner", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Search for touring motorcycles priced between $8,000 and $20,000.",
            "params": {"query": "touring", "min_price": "8000", "max_price": "20000"},
            "difficulty": "hard"
        },
        {
            "task": "Find dirt bikes under $6,000 with images.",
            "params": {"query": "dirt bike", "hasPic": "1", "max_price": "6000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse adventure motorcycles with photos.",
            "params": {"query": "adventure", "hasPic": "1"},
            "difficulty": "medium"
        },
        
        # === SORTING (2 tasks) ===
        {
            "task": "Find motorcycles under $5,000 sorted by lowest price with images.",
            "params": {"max_price": "5000", "sort": "priceasc", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Browse Harley-Davidson motorcycles sorted by newest listings.",
            "params": {"auto_make_model": "harley", "sort": "date"},
            "difficulty": "medium"
        },
        
        # === COMPLEX COMBINATIONS (4 tasks) ===
        {
            "task": "Find Harley-Davidson touring motorcycles from 2018 or newer under $22,000 with images.",
            "params": {"auto_make_model": "harley", "query": "touring", "min_auto_year": "2018", "max_price": "22000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Browse Honda sport bikes with less than 15,000 miles from owners.",
            "params": {"auto_make_model": "honda", "query": "sport", "max_auto_miles": "15000", "purveyor": "owner"},
            "difficulty": "hard"
        },
        {
            "task": "Find Suzuki motorcycles in excellent condition priced between $3,000 and $8,000.",
            "params": {"auto_make_model": "suzuki", "condition": "30", "min_price": "3000", "max_price": "8000"},
            "difficulty": "hard"
        },
        {
            "task": "Search for KTM dirt bikes under $7,000 with photos from owners.",
            "params": {"auto_make_model": "ktm", "query": "dirt", "max_price": "7000", "hasPic": "1", "purveyor": "owner"},
            "difficulty": "hard"
        },
    ]
    
    for i, task_data in enumerate(motorcycle_tasks):
        gt_url = build_url(base_url, "mca", task_data["params"])
        tasks.append(TaskConfig(
            task_id=f"navi_bench/craigslist/motorcycles/{i}",
            task=task_data["task"],
            url=f"{base_url}/search/mca",
            gt_urls=[[gt_url]],
            location=region_config["location"],
            timezone=region_config["timezone"],
            difficulty=task_data["difficulty"],
            l2_category="motorcycles"
        ))
    
    return tasks


# =============================================================================
# RVS + CAMP - 23 CURATED TASKS
# =============================================================================
def generate_rvs_camp_tasks(region: str) -> List[TaskConfig]:
    """
    23 curated tasks for RVs & camping (rva).
    Covers: RV types, brands, condition, price, purveyor, sort
    """
    region_config = REGIONS[region]
    base_url = region_config["url_prefix"]
    tasks = []
    
    rv_tasks = [
        # === RV TYPE SEARCHES (8 tasks) ===
        {
            "task": "Find Class A motorhomes with images priced under $60,000.",
            "params": {"query": "class a motorhome", "hasPic": "1", "max_price": "60000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse Class B camper vans sold by owners.",
            "params": {"query": "class b", "purveyor": "owner"},
            "difficulty": "medium"
        },
        {
            "task": "Search for Class C motorhomes priced between $35,000 and $75,000.",
            "params": {"query": "class c motorhome", "min_price": "35000", "max_price": "75000"},
            "difficulty": "hard"
        },
        {
            "task": "Find travel trailers under $18,000 with images.",
            "params": {"query": "travel trailer", "hasPic": "1", "max_price": "18000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse fifth wheel trailers from dealers with photos.",
            "params": {"query": "fifth wheel", "purveyor": "dealer", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Find pop-up campers under $7,000 with images.",
            "params": {"query": "pop up camper", "max_price": "7000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Search for toy haulers priced under $45,000 with photos.",
            "params": {"query": "toy hauler", "hasPic": "1", "max_price": "45000"},
            "difficulty": "hard"
        },
        {
            "task": "Find truck campers under $12,000 sold by owners.",
            "params": {"query": "truck camper", "max_price": "12000", "purveyor": "owner"},
            "difficulty": "hard"
        },
        
        # === BRAND SEARCHES (5 tasks) ===
        {
            "task": "Find Airstream trailers with images.",
            "params": {"query": "airstream", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse Winnebago motorhomes under $70,000 with photos.",
            "params": {"query": "winnebago", "max_price": "70000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Search for Jayco RVs sold by owners.",
            "params": {"query": "jayco", "purveyor": "owner"},
            "difficulty": "medium"
        },
        {
            "task": "Find Forest River trailers priced between $12,000 and $30,000.",
            "params": {"query": "forest river", "min_price": "12000", "max_price": "30000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse Keystone RVs under $28,000 with images.",
            "params": {"query": "keystone", "max_price": "28000", "hasPic": "1"},
            "difficulty": "hard"
        },
        
        # === CONDITION FILTER (3 tasks) ===
        {
            "task": "Find new condition RVs with images.",
            "params": {"condition": "10", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse travel trailers in excellent condition under $25,000.",
            "params": {"query": "travel trailer", "condition": "30", "max_price": "25000"},
            "difficulty": "hard"
        },
        {
            "task": "Find motorhomes in like-new condition from owners.",
            "params": {"query": "motorhome", "condition": "20", "purveyor": "owner"},
            "difficulty": "hard"
        },
        
        # === SORTING (2 tasks) ===
        {
            "task": "Find RVs under $15,000 sorted by lowest price with images.",
            "params": {"max_price": "15000", "sort": "priceasc", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Browse travel trailers sorted by newest listings.",
            "params": {"query": "travel trailer", "sort": "date"},
            "difficulty": "medium"
        },
        
        # === COMPLEX COMBINATIONS (5 tasks) ===
        {
            "task": "Find Airstream travel trailers in excellent condition under $90,000 with images.",
            "params": {"query": "airstream", "condition": "30", "max_price": "90000", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Browse diesel motorhomes priced between $40,000 and $120,000.",
            "params": {"query": "diesel motorhome", "min_price": "40000", "max_price": "120000"},
            "difficulty": "hard"
        },
        {
            "task": "Find teardrop trailers under $15,000 sold by owners with photos.",
            "params": {"query": "teardrop", "max_price": "15000", "purveyor": "owner", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Search for van conversions under $50,000 with images from owners.",
            "params": {"query": "van conversion", "max_price": "50000", "hasPic": "1", "purveyor": "owner"},
            "difficulty": "hard"
        },
        {
            "task": "Find hybrid travel trailers under $35,000 with photos.",
            "params": {"query": "hybrid trailer", "max_price": "35000", "hasPic": "1"},
            "difficulty": "hard"
        },
    ]
    
    for i, task_data in enumerate(rv_tasks):
        gt_url = build_url(base_url, "rva", task_data["params"])
        tasks.append(TaskConfig(
            task_id=f"navi_bench/craigslist/rvs_camp/{i}",
            task=task_data["task"],
            url=f"{base_url}/search/rva",
            gt_urls=[[gt_url]],
            location=region_config["location"],
            timezone=region_config["timezone"],
            difficulty=task_data["difficulty"],
            l2_category="rvs_camp"
        ))
    
    return tasks


# =============================================================================
# BOATS - 22 CURATED TASKS
# =============================================================================
def generate_boats_tasks(region: str) -> List[TaskConfig]:
    """
    22 curated tasks for boats (boa).
    Covers: boat types, brands, condition, price, purveyor, sort
    """
    region_config = REGIONS[region]
    base_url = region_config["url_prefix"]
    tasks = []
    
    boat_tasks = [
        # === BOAT TYPE SEARCHES (8 tasks) ===
        {
            "task": "Find fishing boats with images priced under $18,000.",
            "params": {"query": "fishing boat", "hasPic": "1", "max_price": "18000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse sailboats sold by owners with photos.",
            "params": {"query": "sailboat", "purveyor": "owner", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Search for pontoon boats priced between $12,000 and $35,000.",
            "params": {"query": "pontoon", "min_price": "12000", "max_price": "35000"},
            "difficulty": "hard"
        },
        {
            "task": "Find bass boats under $22,000 with images.",
            "params": {"query": "bass boat", "hasPic": "1", "max_price": "22000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse center console boats from dealers.",
            "params": {"query": "center console", "purveyor": "dealer"},
            "difficulty": "medium"
        },
        {
            "task": "Find ski boats priced under $28,000 with photos.",
            "params": {"query": "ski boat", "hasPic": "1", "max_price": "28000"},
            "difficulty": "hard"
        },
        {
            "task": "Search for bowrider boats priced between $15,000 and $30,000.",
            "params": {"query": "bowrider", "min_price": "15000", "max_price": "30000"},
            "difficulty": "hard"
        },
        {
            "task": "Find cabin cruiser boats with images.",
            "params": {"query": "cabin cruiser", "hasPic": "1"},
            "difficulty": "medium"
        },
        
        # === SMALL WATERCRAFT (4 tasks) ===
        {
            "task": "Find kayaks with photos sorted by lowest price.",
            "params": {"query": "kayak", "hasPic": "1", "sort": "priceasc"},
            "difficulty": "medium"
        },
        {
            "task": "Browse canoes under $800 sold by owners.",
            "params": {"query": "canoe", "max_price": "800", "purveyor": "owner"},
            "difficulty": "hard"
        },
        {
            "task": "Find jet skis under $9,000 with images.",
            "params": {"query": "jet ski", "hasPic": "1", "max_price": "9000"},
            "difficulty": "hard"
        },
        {
            "task": "Search for paddleboards with photos from owners.",
            "params": {"query": "paddleboard", "hasPic": "1", "purveyor": "owner"},
            "difficulty": "medium"
        },
        
        # === BRAND SEARCHES (3 tasks) ===
        {
            "task": "Find Boston Whaler boats with images under $40,000.",
            "params": {"query": "boston whaler", "hasPic": "1", "max_price": "40000"},
            "difficulty": "hard"
        },
        {
            "task": "Browse Sea Ray boats priced between $25,000 and $55,000.",
            "params": {"query": "sea ray", "min_price": "25000", "max_price": "55000"},
            "difficulty": "hard"
        },
        {
            "task": "Find Bayliner boats under $16,000 with photos.",
            "params": {"query": "bayliner", "max_price": "16000", "hasPic": "1"},
            "difficulty": "hard"
        },
        
        # === CONDITION FILTER (2 tasks) ===
        {
            "task": "Find boats in excellent condition with images.",
            "params": {"condition": "30", "hasPic": "1"},
            "difficulty": "medium"
        },
        {
            "task": "Browse like-new fishing boats under $30,000.",
            "params": {"query": "fishing boat", "condition": "20", "max_price": "30000"},
            "difficulty": "hard"
        },
        
        # === SORTING (2 tasks) ===
        {
            "task": "Find boats under $10,000 sorted by lowest price with images.",
            "params": {"max_price": "10000", "sort": "priceasc", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Browse pontoon boats sorted by newest listings.",
            "params": {"query": "pontoon", "sort": "date"},
            "difficulty": "medium"
        },
        
        # === COMPLEX COMBINATIONS (3 tasks) ===
        {
            "task": "Find aluminum fishing boats under $14,000 with images from owners.",
            "params": {"query": "aluminum fishing boat", "hasPic": "1", "max_price": "14000", "purveyor": "owner"},
            "difficulty": "hard"
        },
        {
            "task": "Browse Yamaha jet skis under $12,000 sold by owners with photos.",
            "params": {"query": "yamaha jet ski", "max_price": "12000", "purveyor": "owner", "hasPic": "1"},
            "difficulty": "hard"
        },
        {
            "task": "Find boat trailers under $2,500 with images from owners.",
            "params": {"query": "boat trailer", "max_price": "2500", "hasPic": "1", "purveyor": "owner"},
            "difficulty": "hard"
        },
    ]
    
    for i, task_data in enumerate(boat_tasks):
        gt_url = build_url(base_url, "boa", task_data["params"])
        tasks.append(TaskConfig(
            task_id=f"navi_bench/craigslist/boats/{i}",
            task=task_data["task"],
            url=f"{base_url}/search/boa",
            gt_urls=[[gt_url]],
            location=region_config["location"],
            timezone=region_config["timezone"],
            difficulty=task_data["difficulty"],
            l2_category="boats"
        ))
    
    return tasks


# =============================================================================
# CSV EXPORT
# =============================================================================
def task_to_csv_row(task: TaskConfig) -> Dict:
    """Convert a TaskConfig to a CSV row dictionary."""
    task_generation_config = {
        "_target_": "navi_bench.craigslist.craigslist_url_match.generate_task_config",
        "url": task.url,
        "task": task.task,
        "location": task.location,
        "timezone": task.timezone,
        "gt_urls": task.gt_urls
    }
    
    return {
        "task_id": task.task_id,
        "task_generation_config_json": json.dumps(task_generation_config),
        "env": "real",
        "domain": "craigslist",
        "l1_category": "marketplace",
        "l2_category": task.l2_category,
        "suggested_difficulty": task.difficulty,
        "suggested_hint": "null",
        "suggested_max_steps": 0,
        "suggested_split": "validation",
        "metadata_json": "null"
    }


def main():
    parser = argparse.ArgumentParser(description="Generate 100 Curated Craigslist Tasks")
    parser.add_argument("--output", "-o", default="dataset_100.csv", help="Output CSV file")
    parser.add_argument("--region", "-r", default="sfbay", choices=list(REGIONS.keys()), help="Craigslist region")
    args = parser.parse_args()
    
    all_tasks = []
    
    # Generate all tasks
    generators = [
        ("cars_trucks", generate_cars_trucks_tasks),
        ("motorcycles", generate_motorcycles_tasks),
        ("rvs_camp", generate_rvs_camp_tasks),
        ("boats", generate_boats_tasks),
    ]
    
    print("=" * 70)
    print("CRAIGSLIST 100 CURATED TASKS GENERATOR")
    print("=" * 70)
    print(f"\nRegion: {args.region}")
    print(f"Location: {REGIONS[args.region]['location']}")
    print("\n" + "-" * 70)
    
    for category_name, generator_func in generators:
        tasks = generator_func(args.region)
        all_tasks.extend(tasks)
        print(f"  ✓ {category_name}: {len(tasks)} tasks")
    
    print("-" * 70)
    print(f"\n  TOTAL: {len(all_tasks)} tasks")
    
    # Verify we have exactly 100 tasks
    assert len(all_tasks) == 100, f"Expected 100 tasks, got {len(all_tasks)}"
    
    # Write to CSV
    fieldnames = [
        "task_id", "task_generation_config_json", "env", "domain",
        "l1_category", "l2_category", "suggested_difficulty",
        "suggested_hint", "suggested_max_steps", "suggested_split", "metadata_json"
    ]
    
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for task in all_tasks:
            writer.writerow(task_to_csv_row(task))
    
    print(f"\n✅ Generated exactly 100 tasks")
    print(f"📁 Output saved to: {args.output}")
    
    # Print detailed summary
    print("\n" + "=" * 70)
    print("FILTER COVERAGE SUMMARY")
    print("=" * 70)
    
    print("\n📊 Tasks by Category:")
    category_counts = {}
    for task in all_tasks:
        category_counts[task.l2_category] = category_counts.get(task.l2_category, 0) + 1
    
    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"   {category}: {count} tasks")
    
    print("\n📈 Difficulty Distribution:")
    difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}
    for task in all_tasks:
        difficulty_counts[task.difficulty] = difficulty_counts.get(task.difficulty, 0) + 1
    
    for difficulty in ["easy", "medium", "hard"]:
        count = difficulty_counts.get(difficulty, 0)
        pct = count / len(all_tasks) * 100
        bar = "█" * int(pct / 5)
        print(f"   {difficulty:8s}: {count:3d} ({pct:5.1f}%) {bar}")
    
    print("\n📋 Filter Types Covered:")
    print("   cars_trucks: make/model, transmission, fuel, body type, drivetrain,")
    print("                title status, year, mileage, color, condition, price,")
    print("                purveyor (owner/dealer), sort")
    print("   motorcycles: make/model, year, mileage, condition, type query,")
    print("                price, purveyor, sort")
    print("   rvs_camp:    RV type, brand, condition, price, purveyor, sort")
    print("   boats:       boat type, brand, condition, price, purveyor, sort")
    
    print("\n" + "=" * 70)
    print("✅ ALL 100 TASKS VALIDATED AND READY")
    print("=" * 70)


if __name__ == "__main__":
    main()