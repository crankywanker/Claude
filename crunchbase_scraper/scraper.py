"""
Crunchbase scraper for AI companies.
Uses Selenium for dynamic content and requests for static pages.
"""

import json
import logging
import random
import re
import time
from typing import Optional
from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .config import (
    CRUNCHBASE_BASE_URL,
    DEFAULT_HEADERS,
    DOMAIN_KEYWORDS,
    MIN_FUNDING_AMOUNT,
    PRIORITY_KEYWORDS,
    REQUEST_DELAY_SECONDS,
    SEARCH_CATEGORIES,
)
from .models import Company, FundingRound

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrunchbaseScraper:
    """Scraper for Crunchbase company data."""

    def __init__(self, headless: bool = True, use_selenium: bool = True):
        self.headless = headless
        self.use_selenium = use_selenium
        self.driver: Optional[webdriver.Chrome] = None
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()

    def _setup_session(self):
        """Configure requests session with headers."""
        self.session.headers.update(DEFAULT_HEADERS)
        self.session.headers["User-Agent"] = self.ua.random

    def _setup_driver(self):
        """Initialize Selenium WebDriver."""
        if self.driver:
            return

        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={self.ua.random}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def _delay(self):
        """Add random delay between requests."""
        delay = REQUEST_DELAY_SECONDS + random.uniform(0.5, 1.5)
        time.sleep(delay)

    def search_companies(
        self,
        category: str = "artificial-intelligence",
        max_results: int = 100,
    ) -> list[dict]:
        """
        Search for companies in a category.
        Returns list of basic company info from search results.
        """
        logger.info(f"Searching for companies in category: {category}")

        if self.use_selenium:
            return self._search_with_selenium(category, max_results)
        else:
            return self._search_with_requests(category, max_results)

    def _search_with_selenium(self, category: str, max_results: int) -> list[dict]:
        """Search using Selenium for JavaScript-rendered content."""
        self._setup_driver()
        companies = []

        # Crunchbase search URL for category
        search_url = f"{CRUNCHBASE_BASE_URL}/discover/organization.companies/field/categories/{category}"

        try:
            self.driver.get(search_url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='identifier']"))
            )
            self._delay()

            page = 1
            while len(companies) < max_results:
                logger.info(f"Processing page {page}, found {len(companies)} companies so far")

                # Parse current page
                soup = BeautifulSoup(self.driver.page_source, "lxml")
                page_companies = self._parse_search_results(soup)

                if not page_companies:
                    logger.info("No more companies found on this page")
                    break

                companies.extend(page_companies)

                # Try to go to next page
                try:
                    next_button = self.driver.find_element(
                        By.CSS_SELECTOR, "[aria-label='Next page'], [class*='next']"
                    )
                    if next_button and next_button.is_enabled():
                        next_button.click()
                        self._delay()
                        page += 1
                    else:
                        break
                except Exception:
                    logger.info("No next page available")
                    break

        except Exception as e:
            logger.error(f"Error during search: {e}")

        return companies[:max_results]

    def _search_with_requests(self, category: str, max_results: int) -> list[dict]:
        """Fallback search using requests (limited functionality)."""
        companies = []
        search_url = f"{CRUNCHBASE_BASE_URL}/discover/organization.companies/field/categories/{category}"

        try:
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            companies = self._parse_search_results(soup)
        except Exception as e:
            logger.error(f"Error during request-based search: {e}")

        return companies[:max_results]

    def _parse_search_results(self, soup: BeautifulSoup) -> list[dict]:
        """Parse company data from search results page."""
        companies = []

        # Find company cards/rows in search results
        # Crunchbase uses various class patterns
        company_elements = soup.select(
            "[class*='identifier'], "
            "[data-test='organization-row'], "
            ".search-result-row, "
            "[class*='EntityCard']"
        )

        for elem in company_elements:
            try:
                # Extract company link and name
                link_elem = elem.select_one("a[href*='/organization/']")
                if not link_elem:
                    continue

                name = link_elem.get_text(strip=True)
                url = urljoin(CRUNCHBASE_BASE_URL, link_elem.get("href", ""))

                if not name or not url:
                    continue

                company_data = {
                    "name": name,
                    "url": url,
                }

                # Try to extract additional info from the row
                desc_elem = elem.select_one("[class*='description'], [class*='snippet']")
                if desc_elem:
                    company_data["short_description"] = desc_elem.get_text(strip=True)

                funding_elem = elem.select_one("[class*='funding'], [class*='money']")
                if funding_elem:
                    company_data["funding_text"] = funding_elem.get_text(strip=True)

                companies.append(company_data)

            except Exception as e:
                logger.debug(f"Error parsing company element: {e}")
                continue

        return companies

    def get_company_details(self, company_url: str) -> Optional[Company]:
        """
        Fetch detailed company information from company page.
        """
        logger.info(f"Fetching details for: {company_url}")
        self._delay()

        try:
            if self.use_selenium:
                self._setup_driver()
                self.driver.get(company_url)
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='profile']"))
                )
                soup = BeautifulSoup(self.driver.page_source, "lxml")
            else:
                response = self.session.get(company_url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "lxml")

            return self._parse_company_page(soup, company_url)

        except Exception as e:
            logger.error(f"Error fetching company details: {e}")
            return None

    def _parse_company_page(self, soup: BeautifulSoup, url: str) -> Optional[Company]:
        """Parse detailed company data from company profile page."""
        try:
            # Extract name
            name_elem = soup.select_one(
                "h1, [class*='title'], [class*='name'], [data-test='profile-header-title']"
            )
            name = name_elem.get_text(strip=True) if name_elem else "Unknown"

            company = Company(name=name, crunchbase_url=url)

            # Description
            desc_elem = soup.select_one(
                "[class*='description'], [data-test='description'], .about-description"
            )
            if desc_elem:
                company.description = desc_elem.get_text(strip=True)
                company.short_description = company.description[:500]

            # Headquarters
            hq_elem = soup.select_one(
                "[class*='location'], [data-test='headquarters'], [class*='headquarters']"
            )
            if hq_elem:
                company.headquarters = hq_elem.get_text(strip=True)

            # Founded year
            founded_elem = soup.select_one(
                "[class*='founded'], [data-test='founded']"
            )
            if founded_elem:
                year_match = re.search(r"(\d{4})", founded_elem.get_text())
                if year_match:
                    company.founded_year = int(year_match.group(1))

            # Employee count
            emp_elem = soup.select_one(
                "[class*='employee'], [data-test='employees']"
            )
            if emp_elem:
                company.employee_count = emp_elem.get_text(strip=True)

            # Website
            website_elem = soup.select_one(
                "a[href*='website'], [data-test='company-website'], a[class*='website']"
            )
            if website_elem:
                company.website = website_elem.get("href")

            # Funding information
            self._parse_funding_info(soup, company)

            # Categories and tags
            category_elems = soup.select(
                "[class*='category'], [class*='tag'], [data-test='chip']"
            )
            for cat in category_elems:
                text = cat.get_text(strip=True)
                if text:
                    company.categories.append(text)

            # Calculate relevance score
            self._calculate_relevance(company)

            return company

        except Exception as e:
            logger.error(f"Error parsing company page: {e}")
            return None

    def _parse_funding_info(self, soup: BeautifulSoup, company: Company):
        """Extract funding information from company page."""
        # Total funding
        funding_elem = soup.select_one(
            "[class*='total-funding'], [data-test='total-funding'], [class*='funding-total']"
        )
        if funding_elem:
            funding_text = funding_elem.get_text(strip=True)
            company.total_funding = self._parse_funding_amount(funding_text)

        # Last funding info
        last_funding = soup.select_one(
            "[class*='last-funding'], [data-test='last-funding-round']"
        )
        if last_funding:
            date_elem = last_funding.select_one("[class*='date']")
            if date_elem:
                company.last_funding_date = date_elem.get_text(strip=True)

            type_elem = last_funding.select_one("[class*='type'], [class*='round']")
            if type_elem:
                company.last_funding_type = type_elem.get_text(strip=True)

        # Funding rounds
        rounds = soup.select(
            "[class*='funding-round'], [data-test='funding-round']"
        )
        for round_elem in rounds:
            funding_round = FundingRound()

            amount_elem = round_elem.select_one("[class*='amount'], [class*='money']")
            if amount_elem:
                funding_round.amount = self._parse_funding_amount(
                    amount_elem.get_text(strip=True)
                )

            type_elem = round_elem.select_one("[class*='type'], [class*='round-name']")
            if type_elem:
                funding_round.round_type = type_elem.get_text(strip=True)

            date_elem = round_elem.select_one("[class*='date']")
            if date_elem:
                funding_round.date = date_elem.get_text(strip=True)

            company.funding_rounds.append(funding_round)

        # Investors
        investor_elems = soup.select(
            "[class*='investor'] a, [data-test='investor-name'], [class*='investor-name']"
        )
        for inv in investor_elems:
            name = inv.get_text(strip=True)
            if name and name not in company.investors:
                company.investors.append(name)

    def _parse_funding_amount(self, text: str) -> Optional[float]:
        """Parse funding amount from text like '$10M' or '$1.5B'."""
        if not text:
            return None

        text = text.upper().replace(",", "").replace(" ", "")

        multipliers = {
            "K": 1_000,
            "M": 1_000_000,
            "B": 1_000_000_000,
        }

        match = re.search(r"\$?([\d.]+)\s*([KMB])?", text)
        if match:
            amount = float(match.group(1))
            suffix = match.group(2)
            if suffix and suffix in multipliers:
                amount *= multipliers[suffix]
            return amount

        return None

    def _calculate_relevance(self, company: Company):
        """Calculate relevance score based on keyword matches."""
        text_to_search = " ".join([
            company.name.lower(),
            (company.description or "").lower(),
            (company.short_description or "").lower(),
            " ".join(company.categories).lower(),
            " ".join(company.tags).lower(),
        ])

        score = 0.0
        matches = []

        # Priority keywords (higher weight)
        for keyword in PRIORITY_KEYWORDS:
            if keyword.lower() in text_to_search:
                score += 2.0
                matches.append(keyword)

        # Domain-specific keywords (bonus)
        for keyword in DOMAIN_KEYWORDS:
            if keyword.lower() in text_to_search:
                score += 3.0  # Higher bonus for anime/esports relevance
                matches.append(f"[DOMAIN] {keyword}")

        # Funding bonus
        if company.total_funding and company.total_funding >= MIN_FUNDING_AMOUNT:
            score += 1.0
            # Additional bonus for larger funding
            if company.total_funding >= 10_000_000:
                score += 1.0
            if company.total_funding >= 50_000_000:
                score += 1.0

        company.keyword_matches = list(set(matches))
        company.relevance_score = score

    def scrape_ai_companies(
        self,
        categories: list[str] = None,
        max_per_category: int = 50,
        min_relevance: float = 2.0,
    ) -> list[Company]:
        """
        Main method to scrape AI companies across categories.
        """
        if categories is None:
            categories = SEARCH_CATEGORIES

        all_companies = []
        seen_urls = set()

        for category in categories:
            logger.info(f"\n{'='*50}")
            logger.info(f"Searching category: {category}")
            logger.info(f"{'='*50}")

            # Search for companies in category
            search_results = self.search_companies(category, max_per_category)
            logger.info(f"Found {len(search_results)} companies in search results")

            for result in search_results:
                url = result.get("url")
                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                # Get detailed info
                company = self.get_company_details(url)
                if company:
                    # Only include if meets minimum relevance
                    if company.relevance_score >= min_relevance:
                        all_companies.append(company)
                        logger.info(
                            f"Added: {company.name} "
                            f"(score: {company.relevance_score}, "
                            f"funding: ${company.total_funding or 0:,.0f})"
                        )

        # Sort by relevance score
        all_companies.sort(key=lambda c: c.relevance_score, reverse=True)

        logger.info(f"\nTotal companies found: {len(all_companies)}")
        return all_companies

    def close(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
            self.driver = None
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
