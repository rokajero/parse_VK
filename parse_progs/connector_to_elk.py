from elasticsearch import Elasticsearch, helpers
import json
import time
import os


def connect_to_elasticsearch(hosts):
    es = Elasticsearch(hosts, ca_certs='E:\ELK\kibana-8.13.4\data\ca_1715813545106.crt') #, basic_auth=("elastic","Cookies3205XZ#"))
    if not es.ping():
        raise ValueError("Connection failed")
    print("Connected")
    print(es.info())
    return es


def create_index(es, index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    else:
        print("Index exist, stop program for safety...")
        exit()


def read_ndjson(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)


def bulk_index_to_elasticsearch(es, index_name, data):
    actions = [
        {
            "_index": index_name,
            "_source": document,
        }
        for document in data
    ]
    helpers.bulk(es, actions)


def main():
    es_hosts = ["https://localhost:9200"]
    ndjson_folder_path = input("Input name of the folder: ")

    print("Trying to connect Elasticsearch ...")
    try:
        es = connect_to_elasticsearch(es_hosts)
    except Exception as e:
        print(f"Connection to ELK not established, exiting...\nException: {e}")
        time.sleep(5)
        exit()

    files = [f for f in os.listdir(ndjson_folder_path) if f.endswith('.ndjson')]

    for file_name in files:
        start_time = time.time()
        print(f"Started file: {file_name}")
        try:

            index_name = "test-mil" + os.path.splitext(file_name)[0][1:]
            ndjson_file_path = os.path.join(ndjson_folder_path, file_name)

            print("\nTrying to create index ...")
            create_index(es, index_name)
            print(f"Index {index_name} created!!!")

            print("\nTrying to upload data from file ...")
            data = read_ndjson(ndjson_file_path)
            print(f"Data from {ndjson_file_path} downloaded!!!")

            print("\nTrying to upload data to index ...")
            bulk_index_to_elasticsearch(es, index_name, data)
            print("Done!!!")
        except Exception as e:
            input(f"\nException occurred, press Enter to close... \nException: {e}")
            exit()

        print(f"Uploaded file: {file_name}")
        print(f"\n---------------------------------------------------\nElapsed time: {time.time() - start_time}")


if __name__ == "__main__":
    main()
