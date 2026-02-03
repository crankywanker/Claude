# Crunchbase AI Company Scraper

A Python scraper to find generative AI companies on Crunchbase that might be interested in training data from anime and esports domains.

## Purpose

This tool helps identify AI companies that:
- Work on generative AI (images, video, 3D, characters)
- May need training data for visual content generation
- Are actively receiving investment funding
- Operate in gaming, entertainment, or creative AI spaces

## Installation

```bash
# Clone the repository
cd crunchbase-ai-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Web Scraper (Default)

The web scraper uses Selenium to navigate Crunchbase and extract company data.

```bash
# Run with default settings
python main.py

# Scrape specific categories only
python main.py --categories generative-ai artificial-intelligence

# Get more results per category
python main.py --max-per-category 100

# Debug mode (show browser)
python main.py --no-headless

# Output to specific directory
python main.py --output-dir ./my_results
```

### 2. API Scraper (Requires API Key)

If you have a Crunchbase API key, use the API scraper for more reliable results.

```python
from crunchbase_scraper.api_scraper import CrunchbaseAPI

# Set API key
api = CrunchbaseAPI(api_key="your-api-key")
# Or set CRUNCHBASE_API_KEY environment variable

# Search for AI companies
companies = api.search_ai_companies(
    keywords=["generative ai", "synthetic data"],
    min_funding=1_000_000,
    limit=100
)

for company in companies:
    print(f"{company.name}: ${company.total_funding:,.0f}")
```

### 3. Seed Companies List

Use the curated list of known AI companies as a starting point:

```python
from crunchbase_scraper.seed_companies import (
    get_seed_companies,
    get_high_priority_targets,
    get_companies_by_category,
)

# Get all seed companies
all_companies = get_seed_companies()

# Get high-priority targets for anime/esports data
priority = get_high_priority_targets()

# Get companies by category
gaming_ai = get_companies_by_category("Gaming AI")
```

## Output

Results are saved to the `output/` directory:

- `ai_companies_TIMESTAMP.json` - Full data in JSON format
- `ai_companies_TIMESTAMP.csv` - Flat data for spreadsheets
- `summary_report.txt` - Human-readable summary

### CSV Fields

| Field | Description |
|-------|-------------|
| name | Company name |
| crunchbase_url | Link to Crunchbase profile |
| description | Company description |
| headquarters | Location |
| founded_year | Year founded |
| total_funding_usd | Total funding received |
| last_funding_date | Date of last funding round |
| last_funding_type | Type (Seed, Series A, etc.) |
| top_investors | Top 5 investors |
| categories | Crunchbase categories |
| keyword_matches | Why this company is relevant |
| relevance_score | Computed relevance score |

## Search Categories

The scraper searches these Crunchbase categories by default:

- `artificial-intelligence`
- `generative-ai`
- `machine-learning`
- `deep-learning`
- `natural-language-processing`
- `computer-vision`
- `synthetic-data`

## Relevance Scoring

Companies are scored based on:

| Factor | Points |
|--------|--------|
| Priority keyword match | +2.0 each |
| Domain keyword match (anime/esports) | +3.0 each |
| Funding >= $1M | +1.0 |
| Funding >= $10M | +1.0 |
| Funding >= $50M | +1.0 |

Only companies with relevance score >= 2.0 are included by default.

### Priority Keywords

- generative ai, llm, foundation model
- training data, synthetic data
- image generation, video generation
- gaming, entertainment, animation

### Domain Keywords (Higher Weight)

- anime, esports, gaming
- virtual characters, digital avatars
- game development, streaming

## Configuration

Edit `crunchbase_scraper/config.py` to customize:

- Search categories
- Keywords and weights
- Minimum funding thresholds
- Rate limiting

## Legal Notice

- This tool is for research purposes
- Respect Crunchbase's Terms of Service
- Consider using the official API for production use
- Rate limiting is built in to avoid overloading servers

## Project Structure

```
crunchbase-ai-scraper/
├── main.py                    # CLI entry point
├── requirements.txt           # Python dependencies
├── crunchbase_scraper/
│   ├── __init__.py
│   ├── config.py              # Configuration
│   ├── models.py              # Data models
│   ├── scraper.py             # Web scraper (Selenium)
│   ├── api_scraper.py         # API scraper
│   ├── seed_companies.py      # Curated company list
│   └── output.py              # Export functions
└── output/                    # Results directory
```

## License

MIT
