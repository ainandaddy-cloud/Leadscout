"""
========================================================
  CONFIG FILE — Edit this file to control the scraper
========================================================
  STEP 1: Set PROFESSION
  STEP 2: Set NICHE (output CSV filename)
  STEP 3: Set SEARCH_QUERIES using build_queries()
  STEP 4: Run: python scraper.py
========================================================
"""

from cities import build_queries, BANGALORE

# ── 1. PROFESSION ─────────────────────────────────────
# Change this one word to switch niche instantly
# Examples: "dentist" "gym" "lawyer" "restaurant" "salon"
#           "ca firm" "hospital" "clinic" "hotel" "spa"
PROFESSION = "dentist"

# ── 2. NICHE ──────────────────────────────────────────
# This becomes the CSV filename
NICHE = "dentists_bangalore"

# ── 3. SEARCH QUERIES ─────────────────────────────────
# build_queries() combines your city areas with profession
#
# Single city:
#   from cities import build_queries, DUBAI
#   SEARCH_QUERIES = build_queries(DUBAI, PROFESSION)
#
# Multiple cities:
#   from cities import build_queries, DUBAI, ABU_DHABI
#   SEARCH_QUERIES = build_queries(DUBAI + ABU_DHABI, PROFESSION)
#
# Entire region:
#   from cities import build_queries, ALL_GCC
#   SEARCH_QUERIES = build_queries(ALL_GCC, PROFESSION)
#
# Unknown / custom place:
#   SEARCH_QUERIES = ["dentist in Bhatkal", "dentist in Gokarna"]
#
SEARCH_QUERIES = build_queries(BANGALORE, PROFESSION)

# ── 4. SETTINGS ───────────────────────────────────────
HEADLESS               = False   # True = silent, False = watch browser
SCROLL_ROUNDS          = 20      # more = more results loaded
DELAY_BETWEEN_LISTINGS = 1500    # ms — increase to 3000 if blocked
LISTING_CONCURRENCY    = 2       # parallel listing workers (safe range: 1-3)
QUERY_COOLDOWN_RANGE   = (4, 8)  # seconds between queries