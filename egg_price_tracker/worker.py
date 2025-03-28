from temporalio.client import Client
from temporalio.worker import Worker

from .activities import fetch_egg_prices, store_egg_prices
from .workflows import EggPriceTrackingWorkflow


async def run_worker(host: str = "localhost", port: int = 7233) -> None:
    """Run the Temporal worker."""
    # Connect to Temporal server
    client = await Client.connect(f"{host}:{port}")

    # Run a worker
    worker = Worker(
        client,
        task_queue="egg-price-tracking",
        workflows=[EggPriceTrackingWorkflow],
        activities=[fetch_egg_prices, store_egg_prices],
    )

    # Run the worker
    await worker.run()
