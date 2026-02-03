"""
Data models for Crunchbase scraper.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class FundingRound:
    """Represents a single funding round."""
    date: Optional[str] = None
    amount: Optional[float] = None
    currency: str = "USD"
    round_type: Optional[str] = None  # Seed, Series A, etc.
    investors: list[str] = field(default_factory=list)
    lead_investor: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "amount": self.amount,
            "currency": self.currency,
            "round_type": self.round_type,
            "investors": self.investors,
            "lead_investor": self.lead_investor,
        }


@dataclass
class Company:
    """Represents a company from Crunchbase."""
    name: str
    crunchbase_url: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None

    # Funding info
    total_funding: Optional[float] = None
    funding_currency: str = "USD"
    last_funding_date: Optional[str] = None
    last_funding_type: Optional[str] = None
    funding_rounds: list[FundingRound] = field(default_factory=list)
    investors: list[str] = field(default_factory=list)

    # Categorization
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    # Relevance scoring
    keyword_matches: list[str] = field(default_factory=list)
    relevance_score: float = 0.0

    # Metadata
    scraped_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "crunchbase_url": self.crunchbase_url,
            "description": self.description,
            "short_description": self.short_description,
            "headquarters": self.headquarters,
            "founded_year": self.founded_year,
            "employee_count": self.employee_count,
            "website": self.website,
            "linkedin": self.linkedin,
            "twitter": self.twitter,
            "total_funding": self.total_funding,
            "funding_currency": self.funding_currency,
            "last_funding_date": self.last_funding_date,
            "last_funding_type": self.last_funding_type,
            "funding_rounds": [fr.to_dict() for fr in self.funding_rounds],
            "investors": self.investors,
            "categories": self.categories,
            "tags": self.tags,
            "keyword_matches": self.keyword_matches,
            "relevance_score": self.relevance_score,
            "scraped_at": self.scraped_at,
        }

    def to_flat_dict(self) -> dict:
        """Flatten for CSV export."""
        return {
            "name": self.name,
            "crunchbase_url": self.crunchbase_url,
            "description": self.short_description or self.description,
            "headquarters": self.headquarters,
            "founded_year": self.founded_year,
            "employee_count": self.employee_count,
            "website": self.website,
            "total_funding_usd": self.total_funding,
            "last_funding_date": self.last_funding_date,
            "last_funding_type": self.last_funding_type,
            "top_investors": ", ".join(self.investors[:5]) if self.investors else "",
            "categories": ", ".join(self.categories),
            "keyword_matches": ", ".join(self.keyword_matches),
            "relevance_score": self.relevance_score,
        }
