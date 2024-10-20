import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time

def is_external_url(url, base_domain):
    parsed_url = urlparse(url)
    return parsed_url.netloc != base_domain

def is_relevant_url(url, keywords, base_domain):
    return is_external_url(url, base_domain) and any(keyword.lower() in url.lower() for keyword in keywords) and not url.endswith(".php") and not url.endswith(".pdf") and not url.endswith(".jpg")

def is_wikipedia_url(url, start_url):
    return "wikipedia.org" in urljoin(start_url, url)

def crawl_web(start_urls, max_urls, keywords, exclude_domains=[]):
    visited_urls = set()
    to_visit = start_urls.copy()

    base_domain = urlparse(start_urls[0]).netloc
    crawled_urls = []

    while to_visit and len(crawled_urls) < max_urls:
        current_url = to_visit.pop(0)

        if current_url in visited_urls or any(domain in current_url for domain in exclude_domains):
            continue

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                new_urls = [urljoin(current_url, a['href']) for a in soup.find_all('a', href=True)
                            if is_relevant_url(urljoin(current_url, a['href']), keywords, base_domain)]

                to_visit.extend(set(new_urls) - visited_urls)
                visited_urls.add(current_url)

                # Check if the current URL is a Wikipedia link and exclude it from the final list
                if is_wikipedia_url(current_url, start_urls[0]):
                    continue
                else:
                    crawled_urls.append(current_url)
                    print(f"Processing: {current_url}")

            else:
                print(f"Failed to fetch {current_url} - Status Code: {response.status_code}")

        except Exception as e:
            print(f"Error processing {current_url}: {e}")

    return crawled_urls

start_urls = ['https://en.wikipedia.org/wiki/David_Fincher','https://variety.com/t/david-fincher/']
max_urls = 24
keywords = ['Fincher']
exclude_domains = ['wikimedia.org','wikinews.org']  

result = crawl_web(start_urls, max_urls, keywords, exclude_domains)
result.append('https://en.wikipedia.org/wiki/David_Fincher')
print("\nList of crawled URLs (excluding Wikipedia links):")
for url in result:
    print(url)
print(f"\nTotal URLs crawled: {len(result)}")

def scrape_to_files(urls, output_dir):
    for i, url in enumerate(urls):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get the text content from the page
            text = soup.get_text()

            # Write text to a file
            file_name = f"page_{i + 1}.txt"
            output_path = os.path.join(output_dir, file_name)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Saved page {i + 1} to {output_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error processing {url}: {e}")

        except Exception as e:
            print(f"Unexpected error processing {url}: {e}")

        # Add a short delay to avoid overwhelming the server and respect robot.txt rules
        time.sleep(1)

output_dir = "pages"

scrape_to_files(result, output_dir)