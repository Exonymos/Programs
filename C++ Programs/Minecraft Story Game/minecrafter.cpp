#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

const int INVENTORY_SIZE = 10;
const int DAY_LENGTH = 15; // added constants for day and night lengths
const int NIGHT_LENGTH = 7;

int main() {
    srand(time(0)); // seed for random number generation
    int playerScore = 0;
    bool keepPlaying = true;
    bool isDaytime = true;
    int inventory[INVENTORY_SIZE] = { 0 };
    int numItems = 0;

    cout << "Welcome to Minecraft Story Game!" << endl;

    while (keepPlaying) {
        // Check time of day
        if (isDaytime) {
            cout << "It's daytime!" << endl;
            cout << "You have " << DAY_LENGTH << " seconds to explore." << endl;
            cout << "What do you want to do?" << endl;
        } else {
            cout << "It's nighttime!" << endl;
            cout << "You have " << NIGHT_LENGTH << " seconds to explore." << endl;
            cout << "Be careful, monsters come out at night." << endl;
            cout << "What do you want to do?" << endl;
        }
        cout << "1. Go mining" << endl;
        cout << "2. Explore" << endl;
        cout << "3. Check inventory" << endl;
        cout << "4. Quit" << endl;

        int choice;
        cin >> choice;

        if (choice == 1) {
            cout << "You are mining..." << endl;
            int ore = rand() % 10; // random ore from 0 to 9
            if (ore < 2) { // 20% chance of finding coal
                cout << "You found coal!" << endl;
                inventory[numItems++] = 1; // add coal to inventory
            } else if (ore < 4) { // 20% chance of finding iron
                cout << "You found iron!" << endl;
                inventory[numItems++] = 2; // add iron to inventory
            } else if (ore < 6) { // 20% chance of finding gold
                cout << "You found gold!" << endl;
                inventory[numItems++] = 3; // add gold to inventory
            } else if (ore < 8) { // 20% chance of finding redstone
                cout << "You found redstone!" << endl;
                inventory[numItems++] = 4; // add redstone to inventory
            } else { // 20% chance of finding lapis lazuli
                cout << "You found lapis lazuli!" << endl;
                inventory[numItems++] = 5; // add lapis lazuli to inventory
            }

            int monsterProb = rand() % 10; // random number from 0 to 9
            if (!isDaytime && monsterProb < 7) { // 70% chance of encountering a monster at night
                cout << "While mining, you encounter a zombie!" << endl;
                playerScore -= 30;
            } else {
                cout << "Phew! No monsters this time." << endl;
            }
        } else if (choice == 2) {
            cout << "You are exploring..." << endl;
            int monsterProb = rand() % 10; // random number from 0 to 9
            if (!isDaytime && monsterProb < 3) { // 30% chance of encountering a monster at night
                cout << "While exploring, you encounter a creeper!" << endl;
                playerScore -= 50;
            } else {
                int ore = rand() % 6; // random ore from 0 to 5
                if (ore == 0) {
                    cout << "You found coal!" << endl;
                    inventory[numItems++] = 1; // add coal to inventory
                } else if (ore == 1) {
                    cout << "You found iron!" << endl;
                    inventory[numItems++] = 2; // add iron to inventory
                } else if (ore == 2) {
                    cout << "You found gold!" << endl;
                    inventory[numItems++] = 3; // add gold to inventory
                } else if (ore == 3) {
                    cout << "You found diamond!" << endl;
                    inventory[numItems++] = 4; // add diamond to inventory
                } else if (ore == 4) {
                    cout << "You found emerald!" << endl;
                    inventory[numItems++] = 5; // add emerald to inventory
                } else {
                    cout << "You didn't find any rare ores this time." << endl;
                }
            }
        } else if (choice == 3) {
            cout << "Your inventory: " << endl;
            if (numItems == 0) {
                cout << "Empty!" << endl;
            } else {
                for (int i = 0; i < numItems; i++) {
                    if (inventory[i] == 1) {
                        cout << "- Coal" << endl;
                    } else if (inventory[i] == 2) {
                        cout << "- Iron" << endl;
                    } else if (inventory[i] == 3) {
                        cout << "- Gold" << endl;
                    } else if (inventory[i] == 4) {
                        cout << "- Diamond" << endl;
                    } else if (inventory[i] == 5) {
                        cout << "- Emerald" << endl;
                    }
                }
            }
        } else if (choice == 4) {
            keepPlaying = false;
        } else {
            cout << "Invalid input. Please choose 1, 2, 3, or 4." << endl;
        }
        if (numItems == INVENTORY_SIZE) {
            cout << "Your inventory is full!" << endl;
        }

        // Check if day/night has ended
        if (isDaytime) {
            if (DAY_LENGTH == 0) {
                isDaytime = false;
                // reset day length to original value
            } else {
                
            }
        } else {
            if (NIGHT_LENGTH == 0) {
                isDaytime = true;
                // reset night length to original value
            } else {
                
            }
        }

    }

    cout << "Your score is: " << playerScore << endl;
    cout << "Thanks for playing!" << endl;
    return 0;
}
