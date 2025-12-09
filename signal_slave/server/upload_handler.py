import os

UPLOAD_ROOT = "/home/lgvision/Pictures/slave_uploads"

def save_uploaded_file(file_storage, slave_id):
    # Create slave-specific folder
    slave_folder = os.path.join(UPLOAD_ROOT, slave_id)
    os.makedirs(slave_folder, exist_ok=True)

    # Full save path
    filename = file_storage.filename
    save_path = os.path.join(slave_folder, filename)

    file_storage.save(save_path)

    print(f"[UPLOAD] Saved file for {slave_id}: {save_path}")

    return save_path
