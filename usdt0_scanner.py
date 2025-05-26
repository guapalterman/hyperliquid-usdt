#!/usr/bin/env python3
"""
Stablecoin Price Scanner for Hyperliquid

This script monitors the prices of multiple stablecoins on Hyperliquid (USDT0, FEUSD, USDE)
and sends Discord webhook notifications when their prices fall below specific thresholds.
"""

import requests
import time
from datetime import datetime

# Configuration
HYPERLIQUID_INFO_URL = "https://api.hyperliquid.xyz/info"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1376603069088792596/75DqqA-d3V2_6tvi-GC7sdnY8bIt-zo5xIQKbeeQPdjqEPdCz0i7fB941YBOLzUXdFSB"
CHECK_INTERVAL = 60  # seconds
ALERT_COOLDOWN = 900  # 15 minutes in seconds

# Stablecoin configuration
STABLECOINS = {
    "USDT0": {
        "index": "166",    # USDT0/USDC price: ~0.9992
        "threshold": 0.998,
        "last_alert": 0     # Timestamp of the last alert
    },
    "FEUSD": {
        "index": "153",    # FEUSD/USDC price: ~0.99668
        "threshold": 0.985,
        "last_alert": 0
    },
    "USDE": {
        "index": "150",    # USDE/USDC price: ~1.00065
        "threshold": 0.99,
        "last_alert": 0
    }
}

def get_stablecoin_prices():
    """
    Fetch the current prices of all monitored stablecoins from Hyperliquid API.
    
    Returns:
        dict: Dictionary of stablecoin names and their current prices
    """
    try:
        # Get prices from allMids endpoint
        payload = {
            "type": "allMids"
        }
        response = requests.post(HYPERLIQUID_INFO_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Get prices for all configured stablecoins
        prices = {}
        for coin_name, coin_data in STABLECOINS.items():
            coin_key = f"@{coin_data['index']}"
            if coin_key in data:
                price = float(data[coin_key])
                prices[coin_name] = price
                print(f"{coin_name} price: {price}")
            else:
                print(f"{coin_name} price not found at index {coin_key}")
        
        return prices
    
    except Exception as e:
        print(f"Error fetching stablecoin prices: {e}")
        return {}

def send_discord_alert(coin_name, current_price, threshold):
    """
    Send an alert to Discord webhook when a stablecoin's price is below threshold.
    
    Args:
        coin_name (str): The name of the stablecoin
        current_price (float): The current price of the stablecoin
        threshold (float): The threshold that was crossed
    
    Returns:
        bool: True if alert was sent successfully, False otherwise
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        role_tag = "<@&1333036584760774666>"  # Role ID format to tag in Discord
        message = {
            "content": f"{role_tag} ⚠️ ALERT: {coin_name} Depeg Detected ⚠️\n" +
                      f"Price of {coin_name} below {threshold}\n" +
                      f"Current price: {current_price}\n" +
                      f"Time: {timestamp}"
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        response.raise_for_status()
        
        print(f"Discord alert sent successfully. {coin_name} price: {current_price}")
        return True
    
    except Exception as e:
        print(f"Error sending Discord alert: {e}")
        return False

def check_for_depegs(prices):
    """
    Check if any stablecoin prices are below their thresholds and send alerts if needed.
    
    Args:
        prices (dict): Dictionary of stablecoin names and their current prices
    """
    current_time = time.time()
    
    for coin_name, price in prices.items():
        coin_data = STABLECOINS[coin_name]
        threshold = coin_data["threshold"]
        last_alert = coin_data["last_alert"]
        
        # Check if price is below threshold and cooldown period has passed
        if price < threshold and (current_time - last_alert) > ALERT_COOLDOWN:
            print(f"{coin_name} price {price} is below threshold {threshold}. Sending alert...")
            if send_discord_alert(coin_name, price, threshold):
                # Update the last alert timestamp
                STABLECOINS[coin_name]["last_alert"] = current_time

def main():
    """
    Main function to periodically check stablecoin prices and send alerts if needed.
    """
    print("Stablecoin price scanner started")
    print(f"Monitoring: {', '.join(STABLECOINS.keys())}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print(f"Alert cooldown: {ALERT_COOLDOWN} seconds (15 minutes)")
    
    while True:
        try:
            # Get current prices for all stablecoins
            prices = get_stablecoin_prices()
            
            if prices:
                # Check for depegs and send alerts if needed
                check_for_depegs(prices)
            
            # Wait for the next check interval
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"Unexpected error in main loop: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
