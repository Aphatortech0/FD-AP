import requests
from urllib.parse import urlparse, parse_qs
import hashlib
import time
import threading

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': '',
    'x-requested-with': 'org.telegram.messenger',
}

def key_bot():
    try:
        print("\033[96m")
        print("╔════════════════════════════════════════════╗")
        print("║          FreeDogs by Codex Vault           ║")
        print("║                                            ║")
        print("║                  Aphator                   ║")
        print("╚════════════════════════════════════════════╝")
        print("\033[0m")
    except Exception as e:
        print(f"An error occurred: {e}") 

def compute_md5(amount, seq):
    prefix = str(amount) + str(seq) + "7be2a16a82054ee58398c5edb7ac4a5a"
    return hashlib.md5(prefix.encode()).hexdigest()

def auth(url: str) -> dict:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.fragment)
    init = query_params.get('tgWebAppData', [None])[0]
    params = {'invitationCode': '', 'initData': init}
    data = {'invitationCode': '', 'initData': init}
    response = requests.post('https://api.freedogs.bot/miniapps/api/user/telegram_auth', params=params, headers=headers, data=data)
    return response.json()

def do_click(init):
    headers['authorization'] = 'Bearer ' + auth(init)['data']['token']
    response = requests.get('https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo', headers=headers)
    Seq = response.json()['data']['collectSeqNo']
    hsh = compute_md5('100000', Seq)
    params = {
        'collectAmount': '100000',
        'hashCode': hsh,
        'collectSeqNo': str(Seq),
    }
    response = requests.post('https://api.freedogs.bot/miniapps/api/user_game/collectCoin', params=params, headers=headers, data=params)
    return response.json()

def get_init_urls():
    with open('session.txt', 'r') as file:
        urls = file.read().strip().splitlines()
    return urls

def start_clicking(init_url, url_num, attempt_start=1):
    attempt = attempt_start
    while True:
        for i in range(500):
            result = do_click(init_url)
            print(f"URL #{url_num} - Attempt {attempt}, Tap {i+1}: {result}")
            time.sleep(0.1)  # Adjust delay as needed
        attempt += 1
        time.sleep(1)  # Wait 1 second before the next set of 500 taps

if __name__ == '__main__':
    # Display the banner
    key_bot()

    # Get all init URLs from the session file
    init_urls = get_init_urls()

    # Start a separate thread for each URL with its corresponding number
    threads = []
    for url_num, init_url in enumerate(init_urls, start=1):
        thread = threading.Thread(target=start_clicking, args=(init_url, url_num))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
