"""
utils.py — All helper + enrichment functions
Everything runs automatically during scraping.
No manual steps needed.
"""

import os
import re
import json
import time
import random
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

SEEN_LEADS_FILE = "seen_leads.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Seen Leads (Deduplication Memory) ──────────────────

def load_seen_leads():
    if os.path.exists(SEEN_LEADS_FILE):
        with open(SEEN_LEADS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_seen_leads(seen):
    with open(SEEN_LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=2)


def make_lead_key(record):
    phone = str(record.get("Phone", "")).strip()
    name = str(record.get("Name", "")).strip().lower()
    address = str(record.get("Address", "")).strip().lower()
    if phone:
        return f"phone::{phone}"
    return f"name::{name}::addr::{address}"


def filter_new_leads(records, seen):
    new_records = []
    skipped = 0
    for record in records:
        key = make_lead_key(record)
        if key in seen:
            skipped += 1
        else:
            seen.add(key)
            new_records.append(record)
    return new_records, skipped, seen


# ── Web Fetching ────────────────────────────────────────

def fetch_url(url, timeout=8):
    """Safe URL fetch — returns (soup, raw_text) or (None, '')"""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        res = requests.get(url, headers=HEADERS, timeout=timeout)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup, res.text
    except:
        return None, ""


def get_domain(url):
    """Extract clean domain from URL."""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ""


# ── Owner Name Detection ────────────────────────────────

OWNER_PATTERNS = [
    # Titles before name
    r"(?:Dr\.?|Doctor|Prof\.?|Mr\.?|Mrs\.?|Ms\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
    # Role before name
    r"(?:Owner|Founder|Director|CEO|MD|Principal|Proprietor|Head\s+of|Chief)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
    # Founded/Started by
    r"(?:Founded|Started|Established|Run|Managed)\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
    # "Meet Dr/Our" pattern
    r"Meet\s+(?:Dr\.?\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
    # About section name intro
    r"I\s+am\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
    r"My\s+name\s+is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
]


def extract_owner_from_text(text):
    """Extract owner name from any text block."""
    for pattern in OWNER_PATTERNS:
        matches = re.findall(pattern, text)
        for name in matches:
            name = name.strip()
            # Validate: 2+ words, no numbers, not too long
            words = name.split()
            if 2 <= len(words) <= 4 and not any(c.isdigit() for c in name):
                # Skip common false positives
                skip = ["About Us", "Contact Us", "Our Team", "Our Services",
                        "Read More", "Learn More", "Click Here", "Find Out"]
                if not any(s.lower() in name.lower() for s in skip):
                    return name
    return ""


def find_about_pages(base_url, soup):
    """Find About/Contact/Team subpages."""
    if not soup:
        return []
    keywords = ["about", "contact", "team", "founder", "doctor",
                 "our-story", "who-we-are", "staff", "meet"]
    found = []
    try:
        base_domain = urlparse(base_url).netloc
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            text = a.get_text().lower().strip()
            if any(kw in href or kw in text for kw in keywords):
                full = urljoin(base_url, a["href"])
                if base_domain in full:
                    found.append(full)
    except:
        pass
    return list(set(found))[:3]


def find_owner_from_website(website_url):
    """
    Search website main page + about/contact pages for owner name.
    Returns name string or empty string.
    """
    if not website_url:
        return ""

    # Check main page
    soup, _ = fetch_url(website_url)
    if soup:
        owner = extract_owner_from_text(soup.get_text())
        if owner:
            return owner

        # Check about/team pages
        about_pages = find_about_pages(website_url, soup)
        for page_url in about_pages:
            about_soup, _ = fetch_url(page_url)
            if about_soup:
                owner = extract_owner_from_text(about_soup.get_text())
                if owner:
                    return owner

    return ""


def find_owner_from_google(business_name, address=""):
    """
    Search Google for owner name using business name.
    Tries multiple search patterns.
    """
    queries = [
        f'"{business_name}" owner',
        f'"{business_name}" founder',
        f'"{business_name}" director',
        f'"{business_name}" {address[:20] if address else ""} owner'.strip(),
    ]

    for query in queries[:2]:  # limit to 2 to avoid rate limiting
        try:
            url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
            soup, text = fetch_url(url)
            if soup:
                # Check snippets / knowledge panel
                for el in soup.find_all(["span", "div", "p"]):
                    snippet = el.get_text()
                    if len(snippet) > 20 and len(snippet) < 500:
                        owner = extract_owner_from_text(snippet)
                        if owner and business_name.split()[0].lower() not in owner.lower():
                            return owner
            time.sleep(random.uniform(1, 2))
        except:
            pass

    return ""


def find_owner_from_justdial(business_name, city=""):
    """JustDial — India only."""
    try:
        query = f"{business_name} {city}"
        url = f"https://www.justdial.com/search?q={requests.utils.quote(query)}"
        soup, _ = fetch_url(url)
        if soup:
            owner = extract_owner_from_text(soup.get_text())
            if owner:
                return owner
    except:
        pass
    return ""


def find_owner_from_yelp(business_name, address=""):
    """
    Yelp — USA, Canada, UK, Australia.
    Business pages often list owner name in reviews/about.
    """
    try:
        query = f"{business_name} {address[:30]}"
        url = f"https://www.yelp.com/search?find_desc={requests.utils.quote(query)}"
        soup, _ = fetch_url(url)
        if not soup:
            return ""
        # Find first business link
        for a in soup.find_all("a", href=True):
            if "/biz/" in a["href"]:
                biz_url = "https://www.yelp.com" + a["href"] if a["href"].startswith("/") else a["href"]
                biz_soup, _ = fetch_url(biz_url)
                if biz_soup:
                    owner = extract_owner_from_text(biz_soup.get_text())
                    if owner:
                        return owner
                break
    except:
        pass
    return ""


def find_owner_from_yellow_pages(business_name, address=""):
    """
    Yellow Pages — USA, Canada, Australia.
    Lists owner/manager names for many businesses.
    """
    try:
        query = f"{business_name} {address[:30]}"
        url = f"https://www.yellowpages.com/search?search_terms={requests.utils.quote(query)}"
        soup, _ = fetch_url(url)
        if soup:
            owner = extract_owner_from_text(soup.get_text())
            if owner:
                return owner
    except:
        pass
    return ""


def find_owner_from_yell(business_name, address=""):
    """
    Yell.com — UK business directory.
    Often has owner/contact person listed.
    """
    try:
        query = f"{business_name}"
        url = f"https://www.yell.com/ucs/UcsSearchAction.do?keywords={requests.utils.quote(query)}"
        soup, _ = fetch_url(url)
        if soup:
            owner = extract_owner_from_text(soup.get_text())
            if owner:
                return owner
    except:
        pass
    return ""


def find_owner_from_hotfrog(business_name, address=""):
    """
    Hotfrog — Australia, NZ, UK, US, Canada.
    Global business directory with contact details.
    """
    try:
        query = f"{business_name}"
        url = f"https://www.hotfrog.com.au/search/{requests.utils.quote(query)}"
        soup, _ = fetch_url(url)
        if soup:
            owner = extract_owner_from_text(soup.get_text())
            if owner:
                return owner
    except:
        pass
    return ""


def find_owner_from_zomato_sulekha(business_name, address=""):
    """
    Sulekha — India, UAE.
    Zomato — restaurants India/UAE.
    """
    for base_url in [
        f"https://www.sulekha.com/search?keywords={requests.utils.quote(business_name)}",
    ]:
        try:
            soup, _ = fetch_url(base_url)
            if soup:
                owner = extract_owner_from_text(soup.get_text())
                if owner:
                    return owner
        except:
            pass
    return ""


def find_owner_from_trustpilot(business_name):
    """
    Trustpilot — global.
    Company pages sometimes show owner response names.
    """
    try:
        url = f"https://www.trustpilot.com/search?query={requests.utils.quote(business_name)}"
        soup, _ = fetch_url(url)
        if soup:
            owner = extract_owner_from_text(soup.get_text())
            if owner:
                return owner
    except:
        pass
    return ""


def find_owner_from_gulf_directories(business_name, address=""):
    """
    Gulf-specific directories: Dubai Yellow Pages, UAE Business Directory.
    For UAE, Qatar, Saudi, Bahrain, Kuwait, Oman.
    """
    sources = [
        f"https://www.yellowpages.ae/search/{requests.utils.quote(business_name)}",
        f"https://www.uaeyellowpages.com/search?q={requests.utils.quote(business_name)}",
        f"https://www.dubaipages.com/search?q={requests.utils.quote(business_name)}",
    ]
    for url in sources:
        try:
            soup, _ = fetch_url(url)
            if soup:
                owner = extract_owner_from_text(soup.get_text())
                if owner:
                    return owner
        except:
            pass
    return ""


def detect_region(address):
    """
    Detect which region a business is in based on address.
    Returns: 'india', 'gcc', 'uk', 'usa', 'australia', 'canada', 'europe', 'other'
    """
    if not address:
        return "other"
    addr = address.lower()

    india_cities = [
        "mumbai", "delhi", "bangalore", "hyderabad", "chennai",
        "pune", "kolkata", "jaipur", "ahmedabad", "surat", "lucknow",
        "nagpur", "bhopal", "indore", "kochi", "chandigarh", "bhatkal",
        "mangalore", "udupi", "india"
    ]
    gcc_keywords = [
        "dubai", "abu dhabi", "sharjah", "ajman", "uae",
        "riyadh", "jeddah", "saudi", "kuwait", "doha", "qatar",
        "bahrain", "muscat", "oman"
    ]
    uk_keywords = ["london", "manchester", "birmingham", "glasgow",
                   "edinburgh", "united kingdom", "uk", " england", "wales", "scotland"]
    usa_keywords = ["new york", "los angeles", "chicago", "houston",
                    "dallas", "miami", "san francisco", "usa", "united states", "ca ", "ny "]
    australia_keywords = ["sydney", "melbourne", "brisbane", "perth",
                          "adelaide", "australia", "nsw", "victoria", "queensland"]
    canada_keywords = ["toronto", "vancouver", "calgary", "montreal",
                       "ottawa", "canada", "ontario", "british columbia"]

    if any(c in addr for c in india_cities):
        return "india"
    if any(c in addr for c in gcc_keywords):
        return "gcc"
    if any(c in addr for c in uk_keywords):
        return "uk"
    if any(c in addr for c in usa_keywords):
        return "usa"
    if any(c in addr for c in australia_keywords):
        return "australia"
    if any(c in addr for c in canada_keywords):
        return "canada"
    return "other"


def find_owner_smart(business_name, website, address, phone):
    """
    Smart owner detection with region-aware source selection.

    Priority order:
    1. Website (universal — most reliable)
    2. Google search (universal)
    3. Region-specific directories:
       India  → JustDial, Sulekha
       UAE    → Dubai Yellow Pages, UAE directories
       UK     → Yell.com
       USA    → Yelp, Yellow Pages
       AUS/NZ → Hotfrog, Yellow Pages AU
       Canada → Yelp, Yellow Pages
       Global → Trustpilot, Hotfrog
    """
    owner = ""
    region = detect_region(address)

    # ── Step 1: Website (works everywhere) ─────────────
    if website:
        owner = find_owner_from_website(website)
        if owner:
            return owner

    # ── Step 2: Google search (works everywhere) ────────
    owner = find_owner_from_google(business_name, address)
    if owner:
        return owner

    # ── Step 3: Region-specific directories ────────────
    time.sleep(random.uniform(0.5, 1.0))

    if region == "india":
        city = next((c.title() for c in [
            "mumbai", "delhi", "bangalore", "hyderabad", "chennai",
            "pune", "kolkata", "jaipur", "ahmedabad", "surat", "lucknow"
        ] if c in address.lower()), "")
        owner = find_owner_from_justdial(business_name, city)
        if owner:
            return owner
        owner = find_owner_from_zomato_sulekha(business_name, address)
        if owner:
            return owner

    elif region == "gcc":
        owner = find_owner_from_gulf_directories(business_name, address)
        if owner:
            return owner

    elif region == "uk":
        owner = find_owner_from_yell(business_name, address)
        if owner:
            return owner

    elif region in ("usa", "canada"):
        owner = find_owner_from_yelp(business_name, address)
        if owner:
            return owner
        owner = find_owner_from_yellow_pages(business_name, address)
        if owner:
            return owner

    elif region == "australia":
        owner = find_owner_from_hotfrog(business_name, address)
        if owner:
            return owner
        owner = find_owner_from_yelp(business_name, address)
        if owner:
            return owner

    else:
        # Unknown region — try global sources
        owner = find_owner_from_trustpilot(business_name)
        if owner:
            return owner
        owner = find_owner_from_hotfrog(business_name, address)
        if owner:
            return owner

    return ""


# ── Email Detection ──────────────────────────────────────

EMAIL_FORMATS = [
    "{first}@{domain}",
    "{first}.{last}@{domain}",
    "{first}{last}@{domain}",
    "{f}{last}@{domain}",
    "dr.{first}@{domain}",
    "dr{first}@{domain}",
    "info@{domain}",
    "contact@{domain}",
    "admin@{domain}",
    "hello@{domain}",
]

BLACKLIST_DOMAINS = [
    "example.com", "sentry.io", "wixpress.com", "squarespace.com",
    "wordpress.com", "google.com", "schema.org", "w3.org", "jquery.com",
    "facebook.com", "instagram.com", "twitter.com", "youtube.com",
]


def extract_emails_from_text(text):
    """Extract real emails from any text."""
    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )
    cleaned = []
    for e in emails:
        if not any(b in e for b in BLACKLIST_DOMAINS):
            cleaned.append(e.lower())
    return list(set(cleaned))[:3]


