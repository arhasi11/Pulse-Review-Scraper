from utils import get_soup, parse_date

def get_capterra_reviews(company, start_date, end_date):
    """Scrapes Capterra reviews with fallback for 403 blocks."""
    base_url = f"https://www.capterra.com/software/{company}" 
    print(f"Fetching Capterra reviews from: {base_url}")

    soup = get_soup(base_url)
    results = []

    # FALLBACK
    if soup == "BLOCKED" or not soup:
        print("   -> Switching to sample data for Capterra (Assignment Fallback).")
        sample_reviews = [
            {"title": "Essential for remote work", "review": "Can't imagine working without it.", "date": "2023-06-10", "rating": "5/5"},
            {"title": "Good UI", "review": "Very intuitive interface.", "date": "2023-09-01", "rating": "4/5"}
        ]
        for r in sample_reviews:
            r_date = parse_date(r["date"])
            if r_date and start_date <= r_date <= end_date:
                results.append({
                    "source": "Capterra",
                    "title": r["title"],
                    "review": r["review"],
                    "date": r["date"],
                    "additional_info": {"rating": r["rating"], "note": "Sample data (Scraping Blocked)"}
                })
        return results

    # Real Scraping Logic
    review_cards = soup.find_all("div", class_="review-card") 
    for card in review_cards:
        try:
            title_tag = card.find("h3", class_="review-card-title")
            title = title_tag.get_text(strip=True) if title_tag else "Review"

            text_tag = card.find("p", class_="review-card-text")
            text = text_tag.get_text(strip=True) if text_tag else ""

            date_tag = card.find("div", class_="review-date")
            raw_date = date_tag.get_text(strip=True).replace("Written on", "") if date_tag else None
            review_date = parse_date(raw_date)

            rating_tag = card.find("div", class_="star-rating")
            rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

            if review_date and start_date <= review_date <= end_date:
                results.append({
                    "source": "Capterra",
                    "title": title,
                    "review": text[:200] + "...", 
                    "date": review_date.strftime("%Y-%m-%d"),
                    "additional_info": {"rating": rating}
                })
        except Exception:
            continue
    return results