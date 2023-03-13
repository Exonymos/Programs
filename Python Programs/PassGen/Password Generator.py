import random
import array

# Keep asking for input until the user enters a valid input
while True:
    passlen = int(input("Enter the length of password (minimum 5): "))
    if passlen < 5 or passlen == 0:
        print("Minimum length is 5. Please try again.")
    else:
        break

# Here, I have taken four arrays, one for DIGITS, second for lowercase character as LOWCASE_CHARACTERS, 
# third for uppercase character as UPCASE_CHARACTERS and fourth for SYMBOLS
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

LOWCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
					  'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
					  'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
					  'z']

UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
					 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
					 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
					 'Z']

SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>','*', '(', ')', '<']

# Combining all character arrays above to form one array
COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOWCASE_CHARACTERS + SYMBOLS

# Randomly selecting at least one character from each character set above
rand_digit = random.choice(DIGITS)
rand_upper = random.choice(UPCASE_CHARACTERS)
rand_lower = random.choice(LOWCASE_CHARACTERS)
rand_symbol = random.choice(SYMBOLS)

temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol


for x in range(passlen - 4):
	temp_pass = temp_pass + random.choice(COMBINED_LIST)

	temp_pass_list = array.array('u', temp_pass)
	random.shuffle(temp_pass_list)

password = ""
for x in temp_pass_list:
		password = password + x
		
print("Your Generated Password is:",password)
