"""
Paper discovery configuration for the ArXiv Second Brain.
Defines seed papers, keyword tiers, arXiv categories, and Semantic Scholar expansion.
"""

# =============================================================================
# arXiv categories to monitor
# =============================================================================

PRIMARY_CATEGORIES = [
    "q-fin.TR",   # Trading and Market Microstructure
    "q-fin.MF",   # Mathematical Finance
    "q-fin.ST",   # Statistical Finance
    "q-fin.CP",   # Computational Finance
]

# Cross-listed categories: include if also tagged with any PRIMARY category
CROSSLIST_CATEGORIES = [
    "cs.LG",      # Machine Learning
    "cs.AI",      # Artificial Intelligence
    "cs.CE",      # Computational Engineering (execution algos)
    "stat.ML",    # Statistics — Machine Learning
]


# =============================================================================
# Keyword tiers for filtering (applied to title + abstract)
# =============================================================================

# Tier 1: Auto-ingest — core microstructure signals
# Any match in title OR abstract → automatically download and ingest
TIER1_MUST_INGEST = [
    # Order flow signals
    "order flow imbalance",
    "orderflow imbalance",
    "order book imbalance",
    "orderbook imbalance",
    "trade flow imbalance",
    "trade imbalance",
    "OFI",                      # Common abbreviation for Order Flow Imbalance
    "OBI",                      # Order Book Imbalance
    "GOFI",                     # Generalised Order Flow Imbalance
    "deep order flow",
    "multi-level order flow",

    # Microprice and fair value
    "microprice",
    "micro-price",
    "fair price estimate",
    "mid-price prediction",

    # LOB signals
    "limit order book signal",
    "LOB signal",
    "order book feature",
    "book pressure",
    "queue imbalance",
    "volume imbalance",
    "depth imbalance",

    # Specific models you care about
    "Cont Kukanov Stoikov",     # The OFI paper authors
    "Kolm Turiel Westray",     # Deep OFI paper authors
]

# Tier 2: Likely relevant — ingest if in a primary q-fin category
# Match + primary category → auto-ingest
# Match + crosslist only → flag for review
TIER2_LIKELY_RELEVANT = [
    # Market making
    "market making",
    "market-making",
    "liquidity provision",
    "liquidity providing",
    "inventory management",
    "Avellaneda Stoikov",
    "Guéant Lehalle",

    # Spread and price impact
    "bid-ask spread",
    "bid ask spread",
    "price impact",
    "market impact",
    "temporary impact",
    "permanent impact",
    "Kyle lambda",
    "Amihud illiquidity",

    # Adverse selection
    "adverse selection",
    "informed trading",
    "information asymmetry",
    "toxic flow",
    "toxicity indicator",
    "VPIN",

    # High-frequency
    "high-frequency trading",
    "high frequency trading",
    "HFT",
    "ultra-high frequency",
    "tick-by-tick",
    "tick data",
    "intraday",

    # LOB modelling
    "limit order book",
    "LOB",
    "order book",
    "order-driven market",
    "continuous double auction",
    "LOB forecasting",
    "order book dynamics",

    # Execution
    "optimal execution",
    "execution quality",
    "transaction cost",
    "slippage",
    "TWAP",
    "VWAP execution",
    "Almgren Chriss",

    # Exchange-specific microstructure
    "Eurex",
    "HKEX",
    "Hong Kong Exchange",
    "Xetra",
    "Deutsche Börse",
    "T7 trading",
    "CLOB",                     # Central Limit Order Book
    "opening auction",
    "closing auction",
    "volatility interruption",
    "circuit breaker",
]

