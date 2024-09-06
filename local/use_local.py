from modules.gobuster import process_wordlist, scan_url_by_dir
import asyncio

async def scan_hosts():
    # Process wordlist to find duplicates and optionally clean it
    # process_wordlist('wordlist.txt')

    # Open the hosts file and read each line one by one
    with open('hosts', 'r') as hosts:
        for line in hosts:
            host = line.strip()  # Удаляем пробелы и символы перевода строки
            print(f"Scanning {host}...")
            await scan_url_by_dir(host)  # Асинхронно выполняем задачу для каждого хоста

if __name__ == "__main__":
    asyncio.run(scan_hosts())
