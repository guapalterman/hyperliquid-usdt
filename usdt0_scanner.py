#!/usr/bin/env python3
"""
USDT0 Price Scanner for Hyperliquid

This script monitors the price of USDT0 stablecoin on Hyperliquid and sends
a Discord webhook notification when the price goes below 0.998.
"""

import requests
import time
from datetime import datetime

# Configuration
HYPERLIQUID_INFO_URL = "https://api.hyperliquid.xyz/info"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1376603069088792596/75DqqA-d3V2_6tvi-GC7sdnY8bIt-zo5xIQKbeeQPdjqEPdCz0i7fB941YBOLzUXdFSB"
PRICE_THRESHOLD = 0.998
CHECK_INTERVAL = 60  # seconds

# Identified stablecoin indices from API analysis
USDTO_INDEX = "166"  # USDT0/USDC price: ~0.9992
FEUSD_INDEX = "153"  # FEUSD/USDC price: ~0.99668
USDE_INDEX = "150"   # USDE/USDC price: ~1.00065

def get_usdt0_price():
    """
    Fetch the current price of USDT0 from Hyperliquid API.
    
    Returns:
        float: Current price of USDT0 or None if an error occurs
    """
    try:
        # Get prices from allMids endpoint
        payload = {
            "type": "allMids"
        }
        response = requests.post(HYPERLIQUID_INFO_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Try to get USDT0 price using the identified index
        usdt0_key = f"@{USDTO_INDEX}"
        if usdt0_key in data:
            price = float(data[usdt0_key])
            print(f"USDT0 price: {price}")
            return price
        
        # If not found, print an error and return None
        print(f"USDT0 price not found at index {usdt0_key} or by name")
        
        # Debug: print some nearby stablecoin prices if available
        feusd_key = f"@{FEUSD_INDEX}"
        usde_key = f"@{USDE_INDEX}"
        if feusd_key in data:
            print(f"FEUSD price at {feusd_key}: {data[feusd_key]}")
        if usde_key in data:
            print(f"USDE price at {usde_key}: {data[usde_key]}")
            
        return None
    
    except Exception as e:
        print(f"Error fetching USDT0 price: {e}")
        return None

def send_discord_alert(current_price):
    """
    Send an alert to Discord webhook when USDT0 price is below threshold.
    
    Args:
        current_price (float): The current price of USDT0
    
    Returns:
        bool: True if alert was sent successfully, False otherwise
    """
    try:
        message = {
            "content": f"Price of USDT0 below {PRICE_THRESHOLD}\nCurrent price: {current_price}"
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        response.raise_for_status()
        
        print(f"Discord alert sent successfully. USDT0 price: {current_price}")
        return True
    
    except Exception as e:
        print(f"Error sending Discord alert: {e}")
        return False

def main():
    """
    Main function to periodically check USDT0 price and send alerts if needed.
    """
    print("USDT0 price scanner started")
    
    last_alert_time = 0
    alert_cooldown = 300  # 5 minutes cooldown between alerts
    
    while True:
        try:
            current_price = get_usdt0_price()
            
            if current_price is not None:
                print(f"Current USDT0 price: {current_price}")
                
                # Check if price is below threshold and cooldown period has passed
                current_time = time.time()
                if current_price < PRICE_THRESHOLD and (current_time - last_alert_time) > alert_cooldown:
                    if send_discord_alert(current_price):
                        last_alert_time = current_time
            
            # Wait for the next check interval
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"Unexpected error in main loop: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
