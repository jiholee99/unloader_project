import os

def get_latest_file(folder_path):
    """Return the filename of the latest file in the given folder."""
    try:
        files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]

        if not files:
            return None  # folder empty

        latest_file = max(files, key=os.path.getmtime)
        return latest_file

    except Exception as e:
        print("Error while finding latest file:", e)
        return None
