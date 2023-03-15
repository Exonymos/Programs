import json
import os

FILE_NAME = "list.json"

def create_file_if_not_exists():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            f.write("[]")

def read_file():
    create_file_if_not_exists()  # create the file if it does not exist
    with open(FILE_NAME, "r") as f:
        return json.load(f)

def write_file(data):
    create_file_if_not_exists()  # create the file if it does not exist
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)


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

def update_watched_episodes():
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
            item_choice = int(input("Enter the number of the item to update: ")) - 1
            if item_choice >= 0 and item_choice < len(items_to_display):
                entry = items_to_display[item_choice]
                entry_index = start_index + item_choice # calculate the index of the chosen item in the original data list
                print(f'Updating {entry["name"]} ({entry["watched_episodes"]}/{entry["total_episodes"]})')
                while True:
                    watched_episodes = input("Enter number of episodes watched (or type 'back' to return to the menu): ")
                    if watched_episodes == 'back':
                        break
                    elif not watched_episodes.isdigit():
                        print("Invalid input! Please enter a numeric value.")
                    elif int(watched_episodes) > entry["total_episodes"]:
                        print("Invalid input! Watched episodes cannot be greater than total episodes.")
                    else:
                        entry["watched_episodes"] = int(watched_episodes)
                        data[entry_index] = entry # update the original data list with the new watched episodes value
                        write_file(data)
                        print("Watched episodes updated successfully!")
                        print(f'Current status for {entry["name"]}: {entry["watched_episodes"]}/{entry["total_episodes"]}')
            else:
                print("Invalid choice. Please enter a valid choice.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a valid choice.")




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
        print("1. Next")
        print("2. Previous")
        print("3. Back to menu")
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
            break
        else:
            print("Invalid choice. Please enter a valid choice.")

    while True:
        choice = input("Enter your choice (1-{}): ".format(len(data)))
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(data):
            print("Invalid choice. Please enter a valid choice.")
        else:
            break
    index = int(choice) - 1
    name = input("Enter the new name for {}:".format(data[index]['name']))
    data[index]['name'] = name
    write_file(data)
    print("Entry renamed successfully!")
    
def show_list():
    data = read_file()
    total_items = len(data)
    page_size = 10
    current_page = 1
    while True:
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        items_to_display = data[start_index:end_index]
        print("\nList of Movies/TV Shows:")
        print("----------------------------")
        for i, item in enumerate(items_to_display, start=start_index + 1):
            print(f"{i}. {item['name']}")
        print("----------------------------")
        print(f"Page {current_page} of {int((total_items - 1) / page_size) + 1}")
        print("1. Next")
        print("2. Previous")
        print("3. Back to menu")
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
            break
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
        return
    
def delete_entry():
    data = read_file()
    print("Select the Movie/TV Show to delete:")
    for i in range(len(data)):
        print(f"{i+1}. {data[i]['name']}")
    while True:
        choice = input("Enter your choice (1-{}): ".format(len(data)))
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(data):
            print("Invalid choice. Please try again.")
            continue
        choice = int(choice)
        break
    item = data[choice-1]
    while True:
        confirm = input(f"Are you sure you want to delete '{item['name']}'? (y/n): ")
        if confirm.lower() == 'y':
            data.remove(item)
            write_file(data)
            print(f"'{item['name']}' has been deleted.")
            break
        elif confirm.lower() == 'n':
            print(f"'{item['name']}' was not deleted.")
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")
            
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
            add_entry()
        elif choice == '2':
            update_watched_episodes()
        elif choice == '3':
            rename_entry()
        elif choice == '4':
            show_list()
            show_details_choice = input("Do you want to see detailed information for any Movie/TV Show? (y/n): ")
            if show_details_choice.lower() == 'y':
                show_details()
        elif choice == '5':
            delete_entry()
        elif choice == '6':
            print("\nThank you for using this program!")
            print("Created by Exonymos")
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
menu()
