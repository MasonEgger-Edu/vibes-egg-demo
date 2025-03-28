from datetime import datetime
from typing import List

from temporalio import activity

from .models import EggPrice
from .scrapers import walmart_scraper


@activity.defn(name="fetch_egg_prices")
async def fetch_egg_prices() -> List[EggPrice]:
    """Fetch current egg prices from various sources."""
    try:
        # Fetch prices from Walmart
        walmart_prices = await walmart_scraper.fetch_egg_prices()

        # In a real implementation, you would fetch from multiple sources
        # and combine the results. For now, we'll just return Walmart prices.
        return walmart_prices

    except Exception as e:
        # Log the error and return a fallback price
        activity.logger.error(f"Error fetching egg prices: {str(e)}")
        return [
            EggPrice(
                date=datetime.now(),
                price=3.99,
                source="Fallback",
                notes="Using fallback price due to error",
            )
        ]


@activity.defn(name="store_egg_prices")
async def store_egg_prices(prices: List[EggPrice]) -> None:
    """Store egg prices in the database."""
    # In a real implementation, this would store in a database
    print(f"Storing {len(prices)} egg price records")
    for price in prices:
        print(
            f"Date: {price.date}, Price: ${price.price}, Source: {price.source}, Notes: {price.notes}"
        )
