import asyncio
from typing import List, Optional
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .models import EggPrice


class WalmartScraper:
    """Scraper for Walmart's website to get egg prices."""

    BASE_URL = "https://www.walmart.com"
    SEARCH_URL = urljoin(BASE_URL, "/search")

    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    async def fetch_egg_prices(self) -> List[EggPrice]:
        """Fetch egg prices from Walmart."""
        async with aiohttp.ClientSession(headers=self.headers) as session:
            # Search for eggs
            params = {
                "q": "eggs",
                "cat_id": "976759",
                "sort": "price_low",
            }

            try:
                async with session.get(self.SEARCH_URL, params=params) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch data: {response.status}")

                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Find all product items
                    products = soup.find_all("div", {"data-item-id": True})

                    egg_prices = []
                    for product in products[:5]:  # Get top 5 results
                        try:
                            # Extract price
                            price_elem = product.find(
                                "div", {"class": "price-characteristic"}
                            )
                            if not price_elem:
                                continue

                            price = float(price_elem.text.strip().replace("$", ""))

                            # Extract title
                            title_elem = product.find("span", {"class": "normal"})
                            title = (
                                title_elem.text.strip()
                                if title_elem
                                else "Unknown Brand"
                            )

                            egg_prices.append(
                                EggPrice(
                                    date=datetime.now(),
                                    price=price,
                                    source="Walmart",
                                    notes=title,
                                )
                            )
                        except (ValueError, AttributeError) as e:
                            continue

                    return egg_prices

            except Exception as e:
                raise Exception(f"Error fetching egg prices: {str(e)}")


# Create a singleton instance
walmart_scraper = WalmartScraper()
