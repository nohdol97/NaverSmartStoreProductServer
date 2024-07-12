import random

multiple_count = 10

def get_shuffled_proxies():
    try:
        with open('proxyIp.txt', 'r', encoding='utf-8') as file:
            proxies = file.readlines()
        
        proxies = [proxy.strip() for proxy in proxies]
        
        # 각각 셔플한 리스트를 모아서 10배로 확장
        shuffled_proxies = []
        for _ in range(10):
            temp_proxies = proxies.copy()
            random.shuffle(temp_proxies)
            shuffled_proxies.extend(temp_proxies)
        
        return shuffled_proxies
    except Exception as e:
        raise e