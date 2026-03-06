import requests
import whois
import socket
import re
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# Initialize colorama (makes colors work on Windows)
init(autoreset=True)

#  BANNER
def banner():
    print(Fore.CYAN + r"""
  ___  ____  ___ _   _ _____    ____  _____ ____ ___  _   _ 
 / _ \/ ___|_ _| \ | |_   _|  |  _ \| ____/ ___/ _ \| \ | |
| | | \___ \| ||  \| | | |    | |_) |  _|| |  | | | |  \| |
| |_| |___) | || |\  | | |    |  _ <| |__| |__| |_| | |\  |
 \___/|____/___|_| \_| |_|    |_| \_\_____\____\___/|_| \_|
    """)
    print(Fore.YELLOW + "        OSINT Reconnaissance Tool — by Amar")
    print(Fore.WHITE + "        For educational and ethical use only.\n")

# ─────────────────────────────────────────────
#  1. WHOIS LOOKUP — who owns a domain?
# ─────────────────────────────────────────────
def whois_lookup(domain):
    print(Fore.CYAN + f"\n[+] Running WHOIS lookup on: {domain}")
    try:
        w = whois.whois(domain)
        print(Fore.GREEN + f"  Domain Name   : {w.domain_name}")
        print(Fore.GREEN + f"  Registrar     : {w.registrar}")
        print(Fore.GREEN + f"  Creation Date : {w.creation_date}")
        print(Fore.GREEN + f"  Expiry Date   : {w.expiration_date}")
        print(Fore.GREEN + f"  Name Servers  : {w.name_servers}")
        print(Fore.GREEN + f"  Org / Owner   : {w.org}")
    except Exception as e:
        print(Fore.RED + f"  [!] WHOIS failed: {e}")

# ───────────────────────────────────────────
#  2. IP LOOKUP — get IP + location info
# ───────────────────────────────────────────
def ip_lookup(domain):
    print(Fore.CYAN + f"\n[+] Resolving IP address for: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(Fore.GREEN + f"  IP Address : {ip}")

        # Use free API to get location info
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        print(Fore.GREEN + f"  City       : {data.get('city', 'N/A')}")
        print(Fore.GREEN + f"  Region     : {data.get('region', 'N/A')}")
        print(Fore.GREEN + f"  Country    : {data.get('country', 'N/A')}")
        print(Fore.GREEN + f"  ISP / Org  : {data.get('org', 'N/A')}")
        print(Fore.GREEN + f"  Timezone   : {data.get('timezone', 'N/A')}")
    except Exception as e:
        print(Fore.RED + f"  [!] IP lookup failed: {e}")

# ────────────────────────────────────────────────
#  3. EMAIL SCRAPER — finds emails on a webpage
# ────────────────────────────────────────────────
def scrape_emails(url):
    print(Fore.CYAN + f"\n[+] Scraping emails from: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Regex pattern to find email addresses
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))

        if emails:
            print(Fore.GREEN + f"  Found {len(emails)} email(s):")
            for email in emails:
                print(Fore.GREEN + f"    → {email}")
        else:
            print(Fore.YELLOW + "  No emails found on this page.")
    except Exception as e:
        print(Fore.RED + f"  [!] Email scraping failed: {e}")

# ────────────────────────────────────────────────
#  4. METADATA SCRAPER — page title, links, tech
# ────────────────────────────────────────────────
def scrape_metadata(url):
    print(Fore.CYAN + f"\n[+] Extracting metadata from: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "N/A"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else "N/A"

        print(Fore.GREEN + f"  Page Title   : {title}")
        print(Fore.GREEN + f"  Description  : {description}")
        print(Fore.GREEN + f"  Status Code  : {response.status_code}")

        # Count links
        links = soup.find_all("a", href=True)
        external = [l["href"] for l in links if l["href"].startswith("http")]
        print(Fore.GREEN + f"  Total Links  : {len(links)}")
        print(Fore.GREEN + f"  External Links: {len(external)}")

        # Show first 5 external links
        if external:
            print(Fore.YELLOW + "  Sample External Links:")
            for link in external[:5]:
                print(Fore.YELLOW + f"    → {link}")

    except Exception as e:
        print(Fore.RED + f"  [!] Metadata scraping failed: {e}")

# ──────────────────────────────────────
#  MAIN MENU
# ──────────────────────────────────────
def main():
    banner()

    print(Fore.WHITE + "Enter the target domain (e.g. example.com): ", end="")
    domain = input().strip()

    # Clean up input — remove https:// if user typed it
    domain = domain.replace("https://", "").replace("http://", "").rstrip("/")
    url = "https://" + domain

    print(Fore.MAGENTA + "\nWhat do you want to do?")
    print("  [1] WHOIS Lookup")
    print("  [2] IP & Location Lookup")
    print("  [3] Scrape Emails from Homepage")
    print("  [4] Extract Page Metadata")
    print("  [5] Run ALL")

    print(Fore.WHITE + "\nEnter choice (1-5): ", end="")
    choice = input().strip()

    if choice == "1":
        whois_lookup(domain)
    elif choice == "2":
        ip_lookup(domain)
    elif choice == "3":
        scrape_emails(url)
    elif choice == "4":
        scrape_metadata(url)
    elif choice == "5":
        whois_lookup(domain)
        ip_lookup(domain)
        scrape_emails(url)
        scrape_metadata(url)
    else:
        print(Fore.RED + "[!] Invalid choice.")

    print(Fore.CYAN + "\n[✓] Scan complete.\n")

if __name__ == "__main__":
    main()
