#!/usr/bin/env python3

import socket
import requests
import json
import sys
from geopy.geocoders import Nominatim

# Constants
IPINFO_URL = "https://ipinfo.io/{}/json"
HEADERS = {'User-Agent': 'IPLocatorTool/1.0'}

def get_ip_info(ip):
    """Fetch IP info from ipinfo.io"""
    try:
        response = requests.get(IPINFO_URL.format(ip), headers=HEADERS, timeout=5)
        if response.status_code != 200:
            raise ValueError("API returned non-200 status")
        return response.json()
    except requests.RequestException as e:
        raise ConnectionError(f"Request failed: {e}")

def resolve_hostname_to_ip(hostname):
    """Convert hostname to IP if needed"""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        raise ValueError("Invalid hostname or IP address")

def geolocate(coords):
    """Reverse geocode lat/lon to full address (optional)"""
    try:
        geolocator = Nominatim(user_agent="ip_locator")
        location = geolocator.reverse(coords, timeout=10)
        return location.address if location else "N/A"
    except:
        return "N/A"

def display_info(data):
    """Nicely format the output"""
    print("\n[+] IP Address Information:")
    print(f"  IP:            {data.get('ip', 'N/A')}")
    print(f"  Hostname:      {data.get('hostname', 'N/A')}")
    print(f"  City:          {data.get('city', 'N/A')}")
    print(f"  Region:        {data.get('region', 'N/A')}")
    print(f"  Country:       {data.get('country', 'N/A')}")
    print(f"  Location:      {data.get('loc', 'N/A')}")

    if 'loc' in data:
        address = geolocate(data['loc'])
        print(f"  Full Address:  {address}")

    print(f"  ISP/Org:       {data.get('org', 'N/A')}")
    print(f"  ASN:           {data.get('asn', {}).get('asn', 'N/A')}")
    print(f"  Timezone:      {data.get('timezone', 'N/A')}")
    print(f"  Postal:        {data.get('postal', 'N/A')}")
    print()

def main():
    print("\n=== IP Address Geolocation Tracker ===\n")
    ip_input = input("Enter an IP address or hostname: ").strip()
    
    try:
        ip = resolve_hostname_to_ip(ip_input)
        info = get_ip_info(ip)
        display_info(info)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
