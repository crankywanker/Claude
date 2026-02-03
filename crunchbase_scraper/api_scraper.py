"""
Crunchbase API-based scraper (requires API key).

For users with Crunchbase API access, this provides a more reliable
and ToS-compliant way to fetch company data.

Get API access at: https://www.crunchbase.com/home/api
"""

import logging
import os
import time
from typing import Optional

import requests
from dotenv import load_dotenv

from .config import DOMAIN_KEYWORDS, MIN_FUNDING_AMOUNT, PRIORITY_KEYWORDS
from .models import Company, FundingRound

load_dotenv()
logger = logging.getLogger(__name__)


class CrunchbaseAPI:
    """
    Crunchbase API client for fetching company data.

    Requires CRUNCHBASE_API_KEY environment variable or pass key directly.
    """

    BASE_URL = "https://api.crunchbase.com/api/v4"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CRUNCHBASE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Crunchbase API key required. Set CRUNCHBASE_API_KEY env var or pass key directly."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "X-cb-user-key": self.api_key,
            "Content-Type": "application/json",
        })

    def search_organizations(
        self,
        query: str = None,
        categories: list[str] = None,
        funding_stage: str = None,
        min_funding: float = None,
        limit: int = 50,
    ) -> list[dict]:
        """
        Search for organizations using the Crunchbase API.

        Args:
            query: Text search query
            categories: List of category UUIDs or names
            funding_stage: e.g., "seed", "series_a", etc.
            min_funding: Minimum total funding in USD
            limit: Maximum results to return
        """
        endpoint = f"{self.BASE_URL}/searches/organizations"

        # Build query
        field_ids = [
            "identifier",
            "short_description",
            "categories",
            "location_identifiers",
            "founded_on",
            "num_employees_enum",
            "funding_total",
            "last_funding_type",
            "last_funding_at",
            "investor_identifiers",
            "website_url",
        ]

        query_body = {
            "field_ids": field_ids,
            "limit": limit,
            "order": [{"field_id": "funding_total", "sort": "desc"}],
        }

        # Build query predicates
        predicates = []

        if query:
            predicates.append({
                "field_id": "short_description",
                "operator_id": "contains",
                "values": [query],
            })

        if categories:
            predicates.append({
                "field_id": "categories",
                "operator_id": "includes",
                "values": categories,
            })

        if funding_stage:
            predicates.append({
                "field_id": "last_funding_type",
                "operator_id": "eq",
                "values": [funding_stage],
            })

        if min_funding:
            predicates.append({
                "field_id": "funding_total",
                "operator_id": "gte",
                "values": [min_funding],
            })

        if predicates:
            query_body["query"] = predicates

        try:
            response = self.session.post(endpoint, json=query_body)
            response.raise_for_status()
            data = response.json()
            return data.get("entities", [])
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []

    def get_organization(self, permalink: str) -> Optional[dict]:
        """Get detailed organization info by permalink."""
        endpoint = f"{self.BASE_URL}/entities/organizations/{permalink}"

        params = {
            "field_ids": ",".join([
                "identifier",
                "short_description",
                "description",
                "categories",
                "location_identifiers",
                "founded_on",
                "num_employees_enum",
                "funding_total",
                "last_funding_type",
                "last_funding_at",
                "investor_identifiers",
                "website_url",
                "linkedin",
                "twitter",
                "funding_rounds",
            ]),
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch organization {permalink}: {e}")
            return None

    def get_funding_rounds(self, permalink: str) -> list[dict]:
        """Get funding rounds for an organization."""
        endpoint = f"{self.BASE_URL}/entities/organizations/{permalink}/funding_rounds"

        params = {
            "field_ids": ",".join([
                "identifier",
                "announced_on",
                "money_raised",
                "funding_type",
                "investor_identifiers",
                "lead_investor_identifiers",
            ]),
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("entities", [])
        except requests.RequestException as e:
            logger.error(f"Failed to fetch funding rounds for {permalink}: {e}")
            return []

    def search_ai_companies(
        self,
        keywords: list[str] = None,
        min_funding: float = MIN_FUNDING_AMOUNT,
        limit: int = 100,
    ) -> list[Company]:
        """
        Search for AI companies relevant to anime/esports training data.
        """
        if keywords is None:
            keywords = ["generative ai", "ai training", "synthetic data", "llm"]

        all_companies = []
        seen = set()

        # AI-related category UUIDs (from Crunchbase)
        ai_categories = [
            "artificial-intelligence",
            "machine-learning",
            "generative-ai",
            "natural-language-processing",
        ]

        for keyword in keywords:
            logger.info(f"Searching for: {keyword}")

            results = self.search_organizations(
                query=keyword,
                categories=ai_categories,
                min_funding=min_funding,
                limit=limit // len(keywords),
            )

            for entity in results:
                props = entity.get("properties", {})
                identifier = props.get("identifier", {})
                permalink = identifier.get("permalink", "")

                if permalink in seen:
                    continue
                seen.add(permalink)

                company = self._entity_to_company(entity)
                if company:
                    self._calculate_relevance(company)
                    if company.relevance_score >= 2.0:
                        all_companies.append(company)

            time.sleep(0.5)  # Rate limiting

        # Sort by relevance
        all_companies.sort(key=lambda c: c.relevance_score, reverse=True)
        return all_companies

    def _entity_to_company(self, entity: dict) -> Optional[Company]:
        """Convert API entity to Company model."""
        try:
            props = entity.get("properties", {})
            identifier = props.get("identifier", {})

            company = Company(
                name=identifier.get("value", "Unknown"),
                crunchbase_url=f"https://www.crunchbase.com/organization/{identifier.get('permalink', '')}",
            )

            company.short_description = props.get("short_description", "")
            company.description = props.get("description", "")

            # Location
            locations = props.get("location_identifiers", [])
            if locations:
                company.headquarters = locations[0].get("value", "")

            # Founded
            founded = props.get("founded_on", {})
            if founded:
                company.founded_year = int(founded.get("value", "")[:4]) if founded.get("value") else None

            # Employees
            company.employee_count = props.get("num_employees_enum", "")

            # Website
            company.website = props.get("website_url", "")

            # Funding
            funding_total = props.get("funding_total", {})
            if funding_total:
                company.total_funding = funding_total.get("value_usd")

            company.last_funding_type = props.get("last_funding_type", "")
            last_funding = props.get("last_funding_at", {})
            if last_funding:
                company.last_funding_date = last_funding.get("value", "")

            # Investors
            investors = props.get("investor_identifiers", [])
            company.investors = [inv.get("value", "") for inv in investors]

            # Categories
            categories = props.get("categories", [])
            company.categories = [cat.get("value", "") for cat in categories]

            return company

        except Exception as e:
            logger.error(f"Error converting entity: {e}")
            return None

    def _calculate_relevance(self, company: Company):
        """Calculate relevance score based on keyword matches."""
        text_to_search = " ".join([
            company.name.lower(),
            (company.description or "").lower(),
            (company.short_description or "").lower(),
            " ".join(company.categories).lower(),
        ])

        score = 0.0
        matches = []

        for keyword in PRIORITY_KEYWORDS:
            if keyword.lower() in text_to_search:
                score += 2.0
                matches.append(keyword)

        for keyword in DOMAIN_KEYWORDS:
            if keyword.lower() in text_to_search:
                score += 3.0
                matches.append(f"[DOMAIN] {keyword}")

        if company.total_funding and company.total_funding >= MIN_FUNDING_AMOUNT:
            score += 1.0
            if company.total_funding >= 10_000_000:
                score += 1.0
            if company.total_funding >= 50_000_000:
                score += 1.0

        company.keyword_matches = list(set(matches))
        company.relevance_score = score


def run_api_scraper(api_key: str = None) -> list[Company]:
    """
    Convenience function to run the API scraper.

    Usage:
        from crunchbase_scraper.api_scraper import run_api_scraper
        companies = run_api_scraper("your-api-key")
    """
    api = CrunchbaseAPI(api_key)
    return api.search_ai_companies()
