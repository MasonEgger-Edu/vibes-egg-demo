import asyncio

from .client import start_workflow
from .worker import run_worker


async def main():
    """Main entry point for the application."""
    # Start the worker in the background
    worker_task = asyncio.create_task(run_worker())

    # Start the workflow
    await start_workflow()

    # Keep the worker running
    await worker_task


if __name__ == "__main__":
    asyncio.run(main())
