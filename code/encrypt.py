#!/usr/bin/env python3

import sys

current_passkey = None

def vigenere_encrypt(plaintext, key):
    cipher = []
    klen = len(key)
    for i, ch in enumerate(plaintext):
        pval = ord(ch) - ord('A')
        kval = ord(key[i % klen]) - ord('A')
        encrypted_val = (pval + kval) % 26
        cipher.append(chr(encrypted_val + ord('A')))
    return "".join(cipher)

def vigenere_decrypt(ciphertext, key):
    plain = []
    klen = len(key)
    for i, ch in enumerate(ciphertext):
        cval = ord(ch) - ord('A')
        kval = ord(key[i % klen]) - ord('A')
        decrypted_val = (cval - kval) % 26
        plain.append(chr(decrypted_val + ord('A')))
    return "".join(plain)

def main():
    global current_passkey

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue

        parts = line.split(maxsplit=1)
        command = parts[0]
        argument = ""
        if len(parts) > 1:
            argument = parts[1]

        command = command.upper()

        if command == "QUIT":
            break

        elif command == "PASS":
            current_passkey = argument.upper()
            print("RESULT")
            sys.stdout.flush()

        elif command == "ENCRYPT":
            if current_passkey is None:
                print("ERROR Password not set")
                sys.stdout.flush()
            else:
                if not argument.isalpha():
                    print("ERROR Invalid characters for encryption")
                    sys.stdout.flush()
                else:
                    argument = argument.upper()
                    encrypted = vigenere_encrypt(argument, current_passkey)
                    print(f"RESULT {encrypted}")
                    sys.stdout.flush()

        elif command == "DECRYPT":
            if current_passkey is None:
                print("ERROR Password not set")
                sys.stdout.flush()
            else:
                if not argument.isalpha():
                    print("ERROR Invalid characters for decryption")
                    sys.stdout.flush()
                else:
                    argument = argument.upper()
                    decrypted = vigenere_decrypt(argument, current_passkey)
                    print(f"RESULT {decrypted}")
                    sys.stdout.flush()
        else:
            print("ERROR Unknown command")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
