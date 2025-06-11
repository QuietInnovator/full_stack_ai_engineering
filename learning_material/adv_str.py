# Ask user for a password—ensure it’s alphanumeric.
password = input("Enter a password: ")
if password.isalnum():
    print("Password is valid")
else:
    print("Password is invalid")

# Ask for a title—verify with istitle().
title = input("Enter a title: ")
if title.istitle():
    print("Title is valid")
else:
    print("Title is invalid")

# Convert messy input to all lowercase.
messy_input = "AsFgsrgjp'rgk;'agf;jkFKSERFdsSDFBDFSA"
print(messy_input.lower())