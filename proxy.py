import random

def get_shuffled_proxies():
    try:
        with open('proxyIp.txt', 'r', encoding='utf-8') as file:
            proxies = file.readlines()
        
        proxies = [proxy.strip() for proxy in proxies]
        random.shuffle(proxies)
        return proxies
    except Exception as e:
        raise e