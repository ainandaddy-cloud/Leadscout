"""
standalone_scraper.py
=====================
This file runs as a SEPARATE PROCESS from FastAPI.
FastAPI calls it via subprocess — completely bypasses
the Windows + Python 3.13 + Playwright async conflict.

Usage (called by main.py internally):
  python standalone_scraper.py "dentist in Dubai Marina" "dentist" job_id123

Outputs each lead as a JSON line to stdout.
FastAPI reads stdout line by line and streams to browser.
"""

import sys
import json
import random
import os
from pathlib import Path

# Add google maps root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def extract_place_id(url):
    """Extract the place_id or normalized path from a Google Maps URL for dedup."""
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        # Google Maps place URLs look like:
        # /maps/place/NAME/data=...!...!PLACE_ID
        # We normalize by keeping only the path up to /data
        path = parsed.path
        # Strip query string and fragment
        return path.split("/data")[0] if "/data" in path else path
    except Exception:
        return url


def unique_preserve_order(urls):
    seen_ids = set()
    out = []
    for u in urls:
        if not u:
            continue
        key = extract_place_id(u)
        if key not in seen_ids:
            seen_ids.add(key)
            out.append(u)
    return out


def goto_with_retry(page, url, retries=3, timeout=30000):
    for attempt in range(1, retries + 1):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            return True
        except Exception:
            if attempt < retries:
                page.wait_for_timeout(900 * attempt)
            else:
                return False
    return False


def collect_listing_urls(page, rounds=15, wait_ms=1400):
    prev = 0
    streak = 0

    for _ in range(rounds):
        try:
            page.evaluate("""
                const feed = document.querySelector('div[role="feed"]');
                if (feed) feed.scrollTop = feed.scrollHeight;
            """)
            page.wait_for_timeout(wait_ms)
            cards = page.locator('div[role="feed"] > div > div[jsaction]').all()
            count = len(cards)
            if count == prev:
                streak += 1
                if streak >= 3:
                    break
            else:
                streak = 0
                prev = count
        except:
            break

    urls = []
    try:
        cards = page.locator('div[role="feed"] > div > div[jsaction]').all()
        for card in cards:
            try:
                href = card.locator("a").first.get_attribute("href")
                if href and "/maps/place/" in href:
                    urls.append(href)
            except:
                continue
    except:
        pass

    return unique_preserve_order(urls)


def page_looks_blocked(page):
    """Detect common Google block/interstitial signals."""
    try:
        title = (page.title() or "").lower()
    except Exception:
        title = ""

    text = ""
    try:
        text = (page.locator("body").inner_text(timeout=2500) or "").lower()
    except Exception:
        pass

    indicators = [
        "unusual traffic",
        "our systems have detected",
        "captcha",
        "sorry",
        "automated queries",
        "verify you are human",
        "recaptcha",
    ]

    haystack = f"{title}\n{text}"
    return any(k in haystack for k in indicators)


