# Password Manager
A simple password creator and manager made from Python

This file will generate cryptographically secure passwords and save them on your system as an encrypted bytes array.

You can save passwords, set your existing passwords from other password managers, and load the passwords you have saved. 

Other than writing your own passwords into the password setter function, your passwords will never appear on the screen and will be copied directly into your clipboard for easy use and security.

# Setup
At this time, running this program requires a Python installation. It was written using Python 3.9, but should work with most (recent) versions of Python. Soon it will be a full-fledged .exe application.
If you do not have Python, you will need to install it.

1. Install Python (preferably version 3.9 or later)
2. Download all files from this repository except the README.md file (you can put them into a file for organization, the necessary other files will be created when the program is run
3. Pip install required libraries from requirements.txt, as directed below:

## Pip Installs
You will need to go to the command prompt to install the packages this program uses. Fortunately there is only 1-2. 
1. Download requirements.txt
2. Go to search bar on Windows
3. Search for "cmd"
4. Open "Command Prompt"
5. Type in "pip install -r path\to\requirements.txt"
   
   5.1 If your Python is not installed on your boot drive (C:), you may need to type "path\to\Python.exe -m pip install -r path\to\requirements.txt" or a similar variation instead
6. (optional) If you would like (or if you get an error from my very basic implementation of file naming convention), you can change the path to a specific folder or file name in line 2 of the program file.

# Running the program
You should be able to run the program directly by opening the pw_gui.py file.
The function will automatically run for you when you run the program, but I would recommend running it in a code editor or IDE so you can see the output before the program closes.
When it starts, it will ask if you want the program to create a new password for you, if you want to retrieve an already saved password, or if you want to either bring over an existing password or reset one that the program made for you.
You can type "n" and Enter for a new password, "l" (lowercase L) and Enter to retrieve your saved password for a given website, or "r" to either manually or automatically set a password for an existing password either from a different service or from your previously saved passwords.
If you are ever generating a new password automatically, it will ask you for the length you want the password, as many websites will have a minimum requred password length, and if you want to exclude any types of characters, as some websites may not accept certain types of characters. 

The key for the character types are as follows: 

"l" (lowercase L): Lowercase ascii characters

"u": Uppercase ascii characters

"d": Digits (0-9)

"p": ascii punctuation characters (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~)

You can type any or all of these (though if you type all, your password will be blank) at once with no spaces and it will take those out of possible characters it will make the password from. You can also add a space and then manually enter specific characters that you would like to not have appear in te password.

The program will always ask what website you want to look up data for or save data for. The naming convention will default to SecondLevelDomain.TopLevelDomain (example.com), but it should be able to handle full links. It may struggle with multiple subdomains (www.maps.google.com) since it will try to only save the google.com part, but this should suffice in most cases.

Whenever saving a not-already-existing password into the manager, it will ask for the username you use on that website. **This program only ever saves locally, so none of your data will be stored anywhere except your machine.** Saving the username is only for your convenience later, as it will spit it out to you when you load an existing password in case you forgot your username. 

# Disclaimer
This password manager is meant for personal use only, and while the filetypes are of a non-universal variety and the passwords may be cryptographically randomized, the files are not entirely secure. The files are saved in encrypted bytes arrays, which means they will be fairly unreadable to the human eye, but they can still be interpreted by a computer if they have your private key and symmetric encryption key. Be wary and do not let anyone try and read the private key file as it still may compromise your personal information. This program is only offered as a way to store your passwords offline on your local machine in a convenient way without your data being out on the internet in a database that could be compromised. However, if your machine gets compromised, the data still may be compromised and there is less security in this program than a big corporation would be able to provide.

If you suspect your data may be leaked, it is advised to change your passwords on the websites you have saved, and then you can type "new keys" in the program at the initial step and it will generate new keys and re-encrypt your saved data with the new keys.

This program now is equipped with Symmetric Encryption for your data, using the Fernet method, making it more secure. This symmetric encryption key is encrypted using RSA; however, the private key file with your private key is what is used to decrypt the symmetric key and anyone who has access to this file will be able to decrypt your symmetric key and use that to decrypt your passwords. DO NOT LET ANYONE ACCESS THIS FILE APART FROM YOURSELF AND THIS PROGRAM (and maybe not even yourself unless you really need to transfer your passwords elsewhere).

# Upcoming Updates
Currently working slowly on adding to this program to increase the convenience, accessibility, and features.
The Transfer Data button currently does not do anything as of yet, but there may be an update in the future.

Working on adding:

1. a GUI to make it a full-fledged .exe application (Coming Soon)
2. a way to autofill to other applications like web browsers