def guess_owner_emails(owner_name, domain):
    """Generate likely email formats from owner name + domain."""
    if not domain or not owner_name:
        return []
    parts = owner_name.lower().split()
    if len(parts) < 2:
        return []
    first = re.sub(r"[^a-z]", "", parts[0])
    last = re.sub(r"[^a-z]", "", parts[-1])
    f = first[0] if first else ""

    guesses = []
    for fmt in EMAIL_FORMATS:
        try:
            email = fmt.format(first=first, last=last, f=f, domain=domain)
            if "@" in email and "." in email.split("@")[1]:
                guesses.append(email)
        except:
            continue
    return list(set(guesses))


# ── WhatsApp Link ────────────────────────────────────────

def make_whatsapp_link(phone):
    """Generate WhatsApp click-to-chat link from phone number."""
    if not phone:
        return ""
    clean = re.sub(r"[^\d+]", "", str(phone))
    if not clean:
        return ""
    if not clean.startswith("+"):
        if clean.startswith("00"):
            clean = "+" + clean[2:]
        elif len(clean) == 10:
            clean = "+91" + clean
        elif len(clean) == 9:
            clean = "+971" + clean  # UAE
    return f"https://wa.me/{clean.replace('+', '')}"


# ── LinkedIn Search ──────────────────────────────────────

