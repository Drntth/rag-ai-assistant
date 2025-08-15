import os
import shutil


def clear_directory(dir_path):
    if not os.path.exists(dir_path):
        return
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error occurred while deleting {file_path}: {e}")


if __name__ == "__main__":
    clear_directory("data/images")
    clear_directory("data/temp")
