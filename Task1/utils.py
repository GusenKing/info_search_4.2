import hashlib
import os
import zipfile


def zip_folder(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)

                rel_path = os.path.relpath(full_path, folder_path)

                zipf.write(full_path, rel_path)


def url_to_filename(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest() + ".txt"
