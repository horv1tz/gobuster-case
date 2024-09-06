import os
import asyncio
import subprocess
import logging
import re
import sqlite3
from urllib.parse import urlparse

# Configure logging to log both to file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gobuster_module.log', mode='a'),
        logging.StreamHandler()  # Log to console
    ]
)

def process_wordlist(file_path: str) -> list:
    """
    Process the wordlist file to find duplicates and optionally clean it.
    
    Args:
        file_path: Path to the wordlist file.
    
    Returns:
        List of unique words if cleaned, otherwise an empty list.
    """
    try:
        # Read words from the file
        with open(file_path, 'r') as f:
            words = f.readlines()

        # Count occurrences of each word
        word_count = {}
        for word in words:
            word = word.strip()
            if word:
                word_count[word] = word_count.get(word, 0) + 1

        # Identify duplicates
        duplicates = [word for word, count in word_count.items() if count > 1]

        # Log and print duplicates if found
        if duplicates:
            logging.info(f"Found the following duplicates in the wordlist: {', '.join(duplicates)}")
            print("Found the following duplicates in the wordlist:")
            for word in duplicates:
                print(word)
        else:
            logging.info("No duplicates found in the wordlist.")
            print("No duplicates found in the wordlist.")

        # Prompt user to clean the wordlist
        user_input = input("Do you want to clean the wordlist and remove duplicates? (yes/no): ").strip().lower()
        if user_input not in ['yes', 'y']:
            logging.info("User chose not to clean the wordlist.")
            print("Skipping wordlist cleaning.")
            return []

        # Remove duplicates and empty lines
        cleaned_words = list(set([word.strip() for word in words if word.strip()]))
        
        # Overwrite the file with cleaned data
        with open(file_path, 'w') as f:
            f.write('\n'.join(cleaned_words))

        logging.info("Wordlist cleaned successfully.")
        print("Wordlist cleaned successfully.")
        return cleaned_words

    except Exception as e:
        logging.error(f"Error processing wordlist: {e}")
        print(f"Error processing wordlist: {e}")
        return []

async def scan_url_by_dir(url: str) -> dict:
    """
    Perform an asynchronous directory scan using Gobuster.
    
    Args:
        url: URL to scan.
    
    Returns:
        Dictionary with logs and links extracted from the scan.
    """
    try:
        # Extract protocol and host from the URL
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        protocol = parsed_url.scheme

        # Run Gobuster command asynchronously
        process = await asyncio.create_subprocess_shell(
            f'./gobuster dir -u https://{url} -w wordlist.txt -t 50 --timeout 60s',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()

        # Save console output to log file
        with open('app.log', 'w') as output_file:
            output_file.write(stdout.decode())
            output_file.write("\n")
            output_file.write(stderr.decode())

        # Check process exit code and parse results
        if process.returncode == 0:
            logs = stdout.decode()
            links = parse_log_file('app.log')
            logging.info(f"Gobuster scan completed for URL: {url}")
        else:
            error_message = stderr.decode()
            logging.error(f"Gobuster scan failed for URL: {url} with error: {error_message}")
            logs = ""
            links = []

        # Save extracted links to database
        save_to_database(links)

        return {
            'logs': logs,
            'links': links
        }

    except Exception as e:
        logging.error(f"Error during URL scan: {e}")
        print(f"Error during URL scan: {e}")
        return {
            'logs': "",
            'links': []
        }

def parse_log_file(log_file_path: str) -> list:
    """
    Parse the log file to extract protocol, host, and path information.
    
    Args:
        log_file_path: Path to the log file.
    
    Returns:
        List of dictionaries with protocol, host, method, and path.
    """
    links = []
    protocol = ''
    host = ''
    
    try:
        # Read log file content
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()
        
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        clean_lines = [ansi_escape.sub('', line) for line in lines]
        
        # Extract URLs, protocols, and paths from log lines
        for line in clean_lines:
            if "[+] Url:" in line:
                url = line.split(":", 1)[1].strip()
                parsed_url = urlparse(url)
                protocol = parsed_url.scheme
                host = parsed_url.netloc

            if line.startswith('/'):
                parts = line.split()
                if len(parts) > 1:
                    path = parts[0].strip()
                    status = parts[2].replace('(Status:', '').replace(')', '').strip()
                    size = parts[4].replace('[Size:', '').replace(']', '').strip()
                    links.append({'protocol': protocol, 'host': host, 'path': path, 'status': status, 'size': size})

        logging.info(f"Extracted {len(links)} links from app.log.")
    except Exception as e:
        logging.error(f"Error parsing log file {log_file_path}: {e}")
        print(f"Error parsing log file {log_file_path}: {e}")

    return links

def save_to_database(data: list):
    """
    Save extracted data to the SQLite database.
    
    Args:
        data: List of dictionaries containing the data to save.
    """
    try:
        conn = sqlite3.connect('domains.db')
        cursor = conn.cursor()

        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                host TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                host_id INTEGER,
                protocol TEXT,
                path TEXT,
                size TEXT,
                status TEXT,
                FOREIGN KEY(host_id) REFERENCES hosts(id)
            )
        ''')

        # Insert or ignore host
        for entry in data:
            cursor.execute('SELECT id FROM hosts WHERE host = ?', (entry['host'],))
            host_result = cursor.fetchone()
            
            if host_result:
                host_id = host_result[0]  # Use existing host ID
            else:
                cursor.execute('INSERT INTO hosts (host) VALUES (?)', (entry['host'],))
                host_id = cursor.lastrowid

            # Insert path with protocol information
            cursor.execute('''
                INSERT INTO paths (host_id, protocol, path, size, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (host_id, entry['protocol'], entry['path'], entry['size'], entry['status']))

        conn.commit()
        conn.close()
        logging.info("Data successfully saved to SQLite database.")
    except Exception as e:
        logging.error(f"Error saving data to database: {e}")
        print(f"Error saving data to database: {e}")
