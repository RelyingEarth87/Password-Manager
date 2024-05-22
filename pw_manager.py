from typing import Tuple
import pickle
import rsa

# initializing file names
filename = '.\pwman\passwords.pickle'
public = '.\pwman\public.pem'
private = '.\pwman\private.pem'

def repickle(data: dict) -> None:
    """Resaves the data after unpickling

    Args:
        data (dict): the dictionary containing all the data to repickle
    """
    encrypted_data = encryption(data)

    file = open(filename, 'wb')

    pickle.dump(encrypted_data, file)

def new_pass(length=12, exclusions=None) -> str:
    """Takes in a minimum length and an exclusions parameter that specifies
    anything not accepted by the website and returns a cryptographically
    secure password string

    Args:
        length (int, optional): The required length of the password. Defaults to 12 characters long.
        exclusions (str, optional): Specifies any type of character not accepted in the password. Defaults to None.

    Returns:
        str: A cryptographically secure password string
    """
    import secrets
    import string
    
    # getting the available characters
    lower: str = string.ascii_lowercase
    upper: str = string.ascii_uppercase
    digits: str = string.digits
    punc: str = string.punctuation

    # making a dump for characters that will be chosen from 
    using: str = ''

    # dumping the data that we don't want to exclude into the dump string
    if exclusions is not None:
        if "l" not in exclusions:
            using += lower
        if "u" not in exclusions:
            using += upper
        if "d" not in exclusions:
            using += digits
        if "p" not in exclusions:
            using += punc
    elif exclusions is None:
        using += lower
        using += upper
        using += digits
        using += punc
    
    # generating the cryptographically secure password string
    password: str = ''.join(secrets.choice(using) for i in range(length))

    return password

def save_pass(site: str, username: str, password: str) -> None:
    """A function that saves the username and generated password to the pickle file's dictionary with the key as the site name

    Args:
        site (str): The name of the website the user data belongs to
        username (str): The entered username for the specified website
        password (str): The programmatically generated  and cryptographically secure password
    """

    # opening the file to gather the old passwords
    file = open(filename, 'rb')

    # creating the key for the dictionary with the top level domain of the website name
    site_split = site.split('.')
    if len(site_split) == 3:
        site_name = site_split[1]
    elif len(site_split) == 2:
        site_name = site_split[0]
    elif len(site_split) >= 4:
        site_name = site_split[2]
    else:
        site_name = site
        site = site + ".com"

    # loading the pickled dictionary from the file and appending the new user data to it
    try:
        data = pickle.load(file)
        passwords = decryption(data)
    except EOFError:
        passwords = {}

    passwords[site_name] = {"site": site, "username": username, "password": password}

    file.close()
    repickle(passwords)

    print("Your password has been saved!")

def get_pass(site: str) -> Tuple[str, str, str]:
    """Getter to retrieve user data for a given website

    Args:
        site (str): The name of the website thats data we want to retrieve

    Returns:
        Tuple[str, str, str]: The website name, username, and password for the given website
    """

    # opening the file and retrieving the dictionary with all the information
    file = open(filename, 'rb')
    data = pickle.load(file)
    passwords = decryption(data)
    repickle(passwords)

    # standardizing the website name to prepare for search
    site_split = site.split('.')
    if len(site_split) == 3:
        site_name = site_split[1]
    elif len(site_split) == 2:
        site_name = site_split[0]
    elif len(site_split) >= 4:
        site_name = site_split[2]
    else:
        site_name = site
    
    # creating a new variable for the data from the specified website
    site_data = passwords[site_name]

    # parsing the data from the dictionary into the specific parts to return
    site = site_data["site"]
    username = site_data["username"]
    password = site_data["password"]

    file.close()
    return site, username, password

def reset_pass(site: str, username: str) -> None:
    """Adds functionality to set an already existing password from a different manager or reset a password in this one

    Args:
        site (str): The name of the website thats data we will be changing
        username (str): The provided username to be stored with the site data
    """

    # asking if the user would like to set a password or reset an existing password and then gathering the password accordingly
    manual_auto: str = input("Would you like to manually set the password or have it auto-generated? (m/a) ")
    if manual_auto == "m":
        password: str = input("What would you like to set the password to? ")
    elif manual_auto == "a":
        length: int = int(input("What is the required length of the password? "))
        exclusions: str = input("Are there any types of characters you would like to exclude? ")
        password: str = new_pass(length, exclusions)
    
    # saving the password to the database
    save_pass(site, username, password)

    print("Your password has been set successfully")

