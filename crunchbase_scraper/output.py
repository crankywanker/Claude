"""
Output formatters for scraped company data.
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from .models import Company

logger = logging.getLogger(__name__)


def save_to_json(
    companies: list[Company],
    output_dir: str = "output",
    filename: Optional[str] = None,
) -> str:
    """Save companies to JSON file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_companies_{timestamp}.json"

    filepath = output_path / filename

    data = {
        "metadata": {
            "scraped_at": datetime.now().isoformat(),
            "total_companies": len(companies),
        },
        "companies": [c.to_dict() for c in companies],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved {len(companies)} companies to {filepath}")
    return str(filepath)


def save_to_csv(
    companies: list[Company],
    output_dir: str = "output",
    filename: Optional[str] = None,
) -> str:
    """Save companies to CSV file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_companies_{timestamp}.csv"

    filepath = output_path / filename

    if not companies:
        logger.warning("No companies to save")
        return str(filepath)

    # Use flat dict for CSV
    rows = [c.to_flat_dict() for c in companies]

    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False, encoding="utf-8")

    logger.info(f"Saved {len(companies)} companies to {filepath}")
    return str(filepath)


def save_to_excel(
    companies: list[Company],
    output_dir: str = "output",
    filename: Optional[str] = None,
) -> str:
    """Save companies to Excel file with multiple sheets."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_companies_{timestamp}.xlsx"

    filepath = output_path / filename

    if not companies:
        logger.warning("No companies to save")
        return str(filepath)

    # Main data
    rows = [c.to_flat_dict() for c in companies]
    df_main = pd.DataFrame(rows)

    # High priority (high relevance + funded)
    high_priority = [
        c for c in companies
        if c.relevance_score >= 5.0 and (c.total_funding or 0) >= 1_000_000
    ]
    df_priority = pd.DataFrame([c.to_flat_dict() for c in high_priority])

    # Recently funded
    recently_funded = [
        c for c in companies
        if c.last_funding_date and "2024" in str(c.last_funding_date)
    ]
    df_recent = pd.DataFrame([c.to_flat_dict() for c in recently_funded])

    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df_main.to_excel(writer, sheet_name="All Companies", index=False)
        if not df_priority.empty:
            df_priority.to_excel(writer, sheet_name="High Priority", index=False)
        if not df_recent.empty:
            df_recent.to_excel(writer, sheet_name="Recently Funded", index=False)

    logger.info(f"Saved {len(companies)} companies to {filepath}")
    return str(filepath)


def generate_summary_report(companies: list[Company]) -> str:
    """Generate a text summary report of findings."""
    if not companies:
        return "No companies found."

    total = len(companies)
    funded = [c for c in companies if c.total_funding and c.total_funding > 0]
    total_funding = sum(c.total_funding or 0 for c in companies)

    # Group by relevance
    high_relevance = [c for c in companies if c.relevance_score >= 5.0]
    medium_relevance = [c for c in companies if 2.0 <= c.relevance_score < 5.0]

    # Top investors
    all_investors = []
    for c in companies:
        all_investors.extend(c.investors)
    investor_counts = {}
    for inv in all_investors:
        investor_counts[inv] = investor_counts.get(inv, 0) + 1
    top_investors = sorted(investor_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    report = f"""
================================================================================
           CRUNCHBASE AI COMPANIES REPORT - ANIME/ESPORTS TRAINING DATA
================================================================================

SUMMARY
-------
Total Companies Found: {total}
Companies with Funding: {len(funded)}
Total Funding Tracked: ${total_funding:,.0f}

RELEVANCE BREAKDOWN
-------------------
High Relevance (score >= 5.0): {len(high_relevance)}
Medium Relevance (2.0-5.0): {len(medium_relevance)}

TOP 10 HIGH-PRIORITY COMPANIES
------------------------------
"""

    for i, company in enumerate(high_relevance[:10], 1):
        report += f"""
{i}. {company.name}
   URL: {company.crunchbase_url}
   Funding: ${company.total_funding or 0:,.0f}
   Last Round: {company.last_funding_type or 'N/A'} ({company.last_funding_date or 'N/A'})
   Keywords: {', '.join(company.keyword_matches[:5])}
   Score: {company.relevance_score}
"""

    report += """
TOP INVESTORS IN THIS SPACE
---------------------------
"""
    for inv, count in top_investors:
        report += f"  - {inv}: {count} investments\n"

    report += """
================================================================================
                              END OF REPORT
================================================================================
"""
    return report


def print_summary(companies: list[Company]):
    """Print a summary to console."""
    print(generate_summary_report(companies))
