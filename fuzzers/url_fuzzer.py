import urllib3
import argparse

parser = argparse.ArgumentParser(description="Simple URL fuzzer")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager(
    cert_reqs='CERT_NONE' # Disable certificate verification
)

parser.add_argument("-u", type=str, help="URL")
args = parser.parse_args()
site = args.u

word_list = open("words.txt", "r")
with word_list as word_list:
    lines = word_list.readlines()
    for line in lines:
        word = line.strip()
        saved_site = f"{site}{word}"
        print(saved_site)
        max_retries = 3
        for attempt in range(max_retries + 1):
            try:
                response = http.request("GET", saved_site, timeout=5)
                print(f"Success: {response.status}")
                break
            except urllib3.exceptions.MaxRetryError as e:
                # fixed 1: certain web redirections problems
                if attempt < max_retries:
                    print("Too many retries: Adding a slash and retrying...")
                    saved_site += "/"
                else:
                    print(f"Error: Maximum retries exceeded. {e}")
                    break 
            except urllib3.exceptions.DecodeError as e:
                print(f"Decode Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
