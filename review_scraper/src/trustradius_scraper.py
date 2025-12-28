from utils import get_soup, parse_date

def get_trustradius_reviews(company, start_date, end_date):
    """Scrapes TrustRadius reviews with fallback."""
    base_url = f"https://www.trustradius.com/products/{company}/reviews"
    print(f"Fetching TrustRadius reviews from: {base_url}")

    soup = get_soup(base_url)
    results = []

    # FALLBACK
    if soup == "BLOCKED" or not soup or not soup.find_all("article"):
        print("   -> Switching to sample data for TrustRadius (Assignment Fallback).")
        sample_reviews = [
            {"title": "Trustworthy platform", "review": "Secure and scalable for enterprise.", "date": "2023-04-12"},
            {"title": "Solid performance", "review": "Uptime is great, rarely have issues.", "date": "2023-11-20"}
        ]
        for r in sample_reviews:
            r_date = parse_date(r["date"])
            if r_date and start_date <= r_date <= end_date:
                results.append({
                    "source": "TrustRadius",
                    "title": r["title"],
                    "review": r["review"],
                    "date": r["date"],
                    "additional_info": {"company": company, "note": "Sample data (Scraping Blocked)"}
                })
        return results

    # Real Scraping Logic
    review_articles = soup.find_all("article", class_="review")
    for article in review_articles:
        try:
            title_tag = article.find("div", class_="review-title")
            title = title_tag.get_text(strip=True) if title_tag else "TrustRadius Review"
            content_tag = article.find("div", class_="ugc")
            text = content_tag.get_text(strip=True) if content_tag else ""
            date_tag = article.find("div", class_="review-date")
            raw_date = date_tag.get_text(strip=True) if date_tag else None
            review_date = parse_date(raw_date)

            if review_date and start_date <= review_date <= end_date:
                results.append({
                    "source": "TrustRadius",
                    "title": title,
                    "review": text,
                    "date": review_date.strftime("%Y-%m-%d"),
                    "additional_info": {"company": company}
                })
        except Exception:
            continue
    return results