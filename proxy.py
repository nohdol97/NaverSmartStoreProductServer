import os
import shutil

def initialize_ip_file():
    if not os.path.exists('Ip.txt') or os.path.getsize('Ip.txt') == 0:
        if os.path.exists('proxyIp.txt'):
            shutil.copy('proxyIp.txt', 'Ip.txt')
        else:
            raise FileNotFoundError('proxyIp.txt 파일이 존재하지 않습니다.')

def get_additional_proxies(required_lines):
    with open('proxyIp.txt', 'r', encoding='utf-8') as file:
        proxy_lines = [line.strip().replace(' ', '') for line in file if line.strip()]
    return proxy_lines[:required_lines]

def get_requested_proxies():
    initialize_ip_file()

    with open('Ip.txt', 'r', encoding='utf-8') as file:
        lines = [line.strip().replace(' ', '') for line in file if line.strip()]

    requested_proxies = lines[:10]
    remaining_lines = lines[10:]

    if len(requested_proxies) < 10:
        additional_proxies_needed = 10 - len(requested_proxies)
        additional_proxies = get_additional_proxies(additional_proxies_needed)
        requested_proxies.extend(additional_proxies)

        remaining_lines = remaining_lines + additional_proxies[additional_proxies_needed:]

    with open('Ip.txt', 'w', encoding='utf-8') as file:
        file.writelines([line + '\n' for line in remaining_lines])

    extended_proxies = requested_proxies * 10
    return extended_proxies