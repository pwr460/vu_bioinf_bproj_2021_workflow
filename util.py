import os
import shutil


def get_folder_full_path(folder_path):
    is_abs = os.path.isabs(folder_path)
    if is_abs:
        return folder_path

    working_dir = os.getcwd()
    return os.path.join(working_dir, folder_path)


def move_folder_content(source_dir, target_dir):
    file_names = os.listdir(source_dir)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


def clear_temp_folders(tmp_source_dir, search_depth = 1):
    for f in os.listdir(tmp_source_dir):
        f_path = os.path.join(tmp_source_dir, f)
        try:
            if os.path.isfile(f_path) or os.path.islink(f_path):
                os.unlink(f_path)
            elif os.path.isdir(f_path):
                if search_depth <= 0:
                    shutil.rmtree(f_path)
                else:
                    clear_temp_folders(f_path, search_depth - 1)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (f_path, e))
