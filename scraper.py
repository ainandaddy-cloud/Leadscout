"""
========================================================
  Google Maps Lead Scraper — Auto-Enriched Edition
========================================================
  Everything is automatic:
  - Scrapes Maps data
  - Detects owner name (website + Google + JustDial)
  - Generates owner email guesses
  - Creates WhatsApp links
  - Finds LinkedIn profiles
  - Detects social media, chatbot, dev opportunity
  - Deduplicates across all runs
  - Saves enriched CSV ready for Google Sheets

  RUN:
    python scraper.py              (uses config.py)
    python scraper.py config2.py   (uses another config)
========================================================
"""

import asyncio
import os
import sys
import importlib.util
import random
from playwright.async_api import async_playwright
from utils import (
    analyze_website,
    auto_enrich,
    deduplicate,
    save_to_csv,
    print_banner,
    sanitize_filename,
    load_seen_leads,
    save_seen_leads,
    filter_new_leads,
)


def load_config(config_path="config.py"):
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config


async def goto_with_retry(page, url, retries=3, timeout=30000):
    """Navigate with automatic retry on timeout."""
    for attempt in range(1, retries + 1):
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            return True
        except Exception:
            if attempt < retries:
                wait = attempt * 8
                print(f"    ⚠️  Attempt {attempt} failed. Retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                return False
    return False


async def scroll_results(page, scroll_rounds=20):
    """Scroll the results panel until all listings load."""
    try:
        feed = page.locator('div[role="feed"]')
        prev_count = 0
        same_streak = 0

        for _ in range(scroll_rounds):
            await feed.evaluate("el => el.scrollTop = el.scrollHeight")
            # Slightly faster adaptive wait keeps completeness but reduces idle time.
            await page.wait_for_timeout(1400)
            cards = page.locator('div[role="feed"] > div > div[jsaction]')
            count = await cards.count()

            if count == prev_count:
                same_streak += 1
                if same_streak >= 3:
                    break
            else:
                same_streak = 0
                print(f"    ↳ Loaded {count} listings...")
            prev_count = count

        return page.locator('div[role="feed"] > div > div[jsaction]')
    except Exception as e:
        print(f"  ⚠️  Scroll error: {e}")
        return None


async def extract_social_from_maps(page):
    """Extract social media links directly from Maps listing page."""
    socials = {
        "Facebook": "", "Instagram": "",
        "Twitter": "", "LinkedIn": "", "YouTube": ""
    }
    try:
        links = await page.locator('a[href]').all()
        for link in links:
            href = await link.get_attribute("href") or ""
            h = href.lower()
            if "facebook.com" in h and not socials["Facebook"]:
                socials["Facebook"] = href
            elif "instagram.com" in h and not socials["Instagram"]:
                socials["Instagram"] = href
            elif ("twitter.com" in h or "x.com" in h) and not socials["Twitter"]:
                socials["Twitter"] = href
            elif "linkedin.com" in h and not socials["LinkedIn"]:
                socials["LinkedIn"] = href
            elif "youtube.com" in h and not socials["YouTube"]:
                socials["YouTube"] = href
    except:
        pass
    return socials


async def extract_listing(page, url, profession):
    """
    Full extraction for one Maps listing.
    Includes auto-enrichment: owner, WhatsApp, LinkedIn, emails.
    """
    result = {
        "Name": "", "Category": "", "Rating": "", "Reviews": "",
        "Address": "", "Phone": "", "Website": "", "Email": "",
        "Owner_Name": "", "Owner_Email_Guesses": "",
        "WhatsApp_Link": "", "Owner_LinkedIn": "",
        "Facebook": "", "Instagram": "", "Twitter": "",
        "LinkedIn": "", "YouTube": "",
        "Has_Chatbot": "", "Has_Form": "",
        "Mobile_Friendly": "", "Dev_Opportunity": "",
        "Website Status": "Not Listed",
        "Maps URL": url, "Profession": profession,
    }

    try:
        success = await goto_with_retry(page, url, retries=3, timeout=30000)
        if not success:
            return result

        await page.wait_for_timeout(random.randint(1500, 2500))

        # ── Maps Data ───────────────────────────────────
        try:
            result["Name"] = await page.locator('h1.DUwDvf').inner_text(timeout=5000)
        except:
            pass

        try:
            result["Rating"] = await page.locator(
                'div.F7nice span[aria-hidden="true"]'
            ).first.inner_text(timeout=3000)
        except:
            pass

        try:
            aria = await page.locator(
                'div.F7nice span[aria-label]'
            ).first.get_attribute("aria-label", timeout=3000)
            if aria:
                result["Reviews"] = aria.replace(" reviews", "").replace(" review", "").strip()
        except:
            pass

        try:
            result["Category"] = await page.locator(
                'button.DkEaL'
            ).first.inner_text(timeout=3000)
        except:
            pass

        try:
            addr = await page.locator(
                'button[data-item-id="address"]'
            ).get_attribute("aria-label", timeout=3000)
            if addr:
                result["Address"] = addr.replace("Address: ", "").strip()
        except:
            pass

        try:
            phone = await page.locator(
                'button[data-item-id^="phone:tel"]'
            ).get_attribute("aria-label", timeout=3000)
            if phone:
                result["Phone"] = phone.replace("Phone: ", "").strip()
        except:
            pass

        try:
            website = await page.locator(
                'a[data-item-id="authority"]'
            ).get_attribute("href", timeout=3000)
            if website:
                result["Website"] = website.strip()
                result["Website Status"] = "Present"
        except:
            pass

        # Social from Maps page
        socials = await extract_social_from_maps(page)
        result.update(socials)

        result["Maps URL"] = page.url

        # ── Website Analysis ────────────────────────────
        if result["Website"]:
            # Run blocking requests/BeautifulSoup work in a thread so async workers can progress.
            analysis = await asyncio.to_thread(analyze_website, result["Website"])
            result["Email"] = ", ".join(analysis["emails"]) if analysis["emails"] else ""
            result["Has_Chatbot"] = analysis["has_chatbot"]
            result["Has_Form"] = analysis["has_form"]
            result["Mobile_Friendly"] = analysis["mobile_friendly"]
            result["Dev_Opportunity"] = analysis["dev_opportunity"]

            # Fill social gaps from website
            for platform in ["Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube"]:
                if not result[platform] and analysis.get(platform):
                    result[platform] = analysis[platform]

        # ── Auto Enrichment ─────────────────────────────
        # Owner name, WhatsApp, email guesses, LinkedIn
        # Runs automatically — no manual step needed
        enriched = await asyncio.to_thread(
            auto_enrich,
            name=result["Name"],
            website=result["Website"],
            phone=result["Phone"],
            address=result["Address"],
        )
        result["Owner_Name"] = enriched.get("Owner_Name", "")
        result["Owner_Email_Guesses"] = enriched.get("Owner_Email_Guesses", "")
        result["WhatsApp_Link"] = enriched.get("WhatsApp_Link", "")

        # Use LinkedIn from enrichment if Maps/website didn't have it
        if not result["Owner_LinkedIn"]:
            result["Owner_LinkedIn"] = enriched.get("Owner_LinkedIn", "")

    except Exception as e:
        print(f"    ⚠️  Listing error: {e}")

    return result


def unique_preserve_order(urls):
    seen_urls = set()
    deduped = []
    for u in urls:
        if u and u not in seen_urls:
            seen_urls.add(u)
            deduped.append(u)
    return deduped


async def scrape_one_listing(context, url, profession, index, total, delay):
    """Scrape one listing in an isolated page so multiple workers can run safely."""
    page = await context.new_page()
    try:
        print(f"  [{index}/{total}] Scraping + enriching...")
        details = await extract_listing(page, url, profession)

        name = (details['Name'] or 'Unknown')[:28]
        phone = details['Phone'] or '—'
        owner = f"👤 {details['Owner_Name'][:20]}" if details['Owner_Name'] else "👤 —"
        web = '🌐' if details['Website'] else '❌'
        wa = '📱' if details['WhatsApp_Link'] else ''
        ig = '📸' if details['Instagram'] else ''
        print(f"      {name:<28} | {phone:<14} | {web} {wa}{ig} | {owner}")

        await page.wait_for_timeout(random.randint(int(delay * 0.6), int(delay * 1.0)))
        return details
    except Exception as e:
        print(f"      ⚠️  Failed: {e}")
        return None
    finally:
        await page.close()


async def scrape_query(
    browser,
    query,
    profession,
    all_results,
    seen,
    delay=1500,
    listing_concurrency=2,
    scroll_rounds=20,
):
    """Scrape one search query."""
    search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    context = await browser.new_context(
        locale="en-US",
        viewport={"width": 1280, "height": 800},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    )
    page = await context.new_page()

    print(f"\n{'='*55}")
    print(f"  🔍 Query: {query}")
    print(f"{'='*55}")

    try:
        success = await goto_with_retry(page, search_url, retries=3, timeout=30000)
        if not success:
            print(f"  ❌ Skipping after all retries: {query}")
            await context.close()
            return seen

        await page.wait_for_timeout(random.randint(2000, 4000))

        print(f"  📜 Scrolling...")
        cards = await scroll_results(page, scroll_rounds)
        if not cards:
            await context.close()
            return seen

        # Collect listing URLs
        listing_urls = []
        count = await cards.count()
        for i in range(count):
            try:
                card = cards.nth(i)
                link = card.locator("a").first
                href = await link.get_attribute("href")
                if href and "/maps/place/" in href:
                    listing_urls.append(href)
            except:
                continue

        listing_urls = unique_preserve_order(listing_urls)
        print(f"  🏢 Found {len(listing_urls)} listings")
        print(f"  ⚡ Workers: {listing_concurrency}\n")

        query_results = []
        sem = asyncio.Semaphore(max(1, int(listing_concurrency)))

        async def worker(i, target_url):
            async with sem:
                return await scrape_one_listing(
                    context,
                    target_url,
                    profession,
                    i,
                    len(listing_urls),
                    delay,
                )

        tasks = [
            asyncio.create_task(worker(i + 1, url))
            for i, url in enumerate(listing_urls)
        ]

        for finished in asyncio.as_completed(tasks):
            details = await finished
            if not details:
                continue
            details["Search Query"] = query
            query_results.append(details)

        # Filter against seen leads
        new_records, skipped, seen = filter_new_leads(query_results, seen)
        all_results.extend(new_records)
        print(f"\n  ✅ {len(new_records)} new | ⏭️  {skipped} already seen — skipped")

    except Exception as e:
        print(f"  ❌ Query failed: {query} — {e}")
    finally:
        await context.close()

    return seen


async def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.py"

    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)

    cfg = load_config(config_file)
    print_banner()

    if not cfg.SEARCH_QUERIES:
        print("❌ No queries found in SEARCH_QUERIES.")
        sys.exit(1)

    seen = load_seen_leads()

    print(f"  Config       : {config_file}")
    print(f"  Niche        : {cfg.NICHE}")
    print(f"  Profession   : {cfg.PROFESSION}")
    print(f"  Queries      : {len(cfg.SEARCH_QUERIES)}")
    print(f"  Headless     : {cfg.HEADLESS}")
    print(f"  Already seen : {len(seen)} businesses (skipped)")
    print(f"\n  Queries:")
    for q in cfg.SEARCH_QUERIES:
        print(f"    • {q}")
    print()

    all_results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=cfg.HEADLESS)

        listing_concurrency = max(1, int(getattr(cfg, "LISTING_CONCURRENCY", 2)))
        scroll_rounds = max(8, int(getattr(cfg, "SCROLL_ROUNDS", 20)))
        cooldown_min, cooldown_max = getattr(cfg, "QUERY_COOLDOWN_RANGE", (6, 12))

        for i, query in enumerate(cfg.SEARCH_QUERIES):
            print(f"\n  ── Query {i+1} of {len(cfg.SEARCH_QUERIES)} ──")
            seen = await scrape_query(
                browser, query, cfg.PROFESSION,
                all_results,
                seen,
                cfg.DELAY_BETWEEN_LISTINGS,
                listing_concurrency,
                scroll_rounds,
            )
            save_seen_leads(seen)

            if i < len(cfg.SEARCH_QUERIES) - 1:
                cooldown = random.randint(int(cooldown_min), int(cooldown_max))
                print(f"\n  ⏳ Cooldown {cooldown}s...")
                await asyncio.sleep(cooldown)

        await browser.close()

    if not all_results:
        print("\n✅ No new leads — all already scraped.")
        sys.exit(0)

    print(f"\n{'='*55}")
    print(f"  📊 New leads       : {len(all_results)}")
    cleaned = deduplicate(all_results)
    print(f"  🧹 After dedup     : {len(cleaned)}")

    filename = sanitize_filename(cfg.NICHE)
    output_path = save_to_csv(cleaned, filename)
    save_seen_leads(seen)

    owner_count = sum(1 for r in cleaned if r.get("Owner_Name"))
    wa_count = sum(1 for r in cleaned if r.get("WhatsApp_Link"))
    email_count = sum(1 for r in cleaned if r.get("Email") or r.get("Owner_Email_Guesses"))

    print(f"""
{'='*55}
  ✅ DONE — Fully Enriched CSV Ready!

  📁 File     : {output_path}
  👤 Owners   : {owner_count} / {len(cleaned)}
  📱 WhatsApp : {wa_count} / {len(cleaned)}
  📧 Emails   : {email_count} / {len(cleaned)}
  🧠 Total ever seen : {len(seen)}

  📌 Google Sheets: File → Import → Upload
{'='*55}
""")


if __name__ == "__main__":
    asyncio.run(main())