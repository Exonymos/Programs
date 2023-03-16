# Author: Exonymos
# Github handle: Exonymos
# Date created: 14/03/2023
# Description: This program  help users keep track of movies and TV shows that they have watched or will watch.


import json
import os

FILE_NAME = "list.json"

def create_file_if_not_exists():
    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, "w") as f:
                f.write("[]")
    except Exception as e:
        print("An error occurred while creating the file:", e)

def read_file():
    try:
        create_file_if_not_exists()
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except Exception as e:
        print("An error occurred while reading the file:", e)

def write_file(data):
    try:
        create_file_if_not_exists()
        with open(FILE_NAME, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)
    except Exception as e:
        print("An error occurred while writing to the file:", e)

def wait_for_key():
    input("Press enter key to continue...")

def get_choice():
    print("1. Add a new Movie/TV Show")
    print("2. Update watched episodes")
    print("3. Rename a Movie/TV Show")
    print("4. Show Movie/TV Show names")
    print("5. Delete an entry")
    print("6. Quit")
    choice = input("Please enter your choice: ")
    return choice.strip().lower()

def add_entry():
    name = input("Enter name of the Movie/TV Show: ")
    while True:
        total_episodes = input("Enter total episodes: ")
        if not total_episodes.isdigit() or int(total_episodes) <= 0:
            print("Invalid input!")
        else:
            break
    while True:
        watched_episodes = input("Enter number of episodes watched: ")
        if not watched_episodes.isdigit() or int(watched_episodes) < 0:
            print("Invalid input!")
        elif int(watched_episodes) > int(total_episodes):
            print("Invalid input! Watched episodes cannot be greater than total episodes.")
        else:
            break
    while True:
        entry_type = input("Enter type (M for Movie, S for TV show): ")
        if entry_type.strip().lower() == "m":
            entry_type = "Movie"
            break
        elif entry_type.strip().lower() == "s":
            entry_type = "TV Show"
            break
        else:
            print("Invalid input! Please enter M or S.")
    data = read_file()
    data.append({"name": name, "total_episodes": int(total_episodes), "watched_episodes": int(watched_episodes), "type": entry_type})
    write_file(sorted(data, key=lambda x: x["name"]))
    print("Entry added successfully!")
    wait_for_key()
    os.system('cls' if os.name == 'nt' else 'clear')

