import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Function to get all links from the HTML page
def get_links(url):
    try:
        # Make a request to the site
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the response is not successful (e.g. 404)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links within the page
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error connecting to the domain: {e}")
        return []

# Function to display a progress bar during the process of fetching files
def display_progress_bar(files):
    with tqdm(total=len(files), desc="Scanning files", ncols=100, colour="cyan") as pbar:
        for file in files:
            pbar.set_postfix(file=file)
            pbar.update(1)

# Main function to collect and display files
def main():
    # Ask the user to enter the domain
    global domain
    user_input = input(f"{Fore.YELLOW}Enter the domain (e.g. www.example.com): ")

    # Automatically add the https:// prefix if missing
    if not user_input.startswith(('http://', 'https://')):
        domain = 'https://' + user_input
    else:
        domain = user_input

    # File extensions to search for
    extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.gif', '.bmp', '.svg']

    print(f"\n{Fore.GREEN}Starting scan of domain: {domain}")

    # Get all links from the page
    links = get_links(domain)

    if not links:  # If no links are found (connection error), exit the program
        print(f"{Fore.RED}\nUnable to retrieve links from the domain. Please check the domain or your connection.")
        return

    # Display the progress bar while fetching files
    print(f"{Fore.CYAN}\nStarting file search...\n")
    display_progress_bar(links)

    # Display all files found (not just those with specific extensions)
    print(f"\n{Fore.MAGENTA}Files found on domain {domain}:")

    for file in links:
        # Print each file with a different color for a more visually appealing display
        if file.endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg')):
            print(f"{Fore.GREEN}{file}")
        elif file.endswith(('pdf')):
            print(f"{Fore.BLUE}{file}")
        else:
            print(f"{Fore.YELLOW}{file}")

# Run the script
if __name__ == "__main__":
    main()
