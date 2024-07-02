import requests
import json
import time
from datetime import datetime
from requests.exceptions import RequestException

def get_transaction_history(account_id, last_timestamp=None, max_retries=5, retry_delay=5):
    base_url = "https://mainnet-public.mirrornode.hedera.com"
    endpoint = f"/api/v1/transactions"
    
    params = {
        "account.id": account_id,
        "limit": 100,
        "order": "asc"
    }
    
    if last_timestamp:
        params['timestamp'] = f"gt:{last_timestamp}"
    
    all_transactions = []
    
    while True:
        for attempt in range(max_retries):
            try:
                response = requests.get(base_url + endpoint, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                transactions = data.get('transactions', [])
                all_transactions.extend(transactions)
                
                next_link = data.get('links', {}).get('next')
                if next_link:
                    params['timestamp'] = next_link.split('timestamp=')[1].split('&')[0]
                else:
                    return all_transactions
                
                time.sleep(1)  # Respect rate limits
                break  # Successful request, break the retry loop
            
            except RequestException as e:
                if attempt < max_retries - 1:
                    print(f"Request failed: {e}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Max retries reached. Last error: {e}")
                    return all_transactions

def save_transactions(transactions, filename):
    with open(filename, 'w') as f:
        json.dump(transactions, f, indent=2)

def load_transactions(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def sync_transactions(account_id, filename):
    transactions = load_transactions(filename)
    
    if transactions:
        last_timestamp = transactions[-1]['consensus_timestamp']
    else:
        last_timestamp = None
    
    new_transactions = get_transaction_history(account_id, last_timestamp)
    
    if new_transactions:
        transactions.extend(new_transactions)
        save_transactions(transactions, filename)
    
    return len(new_transactions)

def main():
    account_id = "0.0.626047"
    filename = f"transactions_{account_id}.json"
    
    while True:
        try:
            new_count = sync_transactions(account_id, filename)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if new_count > 0:
                print(f"[{current_time}] Synced {new_count} new transactions")
            else:
                print(f"[{current_time}] No new transactions")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(10)  # Wait for 10 seconds before next sync

if __name__ == "__main__":
    main()