import urllib.request
import zipfile
import io
import os
import shutil

url = 'https://github.com/ONLYOFFICE/onlyoffice-odoo/archive/refs/heads/master.zip'
addons_dir = '/home/sgc/odoo19/addons'
module_temp_name = 'onlyoffice-odoo-master'
module_final_name = 'onlyoffice_odoo'

# Paths
zip_path = os.path.join(addons_dir, 'onlyoffice.zip')
temp_extract_path = os.path.join(addons_dir, module_temp_name)
final_module_path = os.path.join(addons_dir, module_final_name)

try:
    # Download the file
    print(f"Downloading OnlyOffice module from {url}...")
    with urllib.request.urlopen(url) as response, open(zip_path, 'wb') as out_file:
        if response.status != 200:
            raise Exception(f"Download failed with status: {response.status}")
        shutil.copyfileobj(response, out_file)
    print("Download complete.")

    # Extract the zip file
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(addons_dir)
    print("Extraction complete.")

    # Rename the directory
    print(f"Renaming '{temp_extract_path}' to '{final_module_path}'...")
    if os.path.exists(final_module_path):
        shutil.rmtree(final_module_path) # Remove existing directory if it exists
    os.rename(temp_extract_path, final_module_path)
    print("Rename complete.")

finally:
    # Clean up the downloaded zip file
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"Removed temporary file: {zip_path}")

print("\nSuccessfully installed the OnlyOffice module.")
