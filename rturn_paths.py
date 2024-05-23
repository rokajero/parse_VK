import glob
import os


def return_paths(left, right, dir_path):
    directory_path = dir_path
    file_pattern = os.path.join(directory_path, 'data_users*.json')
    file_list = glob.glob(file_pattern)

    filtered_files = []
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        base_name = file_name.replace('data_users', '').replace('.json', '')

        parts = base_name.split('_')

        if len(parts) == 1:
            number = int(parts[0])
            if left <= number <= right:
                filtered_files.append(file_path)
        elif len(parts) == 2:
            number1 = int(parts[0])
            number2 = int(parts[1])
            if (left <= number1 <= right) and (number2 == 2):
                filtered_files.append(file_path)

    filtered_files.sort()
    return filtered_files
