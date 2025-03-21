#!/usr/bin/env python3

import sys
import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python logger.py <logfile>")
        sys.exit(1)

    log_filename = sys.argv[1]

    with open(log_filename, "a") as log_file:
        while True:
            line = sys.stdin.readline()
            if not line:
                
                break

            line = line.strip()
            if line == "QUIT":
                
                break

            if line:
                parts = line.split(maxsplit=1)
                if len(parts) == 1:
                    action = parts[0]
                    message = ""
                else:
                    action, message = parts

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                log_file.write(f"{timestamp} [{action}] {message}\n")

if __name__ == "__main__":
    main()
