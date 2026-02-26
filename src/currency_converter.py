import requests
from cachetools import cached, TTLCache

ttl_cache = TTLCache(maxsize=100, ttl=3*60*60 )

@cached(cache=ttl_cache)
def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching exchange rate: {response.status_code}")
    return response.json().get('rates').get(target_currency), response.json().get('time_last_updated')

def convert_currency(amount, exchange_rate):
    return amount * exchange_rate

if __name__ == "__main__":
    base_currency = input("Enter base currency (e.g., USD): ")
    target_currency = input("Enter target currency (e.g., CAD): ")
    base_amount = float(input(f"Enter amount in {base_currency}: "))
    
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    targetted_amount = convert_currency(base_amount, exchange_rate)
    
    print(f"{base_amount} {base_currency} is : {targetted_amount} {target_currency}") 