def find_linkedin(business_name, owner_name=""):
    """Search Google for LinkedIn profile."""
    try:
        query = owner_name if owner_name else business_name
        search = f'site:linkedin.com "{query}" "{business_name.split()[0]}"'
        url = f"https://www.google.com/search?q={requests.utils.quote(search)}"
        soup, text = fetch_url(url)
        if soup:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "linkedin.com/in/" in href or "linkedin.com/company/" in href:
                    match = re.search(r"linkedin\.com/(in|company)/[^&\"' ]+", href)
                    if match:
                        return "https://www." + match.group(0).rstrip("/")
    except:
        pass
    return ""


# ── Website Full Analysis ────────────────────────────────

def analyze_website(url):
    """
    Full website analysis:
    - Emails
    - Social media
    - Chatbot detection
    - Contact form
    - Mobile friendliness
    - Dev opportunity
    """
    result = {
        "emails": [],
        "has_chatbot": "No",
        "has_form": "No",
        "mobile_friendly": "No",
        "dev_opportunity": "No",
        "Facebook": "",
        "Instagram": "",
        "Twitter": "",
        "LinkedIn": "",
        "YouTube": "",
    }

    soup, html = fetch_url(url)
    if not soup:
        return result

    html_lower = html.lower()
    text = soup.get_text()

    # Emails
    result["emails"] = extract_emails_from_text(text)

    # Social media
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        h = href.lower()
        if "facebook.com" in h and not result["Facebook"]:
            result["Facebook"] = href
        elif "instagram.com" in h and not result["Instagram"]:
            result["Instagram"] = href
        elif ("twitter.com" in h or "x.com" in h) and not result["Twitter"]:
            result["Twitter"] = href
        elif "linkedin.com" in h and not result["LinkedIn"]:
            result["LinkedIn"] = href
        elif "youtube.com" in h and not result["YouTube"]:
            result["YouTube"] = href

    # Chatbot
    chatbot_signals = [
        "tidio", "intercom", "drift", "crisp", "tawk", "freshchat",
        "zendesk", "livechat", "olark", "hubspot", "chatbot",
        "chat-widget", "smartsupp", "jivochat", "purechat",
        "botpress", "manychat", "chatfuel", "landbot",
    ]
    has_chatbot = any(s in html_lower for s in chatbot_signals)
    result["has_chatbot"] = "Yes" if has_chatbot else "No"

    # Form
    result["has_form"] = "Yes" if soup.find_all("form") else "No"

    # Mobile
    viewport = soup.find("meta", attrs={"name": "viewport"})
    result["mobile_friendly"] = "Yes" if viewport else "No"

    # Dev opportunity
    result["dev_opportunity"] = "Yes" if (not has_chatbot or not viewport) else "No"

    return result


