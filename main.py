#!/usr/bin/env python3
"""
Crunchbase AI Company Scraper - Main Entry Point

Scrapes Crunchbase for generative AI companies that may be interested
in training data from anime and esports domains.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from crunchbase_scraper import (
    SEARCH_CATEGORIES,
    CrunchbaseScraper,
    generate_summary_report,
    print_summary,
    save_to_csv,
    save_to_json,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape Crunchbase for AI companies interested in training data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python main.py

  # Scrape specific categories
  python main.py --categories generative-ai artificial-intelligence

  # Increase results per category
  python main.py --max-per-category 100

  # Use headful browser (for debugging)
  python main.py --no-headless

  # Only use requests (no Selenium, limited results)
  python main.py --no-selenium
        """,
    )

    parser.add_argument(
        "--categories",
        nargs="+",
        default=SEARCH_CATEGORIES,
        help="Crunchbase categories to search",
    )
    parser.add_argument(
        "--max-per-category",
        type=int,
        default=50,
        help="Maximum companies to fetch per category (default: 50)",
    )
    parser.add_argument(
        "--min-relevance",
        type=float,
        default=2.0,
        help="Minimum relevance score to include (default: 2.0)",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for results (default: output)",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser in visible mode (for debugging)",
    )
    parser.add_argument(
        "--no-selenium",
        action="store_true",
        help="Use requests only (limited functionality)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        default="both",
        help="Output format (default: both)",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    logger.info("Starting Crunchbase AI Company Scraper")
    logger.info(f"Categories: {args.categories}")
    logger.info(f"Max per category: {args.max_per_category}")
    logger.info(f"Min relevance score: {args.min_relevance}")

    try:
        with CrunchbaseScraper(
            headless=not args.no_headless,
            use_selenium=not args.no_selenium,
        ) as scraper:
            # Scrape companies
            companies = scraper.scrape_ai_companies(
                categories=args.categories,
                max_per_category=args.max_per_category,
                min_relevance=args.min_relevance,
            )

            if not companies:
                logger.warning("No companies found matching criteria")
                return 1

            # Save results
            output_files = []

            if args.format in ["json", "both"]:
                json_file = save_to_json(companies, args.output_dir)
                output_files.append(json_file)

            if args.format in ["csv", "both"]:
                csv_file = save_to_csv(companies, args.output_dir)
                output_files.append(csv_file)

            # Save summary report
            report = generate_summary_report(companies)
            report_file = Path(args.output_dir) / "summary_report.txt"
            report_file.write_text(report)
            output_files.append(str(report_file))

            # Print summary
            print_summary(companies)

            logger.info(f"\nOutput files saved:")
            for f in output_files:
                logger.info(f"  - {f}")

            return 0

    except KeyboardInterrupt:
        logger.info("\nScraping interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Scraping failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
