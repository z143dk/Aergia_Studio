import os

def read_file_safely(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    # Try UTF-16LE first (PowerShell default)
    try:
        with open(filepath, 'r', encoding='utf-16-le') as f:
            print(f.read())
            return
    except UnicodeError:
        pass
        
    # Try UTF-16
    try:
        with open(filepath, 'r', encoding='utf-16') as f:
            print(f.read())
            return
    except UnicodeError:
        pass

    # Try UTF-8
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
            return
    except UnicodeError:
        pass
        
    # Fallback
    try:
        with open(filepath, 'r', errors='ignore') as f:
            print(f.read())
            return
    except Exception as e:
        print(f"Failed to read file: {e}")

if __name__ == "__main__":
    read_file_safely("paper_analysis.txt")
