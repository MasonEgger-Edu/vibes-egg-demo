# Egg Price Tracking Workflow

This project implements a Temporal workflow to track egg prices on a daily basis. The workflow runs continuously, fetching and storing egg price data every 24 hours.

## Project Structure

```
egg_price_tracker/
├── __init__.py          # Package initialization
├── __main__.py          # Main entry point
├── models.py            # Data models
├── activities.py        # Temporal activities
├── workflows.py         # Temporal workflows
├── worker.py           # Worker setup
├── client.py           # Client setup
└── scrapers.py         # Web scraping functionality
```

## Prerequisites

- Python 3.8 or higher
- Temporal server running locally (or access to a Temporal Cloud instance)
- pip (Python package manager)

## Setup

1. Create and activate a virtual environment:

   On Unix/macOS:
   ```bash
   # Create and activate virtual environment
   ./setup.sh
   
   # If you need to activate the environment later:
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   # Create and activate virtual environment
   setup.bat
   
   # If you need to activate the environment later:
   venv\Scripts\activate.bat
   ```

2. Make sure you have a Temporal server running locally. If not, you can start one using Docker:
   ```bash
   docker run --rm -p 7233:7233 -p 7234:7234 -p 7235:7235 temporalio/auto-setup:1.22.3
   ```

## Running the Workflow

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal prompt)

2. Start the workflow:
   ```bash
   python -m egg_price_tracker
   ```

The workflow will:
- Connect to the Temporal server
- Start a worker to process tasks
- Begin the egg price tracking workflow
- Run continuously, fetching and storing prices daily

## Current Implementation

The current implementation includes:
- A data model for egg prices using Pydantic
- Web scraping functionality to fetch real egg prices from Walmart
- An activity to store egg prices (currently prints to console)
- A workflow that runs daily with retry policies and error handling
- Fallback mechanism in case of scraping failures

## Data Sources

Currently, the workflow fetches egg prices from:
- Walmart.com (primary source)
  - Fetches top 5 egg products
  - Includes price and product details
  - Sorts by lowest price

## Customization

To customize this workflow for your needs:

1. Add more data sources by creating new scrapers in `scrapers.py`
2. Update the `store_egg_prices` activity to store data in your preferred database
3. Adjust the retry policy and timeouts in `workflows.py` as needed
4. Add additional activities for data processing or analysis

## Error Handling

The workflow includes robust error handling:
- Retries failed activities up to 3 times
- Logs errors to the Temporal logger
- Provides fallback prices if scraping fails
- Waits 5 minutes before retrying on errors
- Continues running indefinitely unless manually stopped

## Note on Web Scraping

This implementation uses web scraping to fetch prices. Please be aware that:
- Web scraping may be subject to rate limiting
- Website structure may change, requiring updates to the scraper
- Some websites may have terms of service that restrict scraping
- Consider using official APIs where available

## Development

When developing:
1. Always activate the virtual environment before running the application
2. The virtual environment keeps project dependencies isolated
3. To deactivate the virtual environment when you're done:
   ```bash
   deactivate
   ``` 