import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

SCALE_SERP_API_KEY = "DB22AD69EF944A96B71149EBB2787714"

def search_prices(restaurant_name):
    search_url = f"https://api.scaleserp.com/search?api_key={SCALE_SERP_API_KEY}&q=site:fastfoodmenuprices.com+{restaurant_name.replace(' ', '+')}+menu+prices&location=United+States"

    response = requests.get(search_url)
    search_results = response.json()

    menu_url = None
    best_match_score = 0

    # Find the best matching menu page
    for result in search_results.get("organic_results", []):
        title, url = result["title"], result["link"]
        similarity_score = fuzz.partial_ratio(f"{restaurant_name} Menu Prices".lower(), title.lower())
        if similarity_score > best_match_score:
            best_match_score = similarity_score
            menu_url = url

    if not menu_url:
        print(f"Could not find a valid menu page for {restaurant_name}.")
        return {}  # Return empty dictionary instead of exiting

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(menu_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch menu for {restaurant_name}. HTTP Status: {response.status_code}")
        return {}  # Return empty dictionary instead of exiting

    soup = BeautifulSoup(response.text, "html.parser")
    menu_prices = {}

    tables = soup.find_all("table")

    for table in tables:
        for row in table.select("tbody tr"):
            columns = row.find_all("td")
            if len(columns) >= 2:
                name = columns[0].text.strip()
                possible_prices = [col.text.strip() for col in columns if "$" in col.text]

                if possible_prices:
                    raw_price = possible_prices[0]

                    try:
                        cleaned_price = raw_price.replace("$", "").replace(",", "").strip()
                        price = float(cleaned_price)
                        menu_prices[name] = price
                    except ValueError:
                        print(f"Skipping invalid price format: '{raw_price}' for item '{name}'")

    if not menu_prices:
        print(f"No menu items found for {restaurant_name}.")

    return menu_prices 

menu_data = search_prices("Chick-fil-A")
print(menu_data)
