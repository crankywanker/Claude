"""
Crunchbase AI Company Scraper

Finds generative AI companies interested in training data,
particularly for anime and esports domains.
"""

from .config import (
    DOMAIN_KEYWORDS,
    PRIORITY_KEYWORDS,
    SEARCH_CATEGORIES,
)
from .models import Company, FundingRound
from .output import (
    generate_summary_report,
    print_summary,
    save_to_csv,
    save_to_excel,
    save_to_json,
)
from .scraper import CrunchbaseScraper
from .seed_companies import (
    SEED_COMPANIES,
    get_companies_by_category,
    get_high_priority_targets,
    get_seed_companies,
)

__all__ = [
    "CrunchbaseScraper",
    "Company",
    "FundingRound",
    "save_to_json",
    "save_to_csv",
    "save_to_excel",
    "print_summary",
    "generate_summary_report",
    "SEARCH_CATEGORIES",
    "PRIORITY_KEYWORDS",
    "DOMAIN_KEYWORDS",
    "SEED_COMPANIES",
    "get_seed_companies",
    "get_high_priority_targets",
    "get_companies_by_category",
]

__version__ = "0.1.0"
