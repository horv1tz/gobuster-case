from modules.gobuster import process_wordlist, scan_url_by_dir
import asyncio

if __name__ == "__main__":
    # Process wordlist to find duplicates and optionally clean it
    # process_wordlist('wordlist.txt')
    
    # Start the scanning (example)
    url_to_scan = "https://dvorfs.com"
    asyncio.run(scan_url_by_dir(url_to_scan))
