import json
import datetime
import os

path = "./cache/"

def save_dict_to_file(dictionary, filename):
    print(f"Saving dictionary to {filename}")
    with open(filename, "w") as file:
        json.dump(dictionary, file, indent=4)


def load_dict_from_file(filename):
    print(f"Loading dictionary from {filename}")
    with open(filename, "r") as file:
        return json.load(file)

def get_cache_filename(entity, today=False):
    """Checks if a cache file exists for a given entity."""
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    if today:
        cache_filename = f"{path}{date}_{entity}.json"
    else:
        cache_filename = f"{path}{entity}.json"
    return cache_filename


def does_cache_exist(cache_filename):
    """Checks if a cache file exists for a given entity."""
    # cache_filename = get_cache_filename(entity, today)
    if os.path.exists(cache_filename):
        return True
    else:
        return False

if not os.path.exists(path):
    os.makedirs(path)
    print(f"Created cache directory: {path}")


# # Example usage
# data = {"name": "Alice", "age": 25, "city": "New York"}
# save_dict_to_file(data, "data.json")

# # Reload dictionary
# loaded_data = load_dict_from_file("data.json")
# print(loaded_data)

# if __name__ == "__main__":
#     data = {"name": "Alice", "age": 25, "city": "New York"}
#     save_dict_to_file(data, "data.json")

#     # Reload dictionary
#     loaded_data = load_dict_from_file("data.json")
#     print(loaded_data)
