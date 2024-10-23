#!/usr/bin/env python


import argparse
from bs4 import BeautifulSoup
import requests
import sys
from tabulate import tabulate


def genParser() -> argparse.ArgumentParser:
    """Generates a CLI argument parser"""
    parser = argparse.ArgumentParser(description="SpeedGuide.net port lookup " +
                                     "utility")
    parser.add_argument("port", type=int, action="store",
                        help="port number to look up (0-65535)")
    parser.add_argument("protocol", type=str, choices=["tcp", "udp", ""],
                        nargs="?", action="store", default = "",
                        metavar="protocol", help="port protocol (tcp/udp)")
    return parser

def getPortInfo(port: int) -> dict:
    """Gets port information from SpeedGuide.net"""
    if not 0 <= port <= 65535:
        sys.exit(f"{port} is not a valid port number")
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; " +
                      "x64) AppleWebKit/537.36 (KHTML, like Gecko) " + 
                      "Chrome/130.0.0.0 Safari/537.36"})
    try:
        html = s.get(f"https://www.speedguide.net/port.php?port={port}").content
    except:
        sys.exit("Could not connect to www.speedguide.net")
    try:
        table = BeautifulSoup(html, features="lxml").find(
                              "table", attrs={"class":"port"})
        head = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        portInfo = [head]
        for row in table.find_all("tr")[1:]:
            portInfo.append([td.get_text() for td in row.find_all("td")])
        return portInfo
    except:
        raise
        sys.exit(f"No data found for port {port}")

def printPortInfo(portInfo: list[list], protocol: str = "") -> None:
    """Prints port information optionally filtered by protocol"""
    if protocol:
        filteredData = [portInfo[0]]
        for row in portInfo[1:]:
            if protocol in row[1].strip().split(","):
                filteredData.append(row)
        portInfo = filteredData
    print(tabulate(portInfo, headers="firstrow", tablefmt="grid",
                   numalign="left", stralign="left", maxcolwidths=80))


def main() -> None:
    """Main method"""
    try:
        if len(sys.argv) <= 1:
            genParser().print_help()
            sys.exit()
        else:
            args = genParser().parse_args()
            portInfo = getPortInfo(args.port)
            printPortInfo(portInfo, args.protocol)
    except KeyboardInterrupt:
        sys.exit("Terminated by user")


if __name__ == "__main__":
    main()
