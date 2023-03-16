#include <iostream>
#include <limits>
#include <cstdio>
#include <cstdlib>

using namespace std;

int main() {
    int choice;
    float temperature;

    while (true) {
        // Display menu options and get user choice
        cout << "Select the type of temperature to convert: " << endl;
        cout << "1. Celsius to Fahrenheit" << endl;
        cout << "2. Fahrenheit to Celsius" << endl;
        cout << "3. Celsius to Kelvin" << endl;
        cout << "4. Kelvin to Celsius" << endl;
        cout << "5. Fahrenheit to Kelvin" << endl;
        cout << "6. Kelvin to Fahrenheit" << endl;
        cout << "7. Quit" << endl;
        cout << "Enter your choice: ";

        // Get user input and handle errors
        while (!(cin >> choice) || choice < 1 || choice > 7) {
            if (cin.fail()) {
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }
            cout << "Invalid input! Please enter a number between 1 and 7: ";
        }

        // If the user chose to quit, exit the program
        if (choice == 7) {
            break;
        }

        // Prompt user to enter temperature value
        cout << "Enter temperature value: ";

        // Get user input and handle errors
        while (!(cin >> temperature)) {
            if (cin.fail()) {
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }
            cout << "Invalid input! Please enter a number: ";
        }

        // Convert temperature based on user choice
        switch (choice) {
            case 1:
                temperature = temperature * 9 / 5 + 32;
                cout << "Temperature in Fahrenheit: " << temperature << " degrees Fahrenheit" << endl;
                system("pause");
                system("cls");
                break;
            case 2:
                temperature = (temperature - 32) * 5 / 9;
                cout << "Temperature in Celsius: " << temperature << " degrees Celsius" << endl;
                system("pause");
                system("cls"); 
                break;
            case 3:
                temperature = temperature + 273.15;
                cout << "Temperature in Kelvin: " << temperature << " degrees Kelvin" << endl;
                system("pause");
                system("cls"); 
                break;
            case 4:
                temperature = temperature - 273.15;
                cout << "Temperature in Celsius: " << temperature << " degrees Celsius" << endl;
                system("pause");
                system("cls"); 
                break;
            case 5:
                temperature = (temperature + 459.67) * 5 / 9;
                cout << "Temperature in Kelvin: " << temperature << " degrees Kelvin" << endl;
                system("pause");
                system("cls"); 
                break;
            case 6:
                temperature = temperature * 9 / 5 - 459.67;
                cout << "Temperature in Fahrenheit: " << temperature << " degrees Fahrenheit" << endl;
                system("pause");
                system("cls"); 
               break;
            default:
                cout << "Invalid input! Please try again." << endl;
                system("pause");
                system("cls"); 
                break;
        }
    }

    return 0;
}
