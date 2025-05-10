from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import csv
from datetime import datetime
import pandas as pd
from django.core.cache import cache
import requests
def get_symbol_token(symbol_name):
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

    # Try to get cached data
    data = cache.get("token_data")

    if data is None:
        # If not cached, fetch and store it
        response = requests.get(url)
        data = response.json()
        cache.set("token_data", data, timeout=432000)  # Cache for 10 days

    # Convert to DataFrame and filter
    tokendf = pd.DataFrame.from_dict(data)
    symbol_row = tokendf[tokendf.symbol == symbol_name]

    return symbol_row.values[0]

@csrf_exempt
def input_form(request):
    if request.method == "POST":
        data = {
            "long_entry_trigger": request.POST.get("long_entry_trigger"),
            "long_script": request.POST.get("long_script"),
            "long_target": request.POST.get("long_target"),
            "long_stoploss": request.POST.get("long_stoploss"),
            "short_entry_trigger": request.POST.get("short_entry_trigger"),
            "short_script": request.POST.get("short_script"),
            "short_target": request.POST.get("short_target"),
            "short_stoploss": request.POST.get("short_stoploss"),
            "quantity": request.POST.get("quantity"),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
       
        
        """  url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

        d = requests.get(url).json()
        tokendf = pd.DataFrame.from_dict(d)
        banknifty = tokendf[tokendf.symbol==data["long_script"]] """
        
        print(data)
        
        
        print(data["long_script"])
        banknifty = get_symbol_token(data["long_script"])
        print(banknifty[0])
        
        # Save to CSV
        with open('trade_inputs.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        return HttpResponse(f"Trade setup saved.{banknifty[0]}")

    return render(request, "index.html")

@csrf_exempt
def kill_switch(request):
    # You'd implement kill logic here
    return HttpResponse("KILL SIGNAL SENT.")

@csrf_exempt
def shutdown(request):
    # You'd implement shutdown logic here
    return HttpResponse("SERVER SHUTDOWN INITIATED.")
