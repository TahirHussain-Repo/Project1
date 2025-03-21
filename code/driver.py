#!/usr/bin/env python3

import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python driver.py <logfile>")
        sys.exit(1)

    log_filename = sys.argv[1]

    logger_proc = subprocess.Popen(
        ["python", "logger.py", log_filename],
        stdin=subprocess.PIPE,
        text=True
    )

    encrypt_proc = subprocess.Popen(
        ["python", "encrypt.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    def log_line(line):
        logger_proc.stdin.write(line + "\n")
        logger_proc.stdin.flush()

    log_line("START Driver started.")

    history = [] 

    while True:
        print("\nAvailable Commands: [password, encrypt, decrypt, history, quit]")
        cmd = input("Enter command: ").strip().lower()

        if cmd == "password":
            log_line("CMD password")
            use_history = input("Use history? (y/n): ").strip().lower()
            if use_history == "y":
                if not history:
                    print("History is empty.")
                    continue
                # Show history
                for i, val in enumerate(history):
                    print(f"{i+1}: {val}")
                choice = input("Select index or 'n' for new: ").strip().lower()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(history):
                        passkey = history[idx].upper()
                    else:
                        print("Invalid index.")
                        continue
                else:
                    passkey = input("Enter new password: ").strip()
            else:
                passkey = input("Enter new password: ").strip()

            if not passkey.isalpha():
                print("Error: password must be letters only.")
                continue

            encrypt_proc.stdin.write(f"PASS {passkey.upper()}\n")
            encrypt_proc.stdin.flush()

            resp = encrypt_proc.stdout.readline().strip()
            log_line(resp)
            if resp.startswith("ERROR"):
                print(f"Encryption Program Error: {resp}")
            else:
                print("Password updated successfully.")

        elif cmd == "encrypt":
            log_line("CMD encrypt")
            use_history = input("Use history? (y/n): ").strip().lower()
            if use_history == "y":
                if not history:
                    print("History is empty.")
                    continue
                for i, val in enumerate(history):
                    print(f"{i+1}: {val}")
                choice = input("Select index or 'n' for new: ").strip().lower()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(history):
                        to_encrypt = history[idx].upper()
                    else:
                        print("Invalid index.")
                        continue
                else:
                    to_encrypt = input("Enter text to encrypt: ").strip()
            else:
                to_encrypt = input("Enter text to encrypt: ").strip()

            if not to_encrypt.isalpha():
                print("Error: can only encrypt letters (A-Z).")
                continue

            history.append(to_encrypt.upper())

            encrypt_proc.stdin.write(f"ENCRYPT {to_encrypt.upper()}\n")
            encrypt_proc.stdin.flush()

            resp = encrypt_proc.stdout.readline().strip()
            log_line(resp)

            if resp.startswith("RESULT"):

                parts = resp.split(maxsplit=1)
                if len(parts) > 1:
                    result_text = parts[1]
                    print("Encrypted text:", result_text)

                    history.append(result_text)
            else:
                print("Encryption Program Error:", resp)

        elif cmd == "decrypt":
            log_line("CMD decrypt")
            use_history = input("Use history? (y/n): ").strip().lower()
            if use_history == "y":
                if not history:
                    print("History is empty.")
                    continue
                for i, val in enumerate(history):
                    print(f"{i+1}: {val}")
                choice = input("Select index or 'n' for new: ").strip().lower()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(history):
                        to_decrypt = history[idx].upper()
                    else:
                        print("Invalid index.")
                        continue
                else:
                    to_decrypt = input("Enter text to decrypt: ").strip()
            else:
                to_decrypt = input("Enter text to decrypt: ").strip()

            if not to_decrypt.isalpha():
                print("Error: can only decrypt letters (A-Z).")
                continue

            history.append(to_decrypt.upper())

            encrypt_proc.stdin.write(f"DECRYPT {to_decrypt.upper()}\n")
            encrypt_proc.stdin.flush()

            resp = encrypt_proc.stdout.readline().strip()
            log_line(resp)

            if resp.startswith("RESULT"):
                parts = resp.split(maxsplit=1)
                if len(parts) > 1:
                    result_text = parts[1]
                    print("Decrypted text:", result_text)
                    history.append(result_text)
            else:
                print("Encryption Program Error:", resp)

        elif cmd == "history":
            log_line("CMD history")
            print("History:")
            for i, val in enumerate(history):
                print(f"{i+1}: {val}")

        elif cmd == "quit":
            log_line("CMD quit")
            encrypt_proc.stdin.write("QUIT\n")
            encrypt_proc.stdin.flush()

            log_line("QUIT")

            log_line("STOP Driver exiting.")

            encrypt_proc.wait()
            logger_proc.stdin.close()
            logger_proc.wait()
            break

        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
