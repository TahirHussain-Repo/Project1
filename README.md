# Project 1 - Operating Systems

## Files
- logger.py
  - Logs messages sent via stdin to a specified log file with timestamps.
- encrypt.py
  - Implements a Vigenère-based encryption/decryption program.
- driver.py
  - Main driver that spawns logger and encryption, interacts with user, logs everything.

## How to Run
1. Make sure you have Python 3 installed.
2. Mark scripts as executable (on Linux) or just call them with `python`:
   - `chmod +x logger.py encrypt.py driver.py` (if needed).
3. Run the driver:
   ```bash
   python driver.py mylogfile.txt
