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
    print("Select the Movie/TV Show to update watched episodes:")
    for i in range(len(data)):
        print(f"{i+1}. {data[i]['name']}")
    while True:
        choice = input("Enter your choice (1-{}): ".format(len(data)))
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(data):
            print("Invalid input! Please enter a valid choice.")
        else:
            break
    entry = data[int(choice)-1]
    print(f"Updating {entry['name']}")
    while True:
        watched_episodes = input("Enter number of episodes watched: ")
        if not watched_episodes.isdigit():
            print("Invalid input! Please enter a numeric value.")
        elif int(watched_episodes) > entry["total_episodes"]:
            print("Invalid input! Watched episodes cannot be greater than total episodes.")
        else:
            entry["watched_episodes"] = int(watched_episodes)
            break
    write_file(data)
    print("Watched episodes updated successfully!")

def rename_entry():
    data = read_file()
    print("Select the Movie/TV Show to rename:")
    for i in range(len(data)):
        print(f"{i+1}. {data[i]['name']}")
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
    print("\nList of Movies/TV Shows:")
    print("-----------------------------")
    for item in data:
        print(item['name'])
    print("-----------------------------\n")
    
def show_details():
    data = read_file()
    while True:
        name = input("('!back' to return to the menu)\nEnter the name of the Movie/TV Show: ")
        if name.lower() == '!back':
            return
        for item in data:
            if name.lower() == item['name'].lower():
                print(f"Name: {item['name']}")
                print(f"Total episodes: {item['total_episodes']}")
                print(f"Watched episodes: {item['watched_episodes']}")
                print(f"Type: {item['type']}")
                return
        print("Entry not found!. Please enter the correct name.")
    
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
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
menu()
