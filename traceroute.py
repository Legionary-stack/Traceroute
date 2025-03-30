import subprocess
import re
import socket
import sys
import ipaddress
import requests


def get_geo(ip):
    """Получает информацию об IP через ip-api.com"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode,as,isp,org", timeout=3)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


def perform_traceroute(target):
    """Выполняет трассировку и возвращает список IP с временем отклика"""
    try:
        if sys.platform.startswith('win'):
            command = ['tracert', '-d', '-h', '30', '-w', '1000', target]
        else:
            command = ['traceroute', '-m', '30', '-w', '3', '-q', '1', '-n', target]

        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout

        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            target_ip = target

        hops = []
        for line in output.splitlines():
            match = re.search(
                r'^\s*(\d+)\s+(?:[<.\d]+\s+ms\s+)*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
                line
            )
            if match:
                hop_num, ip = match.groups()
                if ip != target_ip and (not hops or ip != hops[-1]['ip']):
                    hops.append({'hop': int(hop_num), 'ip': ip})

        return hops
    except Exception as e:
        print(f"Ошибка при выполнении трассировки: {e}")
        return []


def get_ip_info(ip):
    """Получает полную информацию об IP"""
    if ipaddress.ip_address(ip).is_private:
        return {
            'as': 'Локальная',
            'country': 'N/A',
            'provider': 'Маршрутизатор',
            'org': 'Локальная сеть'
        }

    geo = get_geo(ip)
    if geo:
        as_info = geo.get('as', 'N/A')
        if as_info != 'N/A':
            as_info = as_info.split()[0]

        org = geo.get('org', geo.get('isp', 'N/A'))
        provider = geo.get('isp', org)

        return {
            'as': f"{as_info}" if as_info != 'N/A' else 'N/A',
            'country': geo.get('countryCode', 'N/A'),
            'provider': provider,
            'org': org
        }


def format_output(value, max_length=30):
    """Форматирует вывод для фиксированной ширины колонки"""
    if len(value) > max_length:
        return value[:max_length - 3] + "..."
    return value.ljust(max_length)


def main():
    print("Трассировка маршрута")
    target = input("Введите доменное имя или IP-адрес: ").strip()

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except:
        print("Ошибка: нет подключения к интернету!")
        return

    try:
        ipaddress.ip_address(target)
    except ValueError:
        try:
            target = socket.gethostbyname(target)
        except:
            print("Ошибка: неверный домен или IP!")
            return

    print("\nВыполняем трассировку...")
    hops = perform_traceroute(target)
    if not hops:
        print("Не удалось выполнить трассировку")
        return

    print("\nРезультаты трассировки:")
    print("№  | IP-адрес      | AS       | Страна | Провайдер")
    print("---|---------------|----------|--------|-----------")

    for hop in hops:
        info = get_ip_info(hop['ip'])

        hop_num = str(hop['hop']).ljust(2)
        ip = hop['ip'].ljust(13)
        as_info = info['as'].ljust(8)
        country = info['country'].ljust(6)
        provider = format_output(info['provider'])

        print(f"{hop_num} | {ip} | {as_info} | {country} | {provider}")


if __name__ == "__main__":
    main()
