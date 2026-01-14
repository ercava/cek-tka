import os
import hashlib
import json

# Secret salt to make filenames unpredictable
SALT = "ercava_secret_2024"

CERT_DIR = "certificates"
JS_FILE = os.path.join("data", "results.js")

def generate_hash(nisn):
    # Create an unpredictable hash for the NISN
    return hashlib.sha256((nisn + SALT).encode()).hexdigest()[:12]

def obfuscate():
    if not os.path.exists(CERT_DIR):
        print(f"Error: {CERT_DIR} directory not found.")
        return

    mapping = {}
    files = [f for f in os.listdir(CERT_DIR) if f.lower().endswith('.pdf')]
    
    print(f"Processing {len(files)} certificates...")

    for filename in files:
        # Extract 10-digit NISN from filename (e.g., '0089126771 - SITI RAQIQA FAHHAMA.pdf')
        import re
        match = re.search(r'\d{10}', filename)
        if not match:
            print(f"Skipping {filename}: NISN not found.")
            continue
            
        nisn = match.group(0)
        h = generate_hash(nisn)
        new_filename = f"cert_{nisn}_{h}.pdf"
        
        old_path = os.path.join(CERT_DIR, filename)
        new_path = os.path.join(CERT_DIR, new_filename)
        
        # Rename the file
        try:
            os.rename(old_path, new_path)
            mapping[nisn] = new_filename
        except Exception as e:
            print(f"Failed to rename {filename}: {e}")

    # Append mapping to results.js
    if os.path.exists(JS_FILE):
        with open(JS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Clean up existing mapping if any (to avoid duplicates if script is run twice)
        if "window.CERT_MAPPING =" in content:
            content = content.split("window.CERT_MAPPING =")[0].strip()
        
        with open(JS_FILE, "w", encoding="utf-8") as f:
            f.write(content + "\n\n")
            f.write(f"window.CERT_MAPPING = {json.dumps(mapping, indent=2)};\n")
            
    print("Obfuscation complete. Mapping updated in data/results.js")

if __name__ == "__main__":
    obfuscate()
