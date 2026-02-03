"""
Configuration for Crunchbase AI company scraper.
Focused on finding generative AI companies interested in training data.
"""

# Search categories on Crunchbase
SEARCH_CATEGORIES = [
    "artificial-intelligence",
    "generative-ai",
    "machine-learning",
    "deep-learning",
    "natural-language-processing",
    "computer-vision",
    "synthetic-data",
]

# Keywords to filter companies (in description, tags, etc.)
PRIORITY_KEYWORDS = [
    # Core AI/ML terms
    "generative ai",
    "large language model",
    "llm",
    "foundation model",
    "diffusion model",
    "transformer",
    "neural network",
    "deep learning",

    # Training data related
    "training data",
    "synthetic data",
    "data labeling",
    "data annotation",
    "dataset",
    "fine-tuning",
    "fine tuning",

    # Content generation
    "image generation",
    "video generation",
    "content generation",
    "text-to-image",
    "text-to-video",
    "ai art",
    "creative ai",

    # Relevant domains
    "gaming",
    "entertainment",
    "media",
    "animation",
    "visual content",
    "digital content",
]

# Secondary keywords (anime/esports specific)
DOMAIN_KEYWORDS = [
    "anime",
    "esports",
    "gaming",
    "streaming",
    "entertainment",
    "video games",
    "virtual characters",
    "digital avatars",
    "character generation",
    "game development",
    "game ai",
]

# Funding stages to prioritize
FUNDING_STAGES = [
    "Seed",
    "Series A",
    "Series B",
    "Series C",
    "Series D",
    "Pre-Seed",
    "Angel",
    "Venture",
]

# Minimum funding amount to consider (in USD)
MIN_FUNDING_AMOUNT = 1_000_000  # $1M

# Rate limiting
REQUEST_DELAY_SECONDS = 2.0
MAX_RETRIES = 3

# Output settings
OUTPUT_DIR = "output"
OUTPUT_FORMATS = ["csv", "json"]

# Crunchbase URLs
CRUNCHBASE_BASE_URL = "https://www.crunchbase.com"
CRUNCHBASE_SEARCH_URL = "https://www.crunchbase.com/discover/organization.companies"
CRUNCHBASE_API_URL = "https://api.crunchbase.com/v4"

# Headers for requests
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
