# Password Manager
A simple password creator and manager made from Python

This file, with its one requirement, will generate cryptographically secure passwords and save them on your system as a bytes array.

You can save passwords, set your existing passwords from other password managers, and load the passwords you have saved. 

Other than writing your own passwords into the password setter function, your passwords will never appear on the screen and will be copied directly into your clipboard for easy use and security.

# Setup
At this time, running this program requires a Python installation. It was written on Python 3.9, but as long as your Python version supports Pickle natively, you will only need to pip install one thing.
If you do not have Python, you will need to install it.

1. Install Python (preferably version 3.9 or later)
2. Download the pw_manager.py file from this repository
3. Pip install pyperclip, RSA (and possibly pickle) packages, as directed below:

## Pip Installs
You will need to go to the command prompt to install the packages this program uses. Fortunately there is only 1-2. 
1. Go to search bar on Windows
2. Search for "cmd"
3. Open Command Prompt
4. Type "pip install pyperclip", hit Enter
   4.1 If your Python is not installed on your boot drive (C:), you may need to type "path\to\Python.exe -m pip install pyperclip" instead
5. Type "pip install rsa", hit Enter
6. If you have Python version 3.9 or later, you are done and can run the program
   6.1 If you have an earlier version of Python, you will also need to type "pip install pickle"
7. (optional) If you would like (or if you get an error from my very basic implementation of file naming convention), you can change the path to a specific folder or file name in line 2 of the program file.

# Running the program
The function will automatically run for you when you run the program, but I would recommend running it in a code editor or IDE so you can see the output before the program closes.
When it starts, it will ask if you want the program to create a new password for you, if you want to retrieve an already saved password, or if you want to either bring over an existing password or reset one that the program made for you.
You can type "n" and Enter for a new password, "l" (lowercase L) and Enter to retrieve your saved password for a given website, or "r" to either manually or automatically set a password for an existing password either from a different service or from your previously saved passwords.
If you are ever generating a new password automatically, it will ask you for the length you want the password, as many websites will have a minimum requred password length, and if you want to exclude any types of characters, as some websites may not accept certain types of characters. 

The key for the character types are as follows: 

"l" (lowercase L): Lowercase ascii characters

"u": Uppercase ascii characters

"d": Digits (0-9)

"p": ascii punctuation characters (!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~)

You can type any or all of these (though if you type all, your password will be blank) at once with no spaces and it will take those out of possible characters it will make the password from.

The program will always ask what website you want to look up data for or save data for. The naming convention will default to SecondLevelDomain.TopLevelDomain (example.com), but it should be able to handle full links. It may struggle with multiple subdomains (www.maps.google.com) since it will try to only save the google.com part, but this should suffice in most cases.

Whenever saving a not-already-existing password into the manager, it will ask for the username you use on that website. **This program only ever saves locally, so none of your data will be stored anywhere except your machine.** Saving the username is only for your convenience later, as it will spit it out to you when you load an existing password in case you forgot your username. 

# Disclaimer
This password manager is meant for personal use only, and while the filetypes are of a non-universal variety and the passwords may be cryptographically randomized, the files are not entirely secure. The files are saved in bytes arrays, which means they will be fairly unreadable to the human eye, but they can still be interpreted by a computer. Be wary and do not let anyone try and read the public key file as it still may compromise your personal information. This program is only offered as a way to store your passwords offline on your local machine in a convenient way without your data being out on the internet in a database that could be compromised. However, if your machine gets compromised, the data still may be compromised and there is less security in this program than a big corporation would be able to provide.

This programm now is equipped with RSA Encryption for your data, making it more secure; however, the private key file with your private key is what is used to decrypt the information and anyone who has access to this file will be able to decrypt your passwords. DO NOT LET ANYONE ACCESS THIS FILE APART FROM YOURSELF AND THIS PROGRAM (and maybe not even yourself unless you really need to transfer your passwords elsewhere).

# Upcoming Updates
Currently working slowly on adding to this program to increase the convenience, accessibility, and features.

Working on adding:

1. a GUI to make it a full-fledged .exe application
2. a way to autofill to other applications like web browsers