# Tier 3: Context papers — flag for manual review
# These are relevant background but not core signal research
TIER3_CONTEXT = [
    # Market structure
    "tick size",
    "tick-to-trade",
    "queue position",
    "queue priority",
    "latency arbitrage",
    "co-location",
    "speed bump",
    "frequent batch auction",

    # Exchange-specific structure
    "maker-taker",
    "maker taker",
    "fee rebate",
    "market fragmentation",
    "dark pool",
    "lit market",
    "MiFID",
    "best execution",
    "SFC",                      # HK Securities and Futures Commission
    "ESMA",
    "Xetra liquidity measure",
    "designated sponsor",       # Eurex market making programme
    "volatility auction",
    "pre-opening",
    "intraday auction",

    # Classic models
    "Kyle model",
    "Glosten-Milgrom",
    "Glosten Milgrom",
    "sequential trade model",
    "PIN model",
    "Roll model",

    # Price discovery
    "price discovery",
    "price formation",
    "information share",
    "Hasbrouck",

    # Volatility at micro scale
    "realised volatility",
    "realized volatility",
    "realised variance",
    "realized variance",
    "microstructure noise",
    "signature plot",

    # ML applied to LOB
    "DeepLOB",
    "deep learning order book",
    "neural network order book",
    "reinforcement learning trading",
    "RL market making",

    # Hawkes processes (used for order arrival modelling)
    "Hawkes process",
    "self-exciting process",
    "point process trading",
]


# =============================================================================
# Seed papers — foundational corpus to bootstrap the wiki
# =============================================================================
# Format: (arxiv_id, short_description)

SEED_PAPERS = [
    # === ORDER FLOW IMBALANCE — the core signal ===
    ("1011.6402", "Cont, Kukanov, Stoikov — The Price Impact of Order Book Events (2014, seminal OFI paper)"),
    ("2112.02947", "Generalized Order Flow Imbalance — GOFI extension"),
    # Kolm, Turiel, Westray — Deep OFI (2021, Mathematical Finance) — may need DOI fetch
    ("2403.09267", "Deep Limit Order Book Forecasting — microstructural guide (2024)"),
    ("2408.03594", "Forecasting high frequency order flow imbalance using Hawkes processes (2024)"),
    ("2507.22712", "Order Book Filtration and Directional Signal Extraction (2025)"),
    ("2602.00776", "Explainable Patterns in Cryptocurrency Microstructure — SHAP on OBI (2026)"),

    # === MICROPRICE ===
    ("2411.13594", "High resolution microprice estimates using Tsetlin Machines (2024)"),
    # Gatheral, Oomen — Microprice (2010) — may need SSRN

    # === MARKET MAKING MODELS ===
    ("0710.0481", "Avellaneda & Stoikov — High-frequency trading in a limit order book (2008)"),
    ("1105.3115", "Guéant, Lehalle, Fernandez-Tapia — Optimal market making (2013)"),
    ("1512.03154", "Cartea, Jaimungal, Penalva — Algorithmic and HFT (2015, textbook chapters on arXiv)"),

    # === LOB MODELLING ===
    ("1204.0148", "Cont — Statistical modelling of high-frequency order book data (2012)"),
    ("1502.03844", "Cont, De Larrard — Price dynamics in a Markovian limit order market (2013)"),
    ("1906.07762", "Sirignano & Cont — Universal features of price formation via deep learning (2019)"),
    ("2003.11941", "Zhang et al — DeepLOB: Deep convolutional neural network for LOB (2019)"),

    # === PRICE IMPACT ===
    ("2004.08290", "Empirical Study of Market Impact Conditional on Order-Flow Imbalance"),
    ("1708.02715", "Bechler, Ludkovski — Order Flows and LOB Resiliency on the Meso-Scale"),
    ("1602.02735", "Bacry et al — Estimation of slowly decreasing Hawkes kernels (market impact)"),

    # === ADVERSE SELECTION & INFORMATION ===
    ("1301.3228", "Easley, López de Prado, O'Hara — VPIN and the Flash Crash"),
    # Glosten-Milgrom (1985) and Kyle (1985) — not on arXiv, use SSRN/JSTOR

    # === OPTIMAL EXECUTION ===
    ("0906.5132", "Almgren — Optimal execution with nonlinear impact functions"),
    ("1206.0603", "Guéant — Optimal execution and block trading (2012)"),
    ("2101.02778", "Cartea, Jaimungal — Optimal execution with stochastic delay"),

    # === ML + LOB ===
    ("1901.01642", "Tran, Pham, Luo — DeepLOB extensions / attention-based LOB"),
    ("2106.12420", "Briola et al — Deep RL for optimal execution"),
    ("2010.01797", "Lucchese et al — Deep learning prediction of LOB mid-price"),

    # === VOLATILITY & MICROSTRUCTURE NOISE ===
    ("1709.04743", "Ait-Sahalia, Xiu — High-frequency covariance estimation"),

    # === RECENT (2025-2026) — state of the art ===
    ("2511.20606", "LOB Dynamics in Matching Markets — Microstructure framework (2025)"),
    ("2512.18648", "Optimal Signal Extraction from Order Flow — matched filter perspective (2025)"),
    ("2502.15757", "TLOB: Transformer with Dual Attention for LOB price prediction (2025)"),
    ("2506.05764", "Microstructural Dynamics in Crypto LOBs — better inputs > deeper models (2025)"),
    ("2505.05784", "FlowHFT: Imitation Learning for Optimal HFT (2025)"),

    # === EUREX / EUROPEAN EXCHANGE MICROSTRUCTURE ===
    ("2401.10722", "Stylized Facts and Market Microstructure — German Bond Futures / Eurex (2024)"),
    ("1706.03411", "Hawkes Microstructure Model — DAX & Bund futures on Eurex (2017)"),
    ("1705.01446", "Algorithmic trading in a microstructural limit order book model"),
    ("2312.08927", "LOB Dynamics and Order Size Modelling — Compound Hawkes Process"),

    # === HKEX / ASIAN EXCHANGE MICROSTRUCTURE ===
    ("1709.02015", "The Microstructure of High Frequency Markets (2017)"),
]

