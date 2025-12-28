import json
import os
from datetime import datetime
from g2_scraper import get_g2_reviews
from capterra_scraper import get_capterra_reviews
from trustradius_scraper import get_trustradius_reviews

def validate_date(date_str):
    """Validates date format YYYY-MM-DD."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def main():
    print("--- SaaS Review Scraper ---")
    
    # 1. Input Parameters [cite: 11]
    company = input("Enter company slug (e.g., slack, asana): ").strip().lower()
    
    # Input validation for source
    valid_sources = ["g2", "capterra", "trustradius", "all"]
    source = input("Source (g2 / capterra / trustradius / all): ").strip().lower()
    while source not in valid_sources:
        print("Invalid source.")
        source = input("Source: ").strip().lower()

    # Input validation for dates [cite: 29]
    start = input("Start date (YYYY-MM-DD): ").strip()
    start_date = validate_date(start)
    while not start_date:
        print("Invalid format. Use YYYY-MM-DD")
        start = input("Start date (YYYY-MM-DD): ").strip()
        start_date = validate_date(start)

    end = input("End date (YYYY-MM-DD): ").strip()
    end_date = validate_date(end)
    while not end_date:
        print("Invalid format. Use YYYY-MM-DD")
        end = input("End date (YYYY-MM-DD): ").strip()
        end_date = validate_date(end)

    reviews = []
    
    # Logic to handle single or all sources
    sources_to_scrape = [source] if source != "all" else ["g2", "capterra", "trustradius"]

    print(f"\nStarting scrape for {company}...")

    # Fetching content
    if "g2" in sources_to_scrape:
        reviews.extend(get_g2_reviews(company, start_date, end_date))
    
    if "capterra" in sources_to_scrape:
        reviews.extend(get_capterra_reviews(company, start_date, end_date))
        
    if "trustradius" in sources_to_scrape:
        reviews.extend(get_trustradius_reviews(company, start_date, end_date))

    # Output to JSON [cite: 17]
    os.makedirs("output", exist_ok=True)
    output_file = "output/reviews.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Completed. {len(reviews)} reviews saved to {output_file}")

if __name__ == "__main__":
    main()