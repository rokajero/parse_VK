import re
import json
import time


def decode_unicode_escapes(value):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), value)


def work(name, where_files, save_path):
    print(f"Started {name}:")

    if not where_files:
        raise Exception(f"Нет файлов")

    file_names = where_files
    combined_data = []

    time_start = time.time()
    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
            for item in source_data["response"]:
                item.pop("photo_max_orig", None)
                item.pop("facebook", None)
                if "personal" in item:
                    if "religion_id" in item["personal"]:
                        item["personal"].pop("religion_id", None)

                combined_data.append(item)

    sv_path = save_path+'/'+name+'.ndjson'
    with open(sv_path, 'w', encoding='utf-8') as f:
        for item in combined_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    end_time = time.time()
    print(f"\nДанные успешно объединены и сохранены в файл: {sv_path}")
    print(f"Elapsed: {end_time-time_start}")
    combined_data.clear()


def start_json_to_nd(name, where_files, save_path):
    work(name, where_files, save_path)
