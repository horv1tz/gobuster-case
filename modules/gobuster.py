import os
import asyncio
import subprocess
from urllib.parse import urlparse

def process_wordlist(file_path: str) -> list:
    """
    Function to find duplicates in the wordlist and optionally clean it by removing duplicates and empty lines.
    Args:
        file_path: Path to the wordlist file.
    Returns:
        cleaned_words: List of unique words if cleaned, otherwise an empty list.
    """
    with open(file_path, 'r') as f:
        words = f.readlines()

    # Count occurrences of each word
    word_count = {}
    for word in words:
        word = word.strip()
        if word:
            word_count[word] = word_count.get(word, 0) + 1

    # Find duplicates (words with more than one occurrence)
    duplicates = [word for word, count in word_count.items() if count > 1]

    # Print duplicates
    if duplicates:
        print("Found the following duplicates in the wordlist:")
        for word in duplicates:
            print(word)
    else:
        print("No duplicates found in the wordlist.")

    # Ask the user whether to perform the cleaning
    user_input = input("Do you want to clean the wordlist and remove duplicates? (yes/no): ").strip().lower()
    if user_input not in ['yes', 'y']:
        print("Skipping wordlist cleaning.")
        return []

    # Remove empty lines and duplicates
    cleaned_words = list(set([word.strip() for word in words if word.strip()]))
    
    # Overwrite the file with cleaned data
    with open(file_path, 'w') as f:
        f.write('\n'.join(cleaned_words))

    print("Wordlist cleaned successfully.")
    return cleaned_words

async def scan_url_by_dir(url: str) -> dict:
    """
    Asynchronous function to perform scanning using Gobuster.
    Args:
        url: URL to scan.
    Returns:
        return_data: Dictionary with logs and links.
    """
    # Extract protocol and host from the URL
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    protocol = parsed_url.scheme

    # Execute gobuster command
    process = await asyncio.create_subprocess_shell(
        f'gobuster dir -u {url} -w wordlist.txt -o app.log',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logs = stdout.decode()
        links = clean_logs(logs, protocol, host)
    else:
        print(f"Error: {stderr.decode()}")
        logs = ""
        links = []

    return {
        'logs': logs,
        'links': links
    }

def clean_logs(logs: str, protocol: str, host: str) -> list:
    """
    Function to parse logs and extract links.
    Args:
        logs: String with logs.
        protocol: The protocol to use (http or https).
        host: The host name.
    Returns:
        links: List of dictionaries with protocol, host, and path.
    """
    links = []
    for line in logs.splitlines():
        # Look for lines that contain paths
        if "Missed:" in line:
            parts = line.split()
            if len(parts) > 1:
                # Extract the path part
                path = parts[1].strip()
                links.append({'protocol': protocol, 'host': host, 'path': path})
    return links

def save_to_file(data: list, file_path: str):
    """
    Function to save data to a file.
    Args:
        data: Data to save.
        file_path: Path to the file.
    """
    with open(file_path, 'w') as f:
        for entry in data:
            f.write(f"{entry['protocol']}://{entry['host']}{entry['path']}\n")

if __name__ == "__main__":
    # Process wordlist to find duplicates and optionally clean it
    process_wordlist('wordlist.txt')
    
    # Start the scanning (example)
    url_to_scan = "https://dvorfs.com"
    asyncio.run(scan_url_by_dir(url_to_scan))