# Papers not on arXiv — fetch from Semantic Scholar by title
SEED_PAPERS_NON_ARXIV = [
    "Deep order flow imbalance: Extracting alpha at multiple horizons from the limit order book",  # Kolm et al 2021
    "The microprice: A model for the dynamics of the limit order book",  # Gatheral, Oomen
    "A Stochastic Model for Order Book Dynamics",  # Cont, Stoikov, Talreja 2010
    "Market Microstructure in Practice",  # Lehalle, Laruelle (book, chapters may be on SSRN)
    "Bid, Ask, and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders",  # Glosten-Milgrom 1985
    "Continuous Auctions and Insider Trading",  # Kyle 1985
    "Multi-level order-flow imbalance in a limit order book",  # Xu, Gould, Howison 2018
    "Microstructure of the Chinese stock market: A historical review",  # covers HKEX-adjacent markets
    "Order Flow Decomposition for Price Impact Analysis in Equity Limit Order Books",  # ACM ICAIF 2023
    "Data-Driven Trade Flow Decomposition for Exchange-Traded Funds",  # ACM ICAIF 2025
]


# =============================================================================
# Semantic Scholar expansion config
# =============================================================================

SEMANTIC_SCHOLAR_CONFIG = {
    # For each seed paper, fetch:
    "max_citations": 50,        # Papers that cite it (newer work building on it)
    "max_references": 20,       # Papers it cites (foundational work)

    # Filter expanded papers by relevance:
    "min_citation_count": 5,    # Skip obscure papers with < 5 citations
    "require_keywords": True,   # Must match at least one TIER1 or TIER2 keyword
    "max_age_years": 15,        # Skip papers older than 2011

    # Recommendation API — find similar papers
    "use_recommendations": True,
    "recommendation_limit": 20,  # Per seed paper
}


# =============================================================================
# Daily fetch config
# =============================================================================

DAILY_FETCH_CONFIG = {
    "max_papers_per_day": 10,    # Max papers to auto-ingest per day
    "lookback_days": 1,          # How many days back to check (1 = yesterday)
    "auto_ingest_tier1": True,   # Tier 1 matches: auto-download & convert
    "auto_ingest_tier2": True,   # Tier 2 matches in primary categories: auto-download
    "flag_tier3": True,          # Tier 3 matches: log but don't download
    "notify_on_finds": True,     # Print summary of new papers found
}
