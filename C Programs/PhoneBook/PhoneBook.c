/*
Phonebook
*/



#include<stdio.h>
#include<conio.h>
#include<stdlib.h>
#include<ctype.h>
#include<string.h>
#define MAXDB 500    //Maximum number of entries in the phonebook


// List of Globe variables
int i;    //globe index
long int phone[MAXDB+1];
int room[MAXDB+1];
//phone_tmp & room_tmp array's are temp storage used for delete recovery
long int phone_tmp[MAXDB+1];
int room_tmp[MAXDB+1];
void AddEntry(int, long int);
int add_count=0;    //master counter for entries added
int current_e_add;    //counter for current entries added within a giventime.
int DeleteEntry(int, long int);
int FindPhone(long int);
int FindRoom(int);
int phone_found, room_found;
int del_entry;    //counts del entry at a given time
int tot_del_entry=0;    //master del counter
int ListAll (void);
int SortAllEntries (char);
int GeTotalEntries (void);
int chkstrdig (char str[], int range);
char menu (void);
void LoadDB (void);    //load database from file function
void exitmenu (void);
void drawscreen (void);
void refreshscreen (void);

char dbload [80];    //loaded database

int main(void)
{
char iroom [80], iphone [80],add_quit;
char option, sortopt, exit_opt;    //menu, sort and exit option
int phone_check, room_check, delete_check, sort_check, list_check;
int iroom_search, iroom_del;
int int_iroom, total_entries;
int error_iphone, error_iroom;    //used to check inputs error's
long int longint_iphone;
long int iphone_search;
long int iphone_del;

//Init while no valid database file is loaded program will work in RAM!
strcpy (dbload, "No database file loaded (RAM MODE!).");

//MAIN MENU
do
    {
        do
        { option = menu();
        if (option == '1')    //Add Entry Option
        { current_e_add=0;    //init current entries added to zero
for (i=add_count; i < MAXDB; i++)
{   clrscr();
    refreshscreen();
    drawscreen();
    gotoxy(1,4);
    printf(">> Add Entry <<");
    gotoxy(1,25);
    cprintf("Please Add Your Entry, leave blank to quit to Main Menu");
    gotoxy(1,6);
    printf("Enter Room Number [%3d]: ",i+1);
    fgets (iroom);

    if (iroom [0] == '\0')    //user hits enter - quits
    {   gotoxy (1,25);
        cprintf("You chose to quit: Entry %d was not added to the database.",i+1);
        getch();
        break;
    }
    printf("Enter Phone Number [%3d] : ",i+1);
    fgets (iphone);

    if (iphone [0] == '\0')    //user hits enter - quits
    {   gotoxy (1,25);
        cprintf("You chose to quit: Entry %d was not added to the database.",i+1);
        getch();
        break;
    }
    //check the string for valid inputs
    error_iroom = chkstrdig (iroom, 4);
    error_iphone = chkstrdig (iphone,8);
    //loop's while room input error (out of range/character)
    while(error_iroom != 0)
    {   if (error_iroom == -1)
        {   clrscr();
            refreshscreen();
            drawscreen();
            gotoxy (1,4);
            printf(">> Add Entry <<");
            gotoxy(1,25);
            cprintf("Error: Room Number - out of Range, Your entry was greater than 4 digits. ");
            gotoxy(1,6);
            printf("Renter Room Number [%3d]: ",i+1);
            fgets (iroom);
        }
        if (error_iroom == -2)
        {   clrscr();
            refreshscreen();
            drawscreen();
            gotoxy(1,4);
            printf("*** Add Entry ***");
            gotoxy (1,25);
            cprintf("Error: Room Number - Character(s) detected, character(s) are not allowed.");
            gotoxy (1,6);
            printf("Renter Room Number [%3d]: ",i+1);
            fgets (iroom);
        }    //checks string room input if valid
        error_iroom = chkstrdig (iroom, 4);
    }    //loop's while phone input error (out of range/character)
    while(error_iphone !=0)
    {   if (error_iphone == -1)
        {   clrscr();
            refreshscreen();
            drawscreen();
            gotoxy(1,4);
            printf(">> Add Entry <<");
            gotoxy (1,25);
            cprintf("Error: Phone Number - out of Range, Your entry was greater than 8 digits. ");
            gotoxy (1,6);
            printf("Room Number[%3d]: ",i+1);
            gotoxy (1,7);
            printf("Renter Phone Number [%3d]: ",i+1);
            fgets (iphone);
        }
        if (error_iphone == -2)
        {   clrscr();
            refreshscreen();
            drawscreen();
            gotoxy (1,4);
            printf(">>Add Entry <<");
            gotoxy(1,25);
            cprintf("Error: Phone Number - Character(s) detected, character(s)are not allowed.");
            gotoxy(1,6);
            printf("Room Number [%3d] Entry: %s",i+1, iroom);
            gotoxy (1,7);
            printf("Renter Phone Number [%3d] : ",i+1);
            fgets (iphone);
        }    //checks phone input valid
        error_iphone = chkstrdig (iphone,8);
    }
    //no room or phone input error - addentry
    if (error_iroom == 0 && error_iphone == 0)
    {   int_iroom = atoi (iroom);    //converts string to int
        longint_iphone = atol (iphone);    //converts string to long int
        current_e_add++;
        AddEntry (int_iroom, longint_iphone);
    }
}
if (add_count == MAXDB)    //database full
{   gotoxy (1,25);
    cprintf("\aDatabase is full!: %d entries were added, ",add_count);
    cprintf("that is the Maximum No. I can hold.");
    getch();
}
    }
    else
    if (option == '2')    //DeleteEntry option
    {   del_entry = 0;    //Initialize del_entry counter zero
    clrscr();
    refreshscreen();
    drawscreen();
    gotoxy (1,4);
    printf(">> Delete Entry <<");
    gotoxy(1,6);
    printf("Enter room number to delete: ");
    scanf("%d",&iroom_del);
    flushall();    //clears buffer

    printf("Enter phone number to delete: ");
    scanf("%ld",&iphone_del);
    flushall();

    delete_check = DeleteEntry (iroom_del, iphone_del);

    if (delete_check == 0)    //successfully found or deleted entriesdisplay
    {   gotoxy(1,25);
        cprintf("Successful: There are currently %d entries in the database,", add_count);
        cprintf("deleted %d.",del_entry);
        getch();
    }
    if (delete_check == -1)    //error: does not delete if db not found
    {   gotoxy(1,25);
        cprintf("Error: The Room No./Phone No. You're looking for was Not Found.");
        getch();
    }
}
else
if (option == '3')    //FindPhone Option
{   phone_found = 0;    //initialize phone no. found to zero
    clrscr();
    refreshscreen();
    drawscreen();
    gotoxy (1,4);
    printf(">> Find Room Number <<");

    gotoxy (1,6);
    printf("Enter the phone number to search for: ");
    scanf("%ld", &iphone_search);
    flushall();    //clears buffer

    phone_check = FindPhone (iphone_search);
    if (phone_check == 0)    //return = 0 Phone found
    {   gotoxy(1,25);
        cprintf("Successful: There are currently %d entries in the database,",add_count);
        //phone_found (globe), counts phone no. found (within FindPhone function
        printf("found %d.", phone_found);
        getch();
    }
    if (phone_check == -1)    //return = -1 Phone not found
    {   gotoxy (1,25);
        cprintf("Error: The Phone No. You're looking for was Not Found.");
        getch();
    }
}
else
if (option == '4') /* FindRoom Option */
{   room_found = 0; /* initialize room no. found to zero */
    clrscr();
    refreshscreen();
    drawscreen();
    gotoxy (1,4);
    printf(">> Find Phone Number <<");

    gotoxy (1,6);
    printf("Enter the room number to search for: ");
    scanf("%d", &iroom_search);
    flushall();

    room_check = FindRoom (iroom_search);

    if (room_check == 0) /* return = 0 Room found */
    {   gotoxy (1,25);
        cprintf("Successful: There are currently %d entries in the database,",add_count);
        //room found is globe it counts room no. found in FindRoom function
        cprintf("found id.", room found);
        getch():
    }
    if (room check == -1) /* return = -1 Room was not found */
    {   gotoxy(1,25);
        cprintf("Error: The Room No. Your looking for was Not Found.");
        getch();
    }

}
else
if (option == '5') /* ListAll option */
{   clrscr();
refreshscreen();
drawscreen();
gotoxy (1,4);
printf(">> ListAll <<\n\n");

list_check = ListAll();

if (list_check == 0)    //return 0 if entries are in database
{   gotoxy(1,25);
cprintf("List Sucuessful");
getch()
}
if (list_check == -1) /* return -1 - emptylist */
{
    gotoxy(1,25);
cprintf("Empty List");
getch();
}
}
else
if (option == '6') /* Getotalentries option */ 
{   total_entries = GeTotal_Entries();
gotoxy(1,25);
cprintf("There are currently %d entries stored in the Database.", total_entries);
getch();
}
else
//exonymos
if (option
==
'7') /* Sort Option */
{ clrscr();
refreshscreen(); drawscreen(); gotoxy (1,4);
printf(">> Sort All Entries <<"); gotoxy(1,6);
printf("Press 'A' to sort database in [A] scending order"); gotoxy (1,7);
printf("Press 'D' to sort database in [D]escending order."); gotoxy (1,9);
printf("Note: Database is sorted by phone no. entries."); sortopt = getch();
flushall();
sort check = SortAllEntries (sortopt); getch();
if (sort_check == 0) /* return = 0 - entries, in db & was sorted */ {gotoxy (1,25);
}
cprintf("Database was successfully Sorted.
getch();
if (sort_check == -1) /* return = -1 - if db is empty */ { gotoxy (1,25);
cprintf("Database was not sorted - Database is empty!"); getch();
else
if (option == '8') /* Load Database from file option */ { clrscr();
refreshscreen();
drawscreen();
gotoxy (1,4);
printf(">> Load Database <<");
LoadDB();
else
if (option == '9') /* exit option */
{ gotoxy (1,25);
cprintf("Do you really want to exit?, Press 'Y' to confirm, anykey to
cancel");
exit_opt = getch();
flushall();
if (exit_opt == 'y' || exit_opt ==
'Y')