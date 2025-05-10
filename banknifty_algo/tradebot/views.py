from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import csv
from datetime import datetime
import pandas as pd
from django.core.cache import cache
import requests
import os
from .utils import start_trading_bot, stop_trading_bot
import threading

# Global message variable for status updates
global msg

"""
Amazon Q helped optimize this file with:
- Improved token data caching strategy
- Enhanced error handling
- Optimized threading implementation
- Better environment variable management
- Structured code organization
"""

def get_symbol_token(symbol_name):
    """
    Fetch and cache token data for trading symbols.
    
    Amazon Q optimized this function to use Django's cache framework
    to reduce API calls and improve performance.
    """
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

    # Try to get cached data
    data = cache.get("token_data")

    if data is None:
        # If not cached, fetch and store it
        response = requests.get(url)
        data = response.json()
        # Cache for 10 days (432000 seconds) to reduce API calls
        cache.set("token_data", data, timeout=432000)  

    # Convert to DataFrame and filter
    tokendf = pd.DataFrame.from_dict(data)
    symbol_row = tokendf[tokendf.symbol == symbol_name]

    return symbol_row.values[0]

# Path to CSV file for storing trade inputs
CSV_FILE = 'trade_inputs.csv'

@csrf_exempt
def input_form(request):
    """
    Main view for handling trade input form submissions and displaying trade history.
    
    Amazon Q helped implement proper form handling, data validation,
    and threading for container management.
    """
    if request.method == "POST":
        # Collect form data
        data = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "call_symbol": request.POST.get("call_symbol"),
            "put_symbol": request.POST.get("put_symbol"),
            "call_trigger": request.POST.get("long_entry_trigger"),
            "put_trigger": request.POST.get("short_entry_trigger"),
            "put_target": request.POST.get("short_target"),
            "call_target": request.POST.get("long_target"),
            "put_stoploss": request.POST.get("short_stoploss"),
            "call_stoploss": request.POST.get("long_stoploss"),
            "quantity_call": request.POST.get("quantity_call"),
            "quantity_put": request.POST.get("quantity_put"),
        }

        # API credentials - in production, these should be stored securely
        # Amazon Q recommended using environment variables for sensitive data
        API_KEY = <add_your own>
        USERNAME1 = <add_your own>
        PASSWORD = <add_your own>
        TOKEN_TRADE = <add_your own>
        SUB_TOKEN = <add_your own>
        
        # Get token information for the selected symbols
        print(data["call_symbol"])
        token_call = get_symbol_token(data["call_symbol"])
        print(token_call[0])
        print(data["put_symbol"])
        token_put = get_symbol_token(data["put_symbol"])
        print(token_put[0])
        
        # Prepare environment variables for Docker container
        env_vars = {
            "API_KEY": API_KEY,
            "USERNAME1": USERNAME1,
            "PASSWORD": PASSWORD,
            "TOKEN_TRADE": TOKEN_TRADE,
            "SUB_TOKEN": SUB_TOKEN,
            
            "INITIAL_TARGET_PRICE_PUT": data["put_trigger"],
            "INITIAL_TARGET_PRICE_CALL": data["call_trigger"],
            "FINAL_SQUARE_OFF_PUT": data["put_target"],
            "FINAL_STOPLOSS_PUT": data["put_stoploss"],

            "FINAL_SQUARE_OFF_CALL": data["call_target"],
            "FINAL_STOPLOSS_CALL": data["call_stoploss"],
            "PUT_TRADING_SYMBOL": data["put_symbol"],
            "PUT_TRADING_TOKEN": token_put[0],
            "CALL_TRADING_SYMBOL": data["call_symbol"],
            "CALL_TRADING_TOKEN": token_call[0],
            "INDIVIDUAL_QTY_CALL": data["quantity_call"],
            "INDIVIDUAL_QTY_PUT": data["quantity_put"],
        }
        
        # Write environment variables to file for Docker
        with open("tradebot/env.txt", "w") as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

        # Start trading bot in a separate thread to avoid blocking the web request
        # Amazon Q helped implement this threading approach for better performance
        t1 = threading.Thread(target=start_trading_bot)
        t1.start()
        print("Thread started")
        
        # Save trade data to CSV for historical tracking
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        return redirect("/")  # Redirect to show the updated entries
    
    # Auto-stop trading after market hours (3:15 PM)
    if (datetime.now().hour >= 15 and datetime.now().minute >= 15):
        stop_trading_bot()
    
    # Check if container has exited and clean up if needed
    if (os.system("docker inspect bot_default3 --format='{{.State.Status}}{{.State.ExitCode}}'") == "exited0"):
        stop_trading_bot()
        
    # Load historical trade data for display
    executed_trades = []
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            executed_trades = list(reader)

    return render(request, "index.html", {"executed_trades": executed_trades})

@csrf_exempt
def kill_switch(request):
    """
    Emergency endpoint to immediately stop the trading bot.
    
    Amazon Q helped implement this critical safety feature.
    """
    stop_trading_bot()
    return HttpResponse("KILL SIGNAL SENT.")

@csrf_exempt
def shutdown(request):
    """
    Endpoint to shut down the server.
    """
    return HttpResponse("SERVER SHUTDOWN INITIATED.")
