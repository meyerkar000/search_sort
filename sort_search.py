"""
Author: Kara Meyer
Date: 2-4-2020
Description: This program can sort a list and then you are able to search the
list using a sort and search algorithms.
"""

# Used Imports
import requests
import json


def create_link(item_id):
    """Create the link using API."""
    link = f"https://api.guildwars2.com/v2/items/{item_id}"
    return link


def get_response(link):
    """Return the response to an API key."""
    response = requests.get(link)
    return response


def print_one_string(response):
    """Print the response in one long string."""
    print(response.json())


def find(response, api_variable):
    """Find the variable and return its data."""
    response_string = response.text
    full_dict = json.loads(response_string)
    data = full_dict[api_variable]
    return data


def txt_of_ids():
    """Create a text document of the item ids."""
    id_link = create_link("")
    response = get_response(id_link)
    raw_data = response.text.splitlines()

    item_ids = []
    for index in range(1, len(raw_data)-1, 64):  # 1/64 of items
        string = raw_data[index]
        remove_extra = ''.join([i for i in string if i.isdigit()])
        item_ids.append(remove_extra)

    file = open("item_ids.txt", "w")
    for id_number in item_ids:
        file.write(f"{id_number}\n")
    file.close()


def txt_of_items():
    """Create a text document of the items."""
    id_file = open("item_ids.txt", "r")
    item_id_list = id_file.read().splitlines()

    item_file = open("gw2_items.txt", "w")
    for index in range(0, len(item_id_list)):
        item_link = create_link(item_id_list[index])
        response = get_response(item_link)
        title = find(response, "name")
        if title.startswith("("):
            continue
        else:
            item_file.write(f"{title}\n")
    item_file.close()


def sort_list(unsorted_list):
    """Sorts a list alphabetically and by name length and returns a new list."""
    """Uses selection sort algorithm."""
    for index in range(len(unsorted_list)):
        min_index = index
        for i in range(index + 1, len(unsorted_list)):
            if unsorted_list[min_index] > unsorted_list[i]:
                min_index = i
        unsorted_list[index], unsorted_list[min_index] = unsorted_list[min_index], unsorted_list[index]
    return unsorted_list


def binary_search(sorted_list, search_item):
    """Returns the index of the item that's being searched."""
    left = 0
    right = len(sorted_list) - 1
    count = 0
    while left <= right and count < 15:
        count += 1
        mid = (left + right) // 2
        if sorted_list[mid] == search_item:
            return mid
        elif sorted_list[mid] < search_item:
            left = mid + 1
        else:  # sorted_list[mid] > search_item
            right = mid - 1
    return -1  # If element was not found


# Create a txt of all possible item IDs.
# txt_of_ids()

# Create a txt of gw2 items.
# txt_of_items()

# Create a list of the gw2 items.
item_file = open("gw2_items.txt", "r")
gw2_items = item_file.read().splitlines()

# Sort the list.
sorted_list = sort_list(gw2_items)
print(sorted_list)
print(binary_search(sorted_list, "32-Slot Orichalcum Locker"))
