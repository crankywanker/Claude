"""
Seed data: Known generative AI companies relevant to anime/esports training data.

This provides a starting list of companies to investigate, curated from
public knowledge about the generative AI space.

These companies are either:
1. Working on generative AI for visual content
2. Building foundation models that could use anime/esports data
3. Creating synthetic data or training data marketplaces
4. Focused on gaming/entertainment AI
"""

SEED_COMPANIES = [
    # Major Foundation Model Companies
    {
        "name": "OpenAI",
        "crunchbase_url": "https://www.crunchbase.com/organization/openai",
        "category": "Foundation Models",
        "relevance": "DALL-E, Sora - visual content generation",
        "funding_stage": "Growth",
    },
    {
        "name": "Anthropic",
        "crunchbase_url": "https://www.crunchbase.com/organization/anthropic",
        "category": "Foundation Models",
        "relevance": "Claude - multimodal AI, potential visual training",
        "funding_stage": "Series C",
    },
    {
        "name": "Stability AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/stability-ai",
        "category": "Image Generation",
        "relevance": "Stable Diffusion - anime style models exist",
        "funding_stage": "Series B",
    },
    {
        "name": "Midjourney",
        "crunchbase_url": "https://www.crunchbase.com/organization/midjourney",
        "category": "Image Generation",
        "relevance": "Image generation, anime/art styles",
        "funding_stage": "Self-funded",
    },

    # Video Generation
    {
        "name": "Runway",
        "crunchbase_url": "https://www.crunchbase.com/organization/runwayml",
        "category": "Video Generation",
        "relevance": "Gen-2 video generation, animation potential",
        "funding_stage": "Series C",
    },
    {
        "name": "Pika Labs",
        "crunchbase_url": "https://www.crunchbase.com/organization/pika-labs",
        "category": "Video Generation",
        "relevance": "Video generation from text/images",
        "funding_stage": "Series A",
    },
    {
        "name": "Luma AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/luma-ai",
        "category": "Video/3D Generation",
        "relevance": "Dream Machine video generation",
        "funding_stage": "Series B",
    },
    {
        "name": "HeyGen",
        "crunchbase_url": "https://www.crunchbase.com/organization/heygen",
        "category": "Video Generation",
        "relevance": "AI avatar video generation",
        "funding_stage": "Series A",
    },

    # Gaming/Entertainment AI
    {
        "name": "Inworld AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/inworld-ai",
        "category": "Gaming AI",
        "relevance": "NPC AI, game character generation",
        "funding_stage": "Series A",
    },
    {
        "name": "Convai",
        "crunchbase_url": "https://www.crunchbase.com/organization/convai",
        "category": "Gaming AI",
        "relevance": "Game character AI, NPC conversations",
        "funding_stage": "Seed",
    },
    {
        "name": "Scenario",
        "crunchbase_url": "https://www.crunchbase.com/organization/scenario-gg",
        "category": "Gaming AI",
        "relevance": "AI game asset generation",
        "funding_stage": "Series A",
    },
    {
        "name": "Leonardo.AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/leonardo-ai",
        "category": "Gaming/Art AI",
        "relevance": "Game art and asset generation",
        "funding_stage": "Series A",
    },
    {
        "name": "Roblox",
        "crunchbase_url": "https://www.crunchbase.com/organization/roblox",
        "category": "Gaming Platform",
        "relevance": "AI-powered game creation tools",
        "funding_stage": "Public",
    },

    # Character/Avatar Generation
    {
        "name": "Character.AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/character-ai",
        "category": "Character AI",
        "relevance": "AI characters, personality generation",
        "funding_stage": "Series A",
    },
    {
        "name": "Synthesia",
        "crunchbase_url": "https://www.crunchbase.com/organization/synthesia",
        "category": "Avatar Generation",
        "relevance": "AI video avatars",
        "funding_stage": "Series C",
    },
    {
        "name": "Soul Machines",
        "crunchbase_url": "https://www.crunchbase.com/organization/soul-machines",
        "category": "Digital Humans",
        "relevance": "Autonomous digital humans",
        "funding_stage": "Series B",
    },

    # Training Data / Data Platforms
    {
        "name": "Scale AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/scale-ai",
        "category": "Data Labeling",
        "relevance": "Training data for AI models",
        "funding_stage": "Series E",
    },
    {
        "name": "Labelbox",
        "crunchbase_url": "https://www.crunchbase.com/organization/labelbox",
        "category": "Data Labeling",
        "relevance": "Training data platform",
        "funding_stage": "Series D",
    },
    {
        "name": "Sama",
        "crunchbase_url": "https://www.crunchbase.com/organization/sama",
        "category": "Data Annotation",
        "relevance": "AI training data annotation",
        "funding_stage": "Series C",
    },
    {
        "name": "Surge AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/surge-ai",
        "category": "Data Labeling",
        "relevance": "High-quality training data",
        "funding_stage": "Series A",
    },
    {
        "name": "Defined.ai",
        "crunchbase_url": "https://www.crunchbase.com/organization/defined-ai",
        "category": "Training Data",
        "relevance": "AI training data marketplace",
        "funding_stage": "Series B",
    },

    # Anime/Art Specific
    {
        "name": "Artbreeder",
        "crunchbase_url": "https://www.crunchbase.com/organization/artbreeder",
        "category": "Art Generation",
        "relevance": "Collaborative AI art, anime styles",
        "funding_stage": "Seed",
    },
    {
        "name": "NovelAI",
        "crunchbase_url": "https://www.crunchbase.com/organization/novelai",
        "category": "Art/Story Generation",
        "relevance": "Anime image generation, storytelling",
        "funding_stage": "Unknown",
    },
    {
        "name": "Hologram Labs",
        "crunchbase_url": "https://www.crunchbase.com/organization/hologram-labs",
        "category": "Digital Characters",
        "relevance": "AI for digital celebrities/vtubers",
        "funding_stage": "Series A",
    },

    # Esports/Streaming Related
    {
        "name": "Fnatic",
        "crunchbase_url": "https://www.crunchbase.com/organization/fnatic",
        "category": "Esports",
        "relevance": "Esports org exploring AI",
        "funding_stage": "Series B",
    },
    {
        "name": "100 Thieves",
        "crunchbase_url": "https://www.crunchbase.com/organization/100-thieves",
        "category": "Esports/Content",
        "relevance": "Gaming content, potential AI integration",
        "funding_stage": "Series C",
    },
    {
        "name": "FaceIt",
        "crunchbase_url": "https://www.crunchbase.com/organization/faceit",
        "category": "Esports Platform",
        "relevance": "Competitive gaming platform",
        "funding_stage": "Acquired",
    },

    # 3D/Animation AI
    {
        "name": "Kaedim",
        "crunchbase_url": "https://www.crunchbase.com/organization/kaedim",
        "category": "3D Generation",
        "relevance": "2D to 3D AI conversion",
        "funding_stage": "Series A",
    },
    {
        "name": "Kinetix",
        "crunchbase_url": "https://www.crunchbase.com/organization/kinetix",
        "category": "Animation AI",
        "relevance": "AI motion capture for games",
        "funding_stage": "Series A",
    },
    {
        "name": "Wonder Dynamics",
        "crunchbase_url": "https://www.crunchbase.com/organization/wonder-dynamics",
        "category": "VFX AI",
        "relevance": "AI-powered VFX and animation",
        "funding_stage": "Acquired by Autodesk",
    },
    {
        "name": "Plask",
        "crunchbase_url": "https://www.crunchbase.com/organization/plask",
        "category": "Animation AI",
        "relevance": "AI motion capture",
        "funding_stage": "Series A",
    },

    # Voice/Audio for Characters
    {
        "name": "ElevenLabs",
        "crunchbase_url": "https://www.crunchbase.com/organization/elevenlabs",
        "category": "Voice AI",
        "relevance": "Voice synthesis for characters",
        "funding_stage": "Series B",
    },
    {
        "name": "Resemble AI",
        "crunchbase_url": "https://www.crunchbase.com/organization/resemble-ai",
        "category": "Voice AI",
        "relevance": "Voice cloning for games/content",
        "funding_stage": "Series A",
    },
    {
        "name": "Replica Studios",
        "crunchbase_url": "https://www.crunchbase.com/organization/replica-studios",
        "category": "Voice AI",
        "relevance": "AI voices for games",
        "funding_stage": "Series A",
    },
]


def get_seed_companies():
    """Return the seed companies list."""
    return SEED_COMPANIES


def get_companies_by_category(category: str):
    """Filter seed companies by category."""
    return [c for c in SEED_COMPANIES if c.get("category") == category]


def get_high_priority_targets():
    """
    Get high-priority companies that are most likely to need
    anime/esports training data.
    """
    high_priority_categories = [
        "Image Generation",
        "Video Generation",
        "Gaming AI",
        "Character AI",
        "Art Generation",
        "Animation AI",
    ]
    return [
        c for c in SEED_COMPANIES
        if c.get("category") in high_priority_categories
    ]


# Categories for quick reference
CATEGORIES = list(set(c["category"] for c in SEED_COMPANIES))
