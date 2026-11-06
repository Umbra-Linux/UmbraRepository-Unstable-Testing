import os
import hashlib
import json

index_data = {}
root_dir = '..'  # Główny folder repozytorium jeden poziom wyżej

# Przeglądamy wszystkie katalogi w głównym folderze repozytorium
for entry in sorted(os.listdir(root_dir)):
    full_entry_path = os.path.join(root_dir, entry)
    
    if os.path.isdir(full_entry_path) and not entry.startswith('.'):
        pkg_name = entry
        pkg_dir = full_entry_path
        
        # Szukamy pliku .tar.gz wewnątrz folderu paczki
        tar_files = [f for f in os.listdir(pkg_dir) if f.endswith('.tar.gz')]
        
        for tar_file in tar_files:
            tar_path = os.path.join(pkg_dir, tar_file)
            
            # 1. Generowanie sumy SHA256 dla paczki
            sha256_hash = hashlib.sha256()
            with open(tar_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            hash_str = sha256_hash.hexdigest()
            
            # Zapisujemy plik .sha256 bezpośrednio w folderze paczki
            sha_file_path = f"{tar_path}.sha256"
            with open(sha_file_path, "w") as sf:
                sf.write(f"{hash_str}  {tar_file}\n")
            
            print(f"[SHA256] Utworzono dla: {tar_file}")
            
            # Wyciągamy wersję z nazwy pliku
            base_name = tar_file[:-7]
            if base_name.startswith(pkg_name + "-"):
                version = base_name[len(pkg_name) + 1:]
            else:
                version = "unknown"
            
            # Dodajemy do struktury index.json
            if pkg_name not in index_data:
                index_data[pkg_name] = {
                    "latest": version,
                    "versions": {}
                }
            
            # Aktualizujemy wersję (ścieżka względna w index.json to np. "Python/Python-3.14.3.tar.gz")
            index_data[pkg_name]["versions"][version] = f"{pkg_name}/{tar_file}"
            index_data[pkg_name]["latest"] = version

# 2. Zapisujemy zaktualizowany index.json w głównym katalogu repozytorium
index_json_path = os.path.join(root_dir, "index.json")
with open(index_json_path, "w") as jf:
    json.dump(index_data, jf, indent=2)

print("\n[SUKCES] Zaktualizowano index.json oraz pliki .sha256 dla wszystkich paczek!")
