import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://99bookstores.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("div", class_="card__content")

book_data = []

for book in books:

    # Title
    title_tag = book.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    # Price
    price_tag = book.find("span", class_="price-item--regular")

    if price_tag:
        price = price_tag.get_text(strip=True)
    else:
        continue   # Skip if no valid price

    # Skip "No Price"
    if "No Price" in price:
        continue

    # Product Link
    link_tag = book.find("a")

    if link_tag and link_tag.get("href"):
        product_link = "https://99bookstores.com" + link_tag.get("href")
    else:
        product_link = "No Link"

    # Store data
    book_data.append({
        "Book Title": title,
        "Price": price,
        "Product Link": product_link
    })

# Create DataFrame
df = pd.DataFrame(book_data)

# Remove duplicates
df = df.drop_duplicates(subset=["Book Title"])

# Save CSV
#df.to_csv("clean_books.csv", index=False, encoding="utf-8")

# Save Excel
df.to_excel("clean_books.xlsx", index=False)

print("Cleaned dataset created successfully!")

print(df.head())