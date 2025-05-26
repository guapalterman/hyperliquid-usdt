# Hyperliquid USDT0 Depeg Scanner

A simple monitoring tool that checks the price of USDT0 stablecoin on Hyperliquid against USDC and sends alerts to Discord when it depegs below a threshold.

## Features

- Monitors USDT0 price on Hyperliquid every minute
- Sends Discord webhook notifications when price falls below 0.998
- Includes logging to file and console
- Built-in alert cooldown to prevent spam

## Requirements

- Python 3.6+
- Required packages are listed in `requirements.txt`

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the scanner:
   ```
   python usdt0_scanner.py
   ```

## Configuration

The following parameters can be modified in the script:

- `PRICE_THRESHOLD`: The price below which alerts are triggered (default: 0.998)
- `CHECK_INTERVAL`: How often to check the price in seconds (default: 60)
- `DISCORD_WEBHOOK_URL`: Your Discord webhook URL

## Logs

Logs are written to both the console and `scanner.log` file.
