from schwab_api import config
import sys

def main():
    key = config.APP_KEY
    secret = config.APP_SECRET
    
    print(f"Key repr: {repr(key)}")
    print(f"Secret repr: {repr(secret)}")
    
    if key:
        print(f"Key bytes: {[ord(c) for c in key]}")
    if secret:
        print(f"Secret bytes: {[ord(c) for c in secret]}")

if __name__ == "__main__":
    main()
