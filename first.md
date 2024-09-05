Входные данные

    инструмент поиска доменов GOBUSTER: https://github.com/OJ/gobuster
    hosts - список хостов для сканирования, можно взять из репы;
    wordlist.txt - словарь для работы GOBUSTER, можно взять из репы.

Выходные данные:

    domains.txt - файл, содержаший список доменов с директориями (результат работы gobuster).
    app.log - файл с логами выполнения скрипта.

Задание:
    функция для чтения и обработки wordlist, удаление дублирующих и пустых строк;
    асинхронная функция для выполнения сканирования с использованием gobuster словарем wordlist.txt;
    парсинг результатов работы инструмента - разобрать вывод URL на протокол, хост и путь;
    запись их (протокол, хост и путь) в файл domains.txt или sqllite (что удобнее);

Gobuster Help:
Usage:
  gobuster [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  dir         Uses directory/file enumeration mode
  dns         Uses DNS subdomain enumeration mode
  fuzz        Uses fuzzing mode. Replaces the keyword FUZZ in the URL, Headers and the request body
  gcs         Uses gcs bucket enumeration mode
  help        Help about any command
  s3          Uses aws bucket enumeration mode
  tftp        Uses TFTP enumeration mode
  version     shows the current version
  vhost       Uses VHOST enumeration mode (you most probably want to use the IP address as the URL parameter)

Flags:
      --debug                 Enable debug output
      --delay duration        Time each thread waits between requests (e.g. 1500ms)
  -h, --help                  help for gobuster
      --no-color              Disable color output
      --no-error              Don't display errors
  -z, --no-progress           Don't display progress
  -o, --output string         Output file to write results to (defaults to stdout)
  -p, --pattern string        File containing replacement patterns
  -q, --quiet                 Don't print the banner and other noise
  -t, --threads int           Number of concurrent threads (default 10)
  -v, --verbose               Verbose output (errors)
  -w, --wordlist string       Path to the wordlist. Set to - to use STDIN.
      --wordlist-offset int   Resume from a given position in the wordlist (defaults to 0)

Use "gobuster [command] --help" for more information about a command.

В папке:
gobuster - бинарник для linux
hosts - список хостов (доменов в виде 1 строка - 1 домен)
wordlist.txt - список возможных роутов (например: ya.ru/.github/workflows/publish.yml и т.п .github/workflows/publish.yml - роут)

пример использования ./gobuster dir -w wordlist.txt -u https://dvorfs.com -v
пример логов:
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://dvorfs.com
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                wordlist.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Verbose:                 true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
Missed: /+CSCOT+/oem-customization?app=AnyConnect&type=oem&platform=..&resource-type=..&name=%2bCSCOE%2b/portal_inc.lua (Status: 404) [Size: 162]
Missed: /%3f                  (Status: 404) [Size: 162]
Missed: /!.htpasswd           (Status: 404) [Size: 162]
Missed: /!.gitignore          (Status: 404) [Size: 162]
Missed: /+CSCOE+/session_password.html (Status: 404) [Size: 162]
Missed: /%ff                  (Status: 404) [Size: 162]
Missed: /%2e%2e;/test         (Status: 404) [Size: 162]
Missed: /!.htaccess           (Status: 404) [Size: 162]
Missed: /+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=.. (Status: 404) [Size: 162]
Missed: /.0                   (Status: 404) [Size: 162]
Missed: /%C0%AE%C0%AE%C0%AF   (Status: 404) [Size: 162]
Missed: /+CSCOE+/logon.html#form_title_text (Status: 404) [Size: 162]
Missed: /.AppleDouble         (Status: 404) [Size: 162]
Missed: /.CVS                 (Status: 404) [Size: 162]
Missed: /.AppleDesktop        (Status: 404) [Size: 162]
Missed: /.AppleDB             (Status: 404) [Size: 162]
Missed: /.7z                  (Status: 404) [Size: 162]
Missed: /.CSV                 (Status: 404) [Size: 162]
Missed: /.DS_Store            (Status: 404) [Size: 162]
Missed: /..;                  (Status: 404) [Size: 162]
Missed: /.JustCode            (Status: 404) [Size: 162]
===============================================================
Finished
===============================================================

код который надо дописать: 
import os
import sys

def clean_links(logs: str) -> list:
    """
    Description:
    Args:
    logs: string
    Returns:
    links: list
    """
    links = []
    return links


def scan_url_by_dir(url: str) -> dict:
    """
    Description:
    Args:
    url: string
    Returns:

    """
    data = os.system(f'gobuster dir -u {url} -w wordlist.txt')
    print(data)
    
    logs = ""
    links = []

    return_data = {
        logs: logs,
        links: links
    }