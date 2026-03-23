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
import time
import os
from pathlib import Path

# Add google maps root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def unique_preserve_order(urls):
    seen_urls = set()
    out = []
    for u in urls:
        if u and u not in seen_urls:
            seen_urls.add(u)
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

    with sync_playwright() as p:
        launch_kwargs = {
            "headless": True,
            "args": ["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"],
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

        # Navigate
        if not goto_with_retry(page, search_url, retries=3, timeout=30000):
            print(json.dumps({"type": "error", "data": "Failed to open Google Maps search URL"}), flush=True)
            browser.close()
            return

        page.wait_for_timeout(random.randint(1200, 2200))

        # Scroll + collect listing URLs
        urls = collect_listing_urls(page, rounds=15, wait_ms=1400)

        # Fallback pass for temporary block/throttle pages
        if len(urls) == 0:
            page.wait_for_timeout(random.randint(2200, 3200))
            if goto_with_retry(page, search_url, retries=1, timeout=30000):
                urls = collect_listing_urls(page, rounds=20, wait_ms=2000)

        print(json.dumps({"type": "count", "data": len(urls)}), flush=True)

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
                "Maps URL": url, "Profession": profession,
            }

            try:
                if not goto_with_retry(page, url, retries=2, timeout=20000):
                    continue
                page.wait_for_timeout(random.randint(700, 1300))

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
                except: pass

                result["Maps URL"] = page.url

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
                if result["Website"]:
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

            page.wait_for_timeout(random.randint(700, 1300))

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