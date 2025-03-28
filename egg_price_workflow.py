from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.common import RetryPolicy
from temporalio.worker import Worker


# Data model for egg prices
class EggPrice(BaseModel):
    date: datetime
    price: float
    source: str
    notes: Optional[str] = None


# Activity to fetch egg prices (simulated for now)
@activity.defn
async def fetch_egg_prices() -> List[EggPrice]:
    # In a real implementation, this would fetch from actual data sources
    # For now, we'll simulate with some sample data
    return [
        EggPrice(
            date=datetime.now(),
            price=3.99,
            source="Local Market",
            notes="Large Grade A eggs",
        )
    ]


# Activity to store egg prices
@activity.defn
async def store_egg_prices(prices: List[EggPrice]) -> None:
    # In a real implementation, this would store in a database
    print(f"Storing {len(prices)} egg price records")
    for price in prices:
        print(f"Date: {price.date}, Price: ${price.price}, Source: {price.source}")


# Main workflow definition
@workflow.defn
class EggPriceTrackingWorkflow:
    @workflow.run
    async def run(self) -> None:
        # Set up retry policy for activities
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(minutes=1),
            maximum_attempts=3,
        )

        while True:
            try:
                # Fetch current egg prices
                prices = await workflow.execute_activity(
                    fetch_egg_prices,
                    start_to_close_timeout=timedelta(minutes=5),
                    retry_policy=retry_policy,
                )

                # Store the prices
                await workflow.execute_activity(
                    store_egg_prices,
                    prices,
                    start_to_close_timeout=timedelta(minutes=5),
                    retry_policy=retry_policy,
                )

                # Wait until next day
                await workflow.sleep(timedelta(days=1))

            except Exception as e:
                workflow.logger.error(f"Error in workflow: {str(e)}")
                # Wait a bit before retrying on error
                await workflow.sleep(timedelta(minutes=5))


async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Run a worker
    worker = Worker(
        client,
        task_queue="egg-price-tracking",
        workflows=[EggPriceTrackingWorkflow],
        activities=[fetch_egg_prices, store_egg_prices],
    )

    # Start the workflow
    await client.start_workflow(
        EggPriceTrackingWorkflow.run,
        id="egg-price-tracking-workflow",
        task_queue="egg-price-tracking",
    )

    # Run the worker
    await worker.run()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