def scrape(query: str, profession: str, job_id: str):
    from playwright.sync_api import sync_playwright
    from utils import analyze_website, auto_enrich

    search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    # Optional proxy mode (disabled by default):
    #   LEADSCOUT_USE_SWIFTSHADOW=1
    #   LEADSCOUT_PROXY_COUNTRIES=IN,US
    #   LEADSCOUT_PROXY_PROTOCOL=http
    use_swiftshadow = str(os.getenv("LEADSCOUT_USE_SWIFTSHADOW", "0")).strip().lower() in ("1", "true", "yes", "on")
    proxy_cfg = None
    if use_swiftshadow:
        try:
            from swiftshadow.classes import ProxyInterface

            countries_raw = os.getenv("LEADSCOUT_PROXY_COUNTRIES", "")
            countries = [c.strip().upper() for c in countries_raw.split(",") if c.strip()]
            protocol = (os.getenv("LEADSCOUT_PROXY_PROTOCOL", "http") or "http").strip().lower()
            if protocol not in ("http", "https", "socks5"):
                protocol = "http"

            swift = ProxyInterface(countries=countries or None, protocol=protocol)
            proxy_value = swift.get().as_string()
            if proxy_value:
                proxy_cfg = {"server": proxy_value}
                print(json.dumps({"type": "info", "data": f"Using proxy: {proxy_value}"}), flush=True)
        except Exception as ex:
            print(json.dumps({"type": "info", "data": f"Swiftshadow unavailable/failure: {ex}"}), flush=True)

    fast_mode = str(os.getenv("LEADSCOUT_FAST_MODE", "0")).strip().lower() in ("1", "true", "yes", "on")
    enable_website_analysis = str(os.getenv("LEADSCOUT_ENABLE_WEBSITE_ANALYSIS", "0")).strip().lower() in ("1", "true", "yes", "on")
    enable_owner_enrich = str(os.getenv("LEADSCOUT_ENABLE_OWNER_ENRICH", "0")).strip().lower() in ("1", "true", "yes", "on")
    min_scroll_rounds = 12 if fast_mode else 20
    max_scroll_rounds = 20 if fast_mode else 30
    min_scroll_wait = 650 if fast_mode else 1200
    max_scroll_wait = 1150 if fast_mode else 2000
    min_detail_wait = 250 if fast_mode else 700
    max_detail_wait = 650 if fast_mode else 1300

    print(json.dumps({
        "type": "info",
        "data": (
            f"Scraper mode: {'FAST' if fast_mode else 'SAFE'} | "
            f"Website analysis: {'ON' if enable_website_analysis else 'OFF'} | "
            f"Owner enrich: {'ON' if enable_owner_enrich else 'OFF'}"
        )
    }), flush=True)

    with sync_playwright() as p:
        launch_kwargs = {
            "headless": True,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--disable-extensions",
                "--disable-background-networking",
            ],
        }
        if proxy_cfg:
            launch_kwargs["proxy"] = proxy_cfg

        browser = p.chromium.launch(**launch_kwargs)
        context = browser.new_context(
            locale="en-US",
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # SUPER LIGHTWEIGHT MODE: Block heavy resources to save RAM/CPU and bandwidth
        def intercept_route(route):
            if route.request.resource_type in ["image", "media", "font"]:
                route.abort()
            else:
                route.continue_()
        
        page.route("**/*", intercept_route)

        # Navigate
        if not goto_with_retry(page, search_url, retries=3, timeout=30000):
            print(json.dumps({"type": "error", "data": "Failed to open Google Maps search URL"}), flush=True)
            browser.close()
            return

        page.wait_for_timeout(random.randint(500, 1100) if fast_mode else random.randint(1200, 2200))

        if page_looks_blocked(page):
            print(json.dumps({
                "type": "blocked",
                "data": {"reason": "Block/CAPTCHA detected on Google Maps search page"}
            }), flush=True)
            browser.close()
            return

        # Scroll + collect listing URLs
        urls = collect_listing_urls(
            page,
            rounds=random.randint(min_scroll_rounds, max_scroll_rounds),
            wait_ms=random.randint(min_scroll_wait, max_scroll_wait),
        )

        # Fallback pass for temporary block/throttle pages
        if len(urls) == 0:
            page.wait_for_timeout(random.randint(1800, 2800))
            if goto_with_retry(page, search_url, retries=1, timeout=30000):
                if page_looks_blocked(page):
                    print(json.dumps({
                        "type": "blocked",
                        "data": {"reason": "Google interstitial detected during fallback"}
                    }), flush=True)
                    browser.close()
                    return
                urls = collect_listing_urls(
                    page,
                    rounds=max_scroll_rounds,
                    wait_ms=max_scroll_wait,
                )

        if len(urls) == 0 and page_looks_blocked(page):
            print(json.dumps({
                "type": "blocked",
                "data": {"reason": "No listings due to probable temporary block"}
            }), flush=True)
            browser.close()
            return

        print(json.dumps({"type": "count", "data": len(urls)}), flush=True)

        # Internal deduplication set — prevent yielding same business twice
        scraped_keys = set()

        def make_scraper_key(name, phone, address):
            """Create a dedup key from normalized fields."""
            import re as _re
            clean_phone = _re.sub(r"[^0-9]", "", str(phone or ""))
            if len(clean_phone) >= 6:
                return f"phone::{clean_phone}"
            clean_name = str(name or "").strip().lower()
            clean_addr = str(address or "").strip().lower()
            return f"name::{clean_name}::addr::{clean_addr}"

        # Scrape each listing
        for i, url in enumerate(urls):
            result = {
                "Name": "", "Category": "", "Rating": "", "Reviews": "",
                "Address": "", "Phone": "", "Website": "", "Email": "",
                "Owner_Name": "", "Owner_Email_Guesses": "", "WhatsApp_Link": "",
                "Owner_LinkedIn": "", "Facebook": "", "Instagram": "",
                "Twitter": "", "LinkedIn": "", "YouTube": "",
                "Has_Chatbot": "", "Has_Form": "", "Mobile_Friendly": "",
                "Dev_Opportunity": "", "Website Status": "Not Listed",
                "has_website": False,
                "Maps URL": url, "Profession": profession,
            }

            try:
                if not goto_with_retry(page, url, retries=2, timeout=20000):
                    continue
                page.wait_for_timeout(random.randint(min_detail_wait, max_detail_wait))

                if page_looks_blocked(page):
                    print(json.dumps({
                        "type": "blocked",
                        "data": {"reason": "Blocked while opening listing details"}
                    }), flush=True)
                    browser.close()
                    return

                try: result["Name"]     = page.locator('h1.DUwDvf').first.inner_text(timeout=4000)
                except: pass
                try: result["Category"] = page.locator('button.DkEaL').first.inner_text(timeout=3000)
                except: pass
                try: result["Rating"]   = page.locator('div.F7nice span[aria-hidden="true"]').first.inner_text(timeout=3000)
                except: pass
                try:
                    aria = page.locator('div.F7nice span[aria-label]').first.get_attribute("aria-label", timeout=3000)
                    if aria: result["Reviews"] = aria.replace(" reviews","").replace(" review","").strip()
                except: pass
                try:
                    addr = page.locator('button[data-item-id="address"]').get_attribute("aria-label", timeout=3000)
                    if addr: result["Address"] = addr.replace("Address: ","").strip()
                except: pass
                try:
                    phone = page.locator('button[data-item-id^="phone:tel"]').get_attribute("aria-label", timeout=3000)
                    if phone: result["Phone"] = phone.replace("Phone: ","").strip()
                except: pass
                try:
                    website = page.locator('a[data-item-id="authority"]').get_attribute("href", timeout=3000)
                    if website:
                        result["Website"]        = website.strip()
                        result["Website Status"] = "Present"
                        result["has_website"]    = True
                except: pass

                result["Maps URL"] = page.url

                # DEDUP CHECK: Skip if we've already yielded this business
                lead_key = make_scraper_key(result["Name"], result["Phone"], result["Address"])
                if lead_key in scraped_keys:
                    continue
                scraped_keys.add(lead_key)

                # Socials
                try:
                    for a in page.locator('a[href]').all():
                        href = (a.get_attribute("href") or "").lower()
                        if "facebook.com"  in href and not result["Facebook"]:  result["Facebook"]  = href
                        elif "instagram.com" in href and not result["Instagram"]: result["Instagram"] = href
                        elif "youtube.com"   in href and not result["YouTube"]:   result["YouTube"]   = href
                        elif "twitter.com"   in href and not result["Twitter"]:   result["Twitter"]   = href
                        elif "linkedin.com"  in href and not result["LinkedIn"]:  result["LinkedIn"]  = href
                except: pass

                # Website enrichment
                if result["Website"] and enable_website_analysis:
                    try:
                        analysis = analyze_website(result["Website"])
                        result["Email"]           = ", ".join(analysis["emails"]) if analysis["emails"] else ""
                        result["Has_Chatbot"]     = analysis["has_chatbot"]
                        result["Has_Form"]        = analysis["has_form"]
                        result["Mobile_Friendly"] = analysis["mobile_friendly"]
                        result["Dev_Opportunity"] = analysis["dev_opportunity"]
                        for pl in ["Facebook","Instagram","Twitter","LinkedIn","YouTube"]:
                            if not result[pl] and analysis.get(pl):
                                result[pl] = analysis[pl]
                    except: pass

                # Owner enrichment
                if enable_owner_enrich:
                    try:
                        enriched = auto_enrich(result["Name"], result["Website"], result["Phone"], result["Address"])
                        result["Owner_Name"]          = enriched.get("Owner_Name", "")
                        result["Owner_Email_Guesses"] = enriched.get("Owner_Email_Guesses", "")
                        result["WhatsApp_Link"]        = enriched.get("WhatsApp_Link", "")
                        result["Owner_LinkedIn"]       = enriched.get("Owner_LinkedIn", "")
                    except: pass

                if result.get("Name"):
                    print(json.dumps({"type": "lead", "data": result}), flush=True)

            except Exception as e:
                pass

            page.wait_for_timeout(random.randint(min_detail_wait, max_detail_wait))

        browser.close()
        print(json.dumps({"type": "done", "data": len(urls)}), flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"type": "error", "data": "Usage: standalone_scraper.py query profession job_id"}), flush=True)
        sys.exit(1)

    query      = sys.argv[1]
    profession = sys.argv[2]
    job_id     = sys.argv[3]

    scrape(query, profession, job_id)