from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

from .activities import fetch_egg_prices, store_egg_prices


@workflow.defn(name="EggPriceTrackingWorkflow")
class EggPriceTrackingWorkflow:
    """Workflow for tracking egg prices on a daily basis."""

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
