# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "httpx",
#     "pydantic",
#     "strenum",
# ]
# ///

import sys
import os
import time
from pathlib import Path

# Add the current directory to sys.path so we can import the local listmonk package
# This assumes the script is run from the project root or the package is installed
sys.path.append(os.getcwd())

try:
    import listmonk
except ImportError:
    print("Error: Could not import 'listmonk'. Make sure you are running from the project root.")
    sys.exit(1)

def main():
    # Configuration
    # Ideally these would come from env vars, but for a demo we'll hardcode or use defaults
    url = os.getenv("LISTMONK_URL", "http://localhost:9003")
    user = os.getenv("LISTMONK_USER", "sdf")
    password = os.getenv("LISTMONK_PASSWORD", "UW6xYMkYan6s5lGaHC4AIX3yLUziYjL3")
    csv_filename = "data.csv"
    
    print(f"--- Listmonk Import API Demo ---")
    print(f"Target URL: {url}")
    
    # 1. Setup
    listmonk.set_url_base(url)
    
    # 2. Login
    print("\n1. Logging in...")
    try:
        if listmonk.login(user, password):
            print("âœ… Login successful")
        else:
            print("âŒ Login failed")
            return
    except Exception as e:
        print(f"âŒ Login error: {e}")
        return

    # 3. Check for Data File
    csv_path = Path(csv_filename).resolve()
    if not csv_path.exists():
        print(f"\nâŒ Error: Data file '{csv_filename}' not found at {csv_path}")
        print("Please create a dummy CSV file to test with.")
        return
    
    print(f"\n2. Found data file: {csv_path.name}")

    # 4. Start Import
    print("\n3. Starting Import...")
    try:
        # Import to list ID 1 (Default list usually)
        result = listmonk.import_subscribers(
            file_path=csv_path,
            lists=[1],
            overwrite=True
        )
        if result:
            print("âœ… Import started successfully")
        else:
            print("âŒ Failed to start import")
            return
            
    except Exception as e:
        print(f"âŒ Import error: {e}")
        return

    # 5. Monitor Status
    print("\n4. Monitoring Status...")
    while True:
        status = listmonk.get_import_status()
        if not status:
            print("No active import status.")
            break
            
        print(f"   Status: {status.status.upper()} | Processed: {status.imported} / {status.total}")
        
        if status.status in ('finished', 'failed', 'none'):
            break
            
        time.sleep(0.5)

    # 6. Fetch Logs
    print("\n5. Fetching Import Logs...")
    logs = listmonk.get_import_logs()
    if logs:
        print("\n--- Start Logs ---")
        print(logs.strip())
        print("--- End Logs ---")
    else:
        print("No logs available.")

    print("\nâœ¨ Demo Completed")

if __name__ == "__main__":
    main()