def update_entry():
    data = read_file()
    total_items = len(data)
    page_size = 10
    current_page = 1
    while True:
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        items_to_display = data[start_index:end_index]
        print("\nSelect the Movie/TV Show to update watched episodes:\n")
        print("----------------------------")
        for i, item in enumerate(items_to_display, start=start_index + 1):
            print(f"{i}. {item['name']} ({item['watched_episodes']}/{item['total_episodes']})")
        print("----------------------------")
        print(f"Page {current_page} of {int((total_items - 1) / page_size) + 1}")
        if total_items <= page_size:
            print("3. Continue")
        else:
            if current_page == 1:
                print("1. Next")
            elif end_index >= total_items:
                print("2. Previous")
            else:
                print("1. Next")
                print("2. Previous")
            print("3. Continue")
        print("4. Back to menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            if end_index < total_items:
                os.system('cls' if os.name == 'nt' else 'clear')
                current_page += 1
            else:
                print("This is the last page.")
        elif choice == "2":
            if start_index > 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                current_page -= 1
            else:
                print("This is the first page.")
        elif choice == "3":
            item_choice = int(input(f"Enter the number of the title to update watched episodes(1-10): ")) - 1
            if item_choice >= 0 and item_choice < len(items_to_display):
                entry = items_to_display[item_choice]
                entry_index = start_index + item_choice # calculate the index of the chosen item in the original data list
                print(f'Updating {entry["name"]} ({entry["watched_episodes"]}/{entry["total_episodes"]})')
                while True:
                    watched_episodes = input("('!back' to return)\nEnter number of episodes watched: ")
                    if watched_episodes == '!back':
                        break
                    elif not watched_episodes.isdigit():
                        print("Invalid input!")
                    elif int(watched_episodes) > entry["total_episodes"]:
                        print("Invalid input! Watched episodes cannot be greater than total episodes.")
                    else:
                        entry["watched_episodes"] = int(watched_episodes)
                        data[entry_index] = entry # update the original data list with the new watched episodes value
                        write_file(data)
                        print("Watched episodes updated successfully!")
                        print(f'Current status for {entry["name"]}: {entry["watched_episodes"]}/{entry["total_episodes"]}')
                        wait_for_key()
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break
            else:
                print("Invalid choice.")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def rename_entry():
    data = read_file()
    total_items = len(data)
    page_size = 10
    current_page = 1
    while True:
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        items_to_display = data[start_index:end_index]
        print("\nSelect the Movie/TV Show to rename:")
        print("----------------------------")
        for i, item in enumerate(items_to_display, start=start_index + 1):
            print(f"{i}. {item['name']}")
        print("----------------------------")
        print(f"Page {current_page} of {int((total_items - 1) / page_size) + 1}")
        if total_items <= page_size:
            print("3. Continue")
        else:
            if current_page == 1:
                print("1. Next")
            elif end_index >= total_items:
                print("2. Previous")
            else:
                print("1. Next")
                print("2. Previous")
            print("3. Continue")
        print("4. Back to menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            if end_index < total_items:
                current_page += 1
            else:
                print("This is the last page.")
        elif choice == "2":
            if start_index > 0:
                current_page -= 1
            else:
                print("This is the first page.")
        elif choice == "3":
            if total_items <= page_size:
                item_choice = int(input("Enter the number of the title to rename: ")) - 1
            else:
                item_choice = int(input(f"Enter the number of the title to rename(1-10): ")) - 1
            if item_choice >= 0 and item_choice < len(items_to_display):
                entry = items_to_display[item_choice]
                entry_index = start_index + item_choice # calculate the index of the chosen item in the original data list
                name = input("Enter the new name for {}:".format(entry['name']))
                entry['name'] = name
                data[entry_index] = entry # update the original data list with the new name value
                write_file(data)
                print("Entry renamed successfully!")
                wait_for_key()
            else:
                print("Invalid choice.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a valid choice.")

def show_list():
    data = read_file()
    while True:
        print("Do you want to filter by type of content?")
        print("1. Movies")
        print("2. TV Shows")
        print("3. Both")
        print("4. Back to menu")
        filter_choice = input("Enter your choice: ")
        if filter_choice == "1":
            filtered_data = [item for item in data if item["type"] == "Movie"]
            break
        elif filter_choice == "2":
            filtered_data = [item for item in data if item["type"] == "TV Show"]
            break
        elif filter_choice == "3":
            filtered_data = data
            break
        elif filter_choice == "4":
            return
        else:
            print("Invalid choice. Please enter a valid choice.")
    total_items = len(filtered_data)
    page_size = 10
    current_page = 1
    while True:
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        items_to_display = filtered_data[start_index:end_index]
        total_pages = int((total_items - 1) / page_size) + 1
        print("\nList of Movies/TV Shows:")
        print("----------------------------")
        for i, item in enumerate(items_to_display, start=start_index + 1):
            print(f"{i}. {item['name']}")
        print("----------------------------")
        print(f"Page {current_page} of {total_pages}")
        if current_page == total_pages:
            print("1. Previous")
        elif current_page == 1:
            print("1. Next")
        else:
            print("1. Next")
            print("2. Previous")
        print("3. Show detailed info")
        print("4. Back to menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            if current_page == total_pages:
                print("This is the last page.")
            else:
                current_page += 1
        elif choice == "2":
            if current_page == 1:
                print("This is the first page.")
            else:
                current_page -= 1
        elif choice == "3":
            name_choice = input("Enter the number of the Movie/TV Show name: ")
            if not name_choice.isdigit() or int(name_choice) <= 0 or int(name_choice) > len(filtered_data):
                print("Invalid choice! Please enter a valid number.")
                continue
            item = filtered_data[int(name_choice) - 1]
            print(f"Name: {item['name']}")
            print(f"Total episodes: {item['total_episodes']}")
            print(f"Watched episodes: {item['watched_episodes']}")
            print(f"Type: {item['type']}")
            wait_for_key()
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please enter a valid choice.")

def show_details():
    data = read_file()
    while True:
        name_choice = input("('!back' to return to the menu)\nEnter the number of the Movie/TV Show name: ")
        if name_choice.lower() == "!back":
            return
        if not name_choice.isdigit() or int(name_choice) <= 0 or int(name_choice) > len(data):
            print("Invalid choice! Please enter a valid number.")
            continue
        item = data[int(name_choice) - 1]
        print(f"Name: {item['name']}")
        print(f"Total episodes: {item['total_episodes']}")
        print(f"Watched episodes: {item['watched_episodes']}")
        print(f"Type: {item['type']}")
        wait_for_key()
        return

def delete_entry():
    data = read_file()
    total_items = len(data)
    page_size = 10
    current_page = 1
    while True:
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        items_to_display = data[start_index:end_index]
        print("\nSelect the Movie/TV Show to delete:")
        print("----------------------------")
        for i, item in enumerate(items_to_display, start=start_index + 1):
            print(f"{i}. {item['name']}")
        print("----------------------------")
        print(f"Page {current_page} of {int((total_items - 1) / page_size) + 1}")
        if total_items <= page_size:
            print("3. Continue")
        else:
            if current_page == 1:
                print("1. Next")
            elif end_index >= total_items:
                print("2. Previous")
            else:
                print("1. Next")
                print("2. Previous")
            print("3. Continue")
        print("4. Back to menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            if end_index < total_items:
                current_page += 1
            else:
                print("This is the last page.")
        elif choice == "2":
            if start_index > 0:
                current_page -= 1
            else:
                print("This is the first page.")
        elif choice == "3":
            if total_items <= page_size:
                item_choice = int(input("Enter the number of the title to delete: ")) - 1
            else:
                item_choice = int(input(f"Enter the number of the title to delete(1-10): ")) - 1
            if item_choice >= 0 and item_choice < len(items_to_display):
                entry = items_to_display[item_choice]
                entry_index = start_index + item_choice # calculate the index of the chosen item in the original data list
                while True:
                    confirm = input(f"Are you sure you want to delete '{entry['name']}'? (y/n): ")
                    if confirm.lower() == 'y':
                        data.remove(entry)
                        write_file(data)
                        print(f"'{entry['name']}' has been deleted.")
                        wait_for_key()
                        break
                        
                    elif confirm.lower() == 'n':
                        print(f"'{entry['name']}' was not deleted.")
                        wait_for_key()
                        break
                        
                    else:
                        print("Invalid choice. Please enter 'y' or 'n'.")
            else:
                print("Invalid choice.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a valid choice.")

def menu():
    while True:
        print("\nMenu:")
        print("-----------------------------")
        print("1. Add a new Movie/TV Show")
        print("2. Update watched episodes")
        print("3. Rename a Movie/TV Show")
        print("4. Show Movie/TV Show List")
        print("5. Delete an entry")
        print("6. Quit")
        print("-----------------------------")
        choice = input("Please enter your choice: ")
        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            add_entry()
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            update_entry()
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            rename_entry()
        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            show_list()
        elif choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            delete_entry()
        elif choice == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nThank you for using this program!")
            print("Created by Exonymos")
            print("Exiting program. Goodbye!\n")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid choice. Please try again.")
            
menu()