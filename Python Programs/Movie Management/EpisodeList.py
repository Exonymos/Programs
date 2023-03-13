import os

#function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

#function to show menu and get user choice
def show_menu():
    clear_console()
    print("Menu:")
    print("1. Add a new Movie/TV Show")
    print("2. Update watched episodes")
    print("3. Rename a Movie/TV Show")
    print("4. Show the Movie/TV Show Names")
    print("5. Create a new file")
    print("6. Delete an entry")
    print("7. Quit")
    choice = input("Enter your choice: ")
    return choice

#function to create a new file
def create_file():
    file_name = input("Enter the file name: ")
    if not file_name.endswith(".txt"):
        file_name += ".txt"
    if os.path.exists(file_name):
        print("File already exists!")
        return
    with open(file_name, 'w') as f:
        print("File created successfully.")

#function to read data from file and return as list
def read_data(file_name):
    with open(file_name, 'r') as f:
        data = f.readlines()
    return data

#function to write data to file
def write_data(file_name, data):
    with open(file_name, 'w') as f:
        f.writelines(data)

#function to add a new movie / tv show
def add_new_entry(file_name):
    name = input("Enter the name of the Movie/TV Show: ")
    total_episodes = input("Enter the total number of episodes: ")
    watched_episodes = input("Enter the number of watched episodes: ")
    m_type = input("Enter the type (Movie/TV Show): ")
    new_entry = f"{name}\nTotal number of episodes: {total_episodes}\nWatched episodes: {watched_episodes}\nType: {m_type}\n"
    data = read_data(file_name)
    index = len(data)
    for i, line in enumerate(data):
        if line.strip() > name:
            index = i
            break
    data.insert(index, new_entry)
    write_data(file_name, data)
    print("Entry added successfully.")

#function to update watched episodes
def update_watched_episodes(file_name):
    data = read_data(file_name)
    titles = [line.strip() for i, line in enumerate(data) if i % 4 == 0]
    titles.sort()
    print("Titles:")
    for i, title in enumerate(titles):
        print(f"{i+1}. {title}")
    choice = int(input("Enter the number of the Movie/TV Show to update: "))
    title_index = (choice - 1) * 4
    total_episodes_index = title_index + 1
    watched_episodes_index = title_index + 2
    new_watched_episodes = input("Enter the new number of watched episodes: ")
    data[watched_episodes_index] = f"Watched episodes: {new_watched_episodes}\n"
    write_data(file_name, data)
    print("Watched episodes updated successfully.")

#function to rename a movie / tv show
def rename_entry(file_name):
    data = read_data(file_name)
    titles = [line.strip() for i, line in enumerate(data) if i % 4 == 0]
    titles.sort()
    print("Titles:")
    for i, title in enumerate(titles):
        print(f"{i+1}. {title}")

    if not titles:
        print("No entries found.")
        return

    choice = int(input("Enter the number of the Movie/TV Show you want to rename: "))
    if choice < 1 or choice > len(titles):
        print("Invalid choice.")
        return

    new_title = input("Enter the new name: ")
    if not new_title:
        print("Invalid title.")
        return

    # update the file
    index = data.index(titles[choice - 1])
    data[index] = new_title
    write_data(file_name, data)
    print("Movie/TV Show renamed successfully!")
def delete_entry(file_name):
    data = read_data(file_name)
    titles = [line.strip() for i, line in enumerate(data) if i % 4 == 0]
    titles.sort()
    print("Titles:")
    for i, title in enumerate(titles):
        print(f"{i+1}. {title}")

    if not titles:
        print("No entries found.")
        return

    choice = int(input("Enter the number of the Movie/TV Show you want to delete: "))
    if choice < 1 or choice > len(titles):
        print("Invalid choice.")
        return

    confirm = input("Are you sure you want to delete this entry? (y/n): ")
    if confirm.lower() == "y": #delete the entry from the data list
        index = data.index(titles[choice - 1])
        data.pop(index + 2)
        data.pop(index + 1)
        data.pop(index)# update the file
        write_data(file_name, data)
        print("Movie/TV Show deleted successfully!")
    else :
        print("Deletion cancelled.")
def display_detailed_info(file_name):
    data = read_data(file_name)
    titles = [line.strip() for i, line in enumerate(data) if i % 4 == 0]
    titles.sort()
    print("Titles:")
    for i, title in enumerate(titles):
        print(f"{i+1}. {title}")

    if not titles:
        print("No entries found.")
        return

    choice = int(input("Enter the number of the Movie/TV Show you want to view detailed info of: "))
    if choice < 1 or choice > len(titles):
        print("Invalid choice.")
        return

    # extract the data of the selected title
    index = data.index(titles[choice - 1])
    total_episodes = int(data[index + 1].split()[-1])
    watched_episodes = int(data[index + 2].split()[-1])
    title_type = data[index + 3].split()[-1]# display the detailed info
    print(f"Title: {titles[choice-1]}")
    print(f"Total Episodes: {total_episodes}")
    print(f"Watched Episodes: {watched_episodes}")
    print(f"Type: {title_type}")
    
def main():
    file_name = input("Enter the name of the file to load: ")
    if not file_name.endswith(".txt"):
        file_name += ".txt"

    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            print(f"Created new file: {file_name}")

    while True:
        print("\nMenu:")
        print("1. Add a new Movie/TV Show")
        print("2. Update watched episodes")
        print("3. Rename a Movie/TV Show")
        print("4. Show the Movie/TV Show Names")
        print("5. Create a new file")
        print("6. Delete an entry")
        print("7. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_new_entry(file_name)

        elif choice == "2":
            update_watched_episodes(file_name)

        elif choice == "3":
            rename_entry(file_name)

        elif choice == "4":
            read_data(file_name)

        elif choice == "5":
            create_file()

        elif choice == "6":
            delete_entry(file_name)

        elif choice == "7":
            print("Exiting program...")
            break

        else :
            print("Invalid choice. Please try again.")
if __name__ == '__main__':
    main()