def check_sites(site) -> Tuple[str, str]:
    """Checks to see if a saved password and username exists for the given website

    Args:
        site (str): The user-given name of the website

    Returns:
        Tuple[str, str]: Outpusts either a 1 if data exists and a username, or a -1 if data does not exist
    """

    # opening the file and importing the pickled data
    file = open(filename, 'rb')
    try:
        data = pickle.load(file)
        passwords = decryption(data)
    except EOFError:
        passwords = {}
    
    file.close()

    # Resaving the encrypted data
    repickle(passwords)

    # extracting the website names from the dictionary
    sites = dict.fromkeys(passwords)

    # standardizing the website name to prepare for search
    site_split = site.split('.')
    if len(site_split) == 3:
        site_name = site_split[1]
    elif len(site_split) == 2:
        site_name = site_split[0]
    elif len(site_split) >= 4:
        site_name = site_split[2]
    else:
        site_name = site

    # searching for the site data and outputting
    if site_name in sites:
        site_data = passwords[site_name]
        site = site_data["site"]
        user = site_data["username"]
        password = site_data["password"]
        return 1, user
    else:
        print("Website data not found")
        return -1, None

def generate_keys(bytes: int) -> None:
    """Generates public and private keys for asymmetric encryption and saves to respective files.

    Args:
        bytes (int): the memory allocation, in bytes, for the generation of the keys
    """

    # generating keys using RSA library
    public_key, private_key = rsa.newkeys(bytes)

    #saving files
    with open(public, 'wb') as f:
        f.write(public_key.save_pkcs1("PEM"))
    
    with open(private, 'wb') as f:
        f.write(private_key.save_pkcs1("PEM"))

def encryption(message: str) -> str:
    """Gets the public key and uses it to encrypt the data for secure storage

    Args:
        message (str): the data to be encrypted

    Returns:
        str: the encrypted data in a bytes array format
    """
    import json
    with open(public, 'rb') as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    
    message_bytes: bytes = json.dumps(message).encode('utf-8')
    encrypted: str = rsa.encrypt(message_bytes, public_key)

    return encrypted

def decryption(message: str) -> str:
    """Gets the private key and uses it to decrypt the data for use

    Args:
        message (str): The encrypted data to be decrypted

    Returns:
        str: An unencrypted string containing the secured data
    """
    import json
    with open(private, 'rb') as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    
    unencrypted_bytes: bytes = rsa.decrypt(message, private_key)
    unencrypted = json.loads(unencrypted_bytes.decode('utf-8'))

    return unencrypted

def initializer() -> None:
    """Initializes the file paths and creates the files and keys"""
    from os import path, mkdir, getcwd
    curr_directory = getcwd()
    path_ = path.join(curr_directory, "pwman")
    if not path.exists(path_):
        mkdir(path_)
    # Creating a file if it doesn't exist
    if not path.isfile(filename):
        file = open(filename, 'x')
        file.close()

    if not path.isfile(public) or not path.isfile(private):
        generate_keys(1024)

def main():
    import pyperclip

    print("""Welcome to Password Manager, to proceed, you can type n to create a new password, l to load a 
        previously saved password, or r to either set a password manually or reset an existing password.""")
    
    # making sure our files are initialized
    initializer()
    
    new_load: str = input("What would you like to do? (nlr) ")

    # if user selects to get a new password, saving it to database and copying it to clipboard
    if new_load == "n":
        print("Ready to generate new password")
        length: int = int(input("What length is needed? "))
        exclusions: str = input("Anything not allowed? ")
        pw = new_pass(length, exclusions)
        site: str = input("What website is this for? ")
        user: str = input("What username did you use for this site? ")
        save_pass(site, user, pw)

        pyperclip.copy(pw)
        print("Password copied to clipboard")

    # if user selects to load a password, printing username and copying password to clipboard
    elif new_load == "l":
        print("Ready to load existing password")
        site = input("What website? ")
        site, user, pw = get_pass(site)
        
        #resaving password because pickle will delete it otherwise
        save_pass(site, user, pw)

        print(user)
        pyperclip.copy(pw)
        print("Password copied to clipboard")

    # if user selects to set/reset a password, getting data from user, setting password in database
    elif new_load == "r":
        print("Ready to set existing password")
        site = input("What website? ")
        exists, user = check_sites(site)
        if exists == -1:
            user = input("What username did you use for this site? ")
        reset_pass(site, user)

if __name__ == "__main__":
    main()