# ── Full Auto Enrichment (called during scraping) ────────

def auto_enrich(name, website, phone, address):
    """
    Runs all enrichment automatically for one lead.
    Called inside scraper — no manual step needed.
    Returns dict with all enriched fields.
    """
    enriched = {
        "Owner_Name": "",
        "Owner_Email_Guesses": "",
        "WhatsApp_Link": "",
        "Owner_LinkedIn": "",
    }

    # WhatsApp — always generate from phone
    enriched["WhatsApp_Link"] = make_whatsapp_link(phone)

    # Owner name — try all sources
    owner = find_owner_smart(name, website, address, phone)
    enriched["Owner_Name"] = owner

    # Owner email guesses
    if owner and website:
        domain = get_domain(website)
        guesses = guess_owner_emails(owner, domain)
        enriched["Owner_Email_Guesses"] = " | ".join(guesses[:4]) if guesses else ""

    # LinkedIn
    if owner or name:
        enriched["Owner_LinkedIn"] = find_linkedin(name, owner)

    return enriched


# ── CSV Save ────────────────────────────────────────────

def deduplicate(data):
    df = pd.DataFrame(data)
    original = len(df)
    df_with_phone = df[df["Phone"].str.strip() != ""]
    df_without_phone = df[df["Phone"].str.strip() == ""]
    df_with_phone = df_with_phone.drop_duplicates(subset=["Phone"], keep="first")
    df_without_phone = df_without_phone.drop_duplicates(
        subset=["Name", "Address"], keep="first"
    )
    result = pd.concat([df_with_phone, df_without_phone], ignore_index=True)
    removed = original - len(result)
    if removed > 0:
        print(f"  Removed {removed} duplicates")
    return result.to_dict(orient="records")


def save_to_csv(data, filename):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = os.path.join("output", f"{filename}_{timestamp}.csv")

    df = pd.DataFrame(data)

    column_order = [
        "Name", "Category", "Profession",
        "Rating", "Reviews",
        "Phone", "WhatsApp_Link",
        "Owner_Name", "Owner_Email_Guesses", "Owner_LinkedIn",
        "Email", "Address",
        "Website", "Website Status",
        "Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube",
        "Has_Chatbot", "Has_Form", "Mobile_Friendly", "Dev_Opportunity",
        "Maps URL", "Search Query",
    ]

    existing_cols = [c for c in column_order if c in df.columns]
    df = df[existing_cols]

    # No-website leads float to top
    df["_sort"] = df["Website Status"].apply(lambda x: 0 if x == "Not Listed" else 1)
    df = df.sort_values("_sort").drop(columns=["_sort"]).reset_index(drop=True)

    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    return filepath


def sanitize_filename(name):
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", name).lower().strip("_")


def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║         Google Maps Lead Scraper                     ║
║         Auto-Enriched — Zero Manual Work             ║
╚══════════════════════════════════════════════════════╝
""")