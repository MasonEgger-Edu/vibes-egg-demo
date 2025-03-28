from temporalio.client import Client

from .workflows import EggPriceTrackingWorkflow


async def start_workflow(host: str = "localhost", port: int = 7233) -> None:
    """Start the egg price tracking workflow."""
    # Connect to Temporal server
    client = await Client.connect(f"{host}:{port}")

    # Start the workflow
    await client.start_workflow(
        EggPriceTrackingWorkflow.run,
        id="egg-price-tracking-workflow",
        task_queue="egg-price-tracking",
    )
