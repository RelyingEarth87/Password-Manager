import sys
from os import path, mkdir, getcwd, remove
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit
from PyQt6.QtGui import QIcon
from pw_manager import *
from PyQt6 import uic
import configparser

# Making the default directory for our extra files
curr_directory = getcwd()
path_ = path.join(curr_directory, "config")
if not path.exists(path_):
    mkdir(path_)

# Making the settings file to save user settings
settings_location: str = './config/settings.ini'
if not path.isfile(settings_location):
    config = configparser.ConfigParser()
    config['Section 1'] = {"Mode": "light"}
    configfile = open(settings_location, 'w')
    config.write(configfile)
    configfile.close()

class PINChanger(QDialog):
    """The dialog box to set or reset a PIN to access the application

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        # Initializing the class and the pre-made UI 
        super().__init__()
        uic.loadUi('./ui/pinCreate.ui', self)

        # Hiding the message received if the fields do not match and hiding the password text from prying eyes
        self.errorMsg.hide()
        self.pinEdit1.setEchoMode(QLineEdit.EchoMode.Password)
        self.pinEdit2.setEchoMode(QLineEdit.EchoMode.Password)

        # connecting button functionality
        self.buttonBox.accepted.connect(self.submit)
        self.buttonBox.rejected.connect(self.cancel)

        self.changed = False

    def submit(self):
        """A function to submit the data
        """
        if self.pinEdit1.text() == self.pinEdit2.text():
            self.pin = self.pinEdit1
            self.changed = True
            self.close()
        else:
            self.errorMsg.show()
    
    def cancel(self):
        """A function to cancel the operation and close the dialog box
        """
        self.changed = False
        self.close()

class PINChecker(QDialog):
    """Function to check the provided PIN against the saved PIN

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self, file_name: str):
        """Initializes the object and adds the functionality

        Args:
            file_name (str): the path to the file where the PIN is stored
        """
        super().__init__()
        uic.loadUi('./ui/pinCheck.ui', self)
        self.filename: str = file_name
        self.pinValid: str = 'incorrect'

        self.pinEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.buttonBox.accepted.connect(self.submit)
        self.buttonBox.rejected.connect(self.cancel)

    def submit(self):
        """A function to check the data and submit back to main window
        """
        import pickle

        # Getting the encrypted PIN and decrypting it
        file = open(self.filename, 'rb')
        encrypted_pin = pickle.load(file)
        file.close()
        pin = decryption(encrypted_pin)

        # Resaving the encrypted version of the PIN
        file = open(self.filename, 'wb')
        pickle.dump(encrypted_pin, file)
        file.close()

        # checking if the pin is valid and closing the dialog
        if self.pinEdit.text() == pin:
            self.pinValid = 'correct'
            self.close()
        else:
            self.pinValid = 'incorrect'
            self.close()

    def cancel(self):
        """A function to cancel the check and close the dialog
        """
        self.pinValid = 'incorrect'
        self.close()

class KeysChanged(QDialog):
    """Dialog box to show that encryption keys have been changed

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/keys_changed.ui', self)

        self.buttonBox.accepted.connect(self.accept)
    
    def accept(self):
        self.close()

class DelPin(QDialog):
    """Dialog box to make sure that user is sure they want to delete the PIN protection

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        """Initializes the window and adds the button functionality
        """
        super().__init__()
        uic.loadUi('./ui/del_pin.ui', self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancelation)

        self.confirmed = False
    
    def accept(self):
        """If user accepts the deletion of the PIN, sends main window the signal to delete before closing
        """
        self.confirmed = True
        self.close()

    def cancelation(self):
        """If user cancels the deletion of the PIN, sends main window signal to do nothing before closing
        """
        self.confirmed = False
        self.close()

class DelDialog(QDialog):
    """Dialog box to get the sitename to be deleted

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        """Initializes the window and adds the button functionality
        """
        super().__init__()
        uic.loadUi('./ui/deletion.ui', self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancelation)
            
    
    def accept(self):
        """When accept button is clicked, opens confirmation dialog and saves sitename before closing 
        """
        # open confirmation dialog
        confirm = DelConfirm()
        confirm.exec()

        # checks if user confirmed deletion or canceled and saves sitename
        if confirm.accepted == True:
            self.sitename: str = self.site.text()
        else:
            self.sitename = -1
        self.close()

    def cancelation(self):
        """Allows for the cancelation of the process and closes the dialog box
        """
        self.sitename = -1
        self.close()

class DelConfirm(QDialog):
    """Dialog box to make sure that user is sure they want to delete the data

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        """Initializing the window and adding the button functionality
        """
        super().__init__()
        uic.loadUi('./ui/confirmDeletion.ui', self)

        self.confirmation.accepted.connect(self.accept)
        self.confirmation.rejected.connect(self.cancelation)
        self.accepted = False
    
    def accept(self):
        """When user clicks to confirm, sets accepted trait before closing
        """
        self.accepted = True
        self.close()
    def cancelation(self):
        """When user clicks to cancel, sets accepted trait before closing
        """
        self.accepted = False
        self.close()

class DeleteSuccess(QDialog):
    """Dialog box to confirm site data has been deleted successfully

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('./ui/deletesuccess.ui', self)

        self.buttonBox.accepted.connect(self.accepted)
    
    def accepted(self):
        """A function that closes the dialog when user clicks on Ok button
        """
        self.close()

class NewPass(QDialog):
    """Dialog box to get information to make a new password with the generator

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('./ui/newPass.ui', self)

        self.buttonBox.accepted.connect(self.submit)
        self.buttonBox.rejected.connect(self.cancel)
        self.submitted = False

    def submit(self):
        """A function that saves the information to generate the new password when user clicks submit
        """
        confirmation = NewPassConfirm()
        confirmation.exec()

        # making sure the user confirmed and did not cancel or x out the other window
        if confirmation.confirmed:
            self.submitted = True

            # getting the values from the inputs and putting them in the right form
            self.length = self.numChars.value()

            self.disallowed = []
            if self.lowercase.isChecked():
                self.disallowed.append('l')
            if self.uppercase.isChecked():
                self.disallowed.append('u')
            if self.integers.isChecked():
                self.disallowed.append('d')
            if self.punctuation.isChecked():
                self.disallowed.append('p')
            self.otherExclusions = self.others.text()
            self.otherExclusions.replace(' ', '')

            self.exclusions = ''
            for i in self.disallowed:
                self.exclusions += i
            if self.otherExclusions != '':
                self.exclusions += ' ' + self.otherExclusions
            
            self.site_name = self.sitename.text()
            self.username = self.user_name.text()
            self.close()
        else:
            self.submitted = False
            self.close()

    def cancel(self):
        """A function to close the window when the user clicks Cancel
        """
        self.submitted = False
        self.close()

class NewPassConfirm(QDialog):
    """The dialog box to have the user confirm their information is correct

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/saveConfirm.ui', self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancel)
        self.confirmed = False
    
    def accept(self):
        """A function to confirm the information on Submit
        """
        self.confirmed = True
        self.close()
    
    def cancel(self):
        """A function to cancel the submission on Cancel"""
        self.confirmed = False
        self.close()

class SaveSuccess(QDialog):
    """The dialog box to show the user their new data has been saved

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/saveSuccess.ui', self)

        self.buttonBox.accepted.connect(self.ok)
    
    def ok(self):
        """A function to close the dialog box on OK
        """
        self.close()

class LoadDialog(QDialog):
    """The dialog box to get the information the user would like to load

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/loadDialog.ui', self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancel)

        self.sitename = -1
    
    def accept(self):
        """A function to get the name of the site/application on Submit
        """
        self.sitename = self.site_name.text()
        self.close()
    
    def cancel(self):
        """A function to return a failure and cancel the operation
        """
        self.sitename = -1
        self.close()

class LoadedPassDialog(QDialog):
    """The dialog box to show the loaded data that the user has requested

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self, site, user, pw):
        super().__init__()
        uic.loadUi('./ui/loadedPassDialog.ui', self)

        # setting the passed arguments for use
        self.site = site
        self.user = user
        self.pw = pw

        # fixing the boxes so the data can't be changed or the passwords seen on screen at first
        self.echo_mode = 'Password'
        self.pass_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_box.setReadOnly(True)
        self.user_box.setReadOnly(True)

        # setting the text in the label and boxes
        self.data_label.setText(f"Data for {site}:")
        self.user_box.setText(self.user)
        self.pass_box.setText(self.pw)

        # connecting all the buttons to their functions
        self.buttonBox.accepted.connect(self.ok)
        self.copyUser.clicked.connect(self.copy_user)
        self.copyPw.clicked.connect(self.copy_pass)
        self.showHide.clicked.connect(self.show_hide)
    
    def ok(self):
        """Closing the dialog when the user is done"""
        self.close()
    
    def copy_user(self):
        """Allows user to copy from username box"""
        import pyperclip
        pyperclip.copy(self.user)
    
    def copy_pass(self):
        """Allows user to copy from password box"""
        import pyperclip
        pyperclip.copy(self.pw)
    
    def show_hide(self):
        """Allows user to show or hide the password on the screen"""
        if self.echo_mode == 'Password':
            self.pass_box.setEchoMode(QLineEdit.EchoMode.Normal)
            self.echo_mode = 'Normal'

        elif self.echo_mode == 'Normal':
            self.pass_box.setEchoMode(QLineEdit.EchoMode.Password)
            self.echo_mode = 'Password'

class PassError(QDialog):
    """The dialog box to show if the data is not found for a requested site/app

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/passError.ui', self)

        self.buttonBox.accepted.connect(self.ok)
    
    def ok(self):
        """Closes the dialog when user is ready"""
        self.close()

class SetDialog(QDialog):
    """The dialog box to ask how a user would like to set their password when they select "Set/Reset"

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/setDialog.ui', self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancel)

        # Variable to show which method the user selects for password generation
        self.method = None
    
    def accept(self):
        """On submit, sets the password generation method and then closes the dialog"""
        if self.manual.isChecked():
            self.method = 'manual'
        elif self.auto_2.isChecked():
            self.method = 'auto'

        self.close()
    
    def cancel(self):
        """Closes the dialog on Cancel"""
        self.close()

class ManualDialog(QDialog):
    """The dialog box to allow user to manually enter data when setting/resetting password

    Args:
        QDialog (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/manualDialog.ui', self)

        # hiding error message for if/when needed
        self.error_msg.hide()

        # hiding password data from screen
        self.pw_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_box.setEchoMode(QLineEdit.EchoMode.Password)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancel)
    
    def accept(self):
        """On submit, checks to see if passwords match and then sets the data fields for use in meta window"""
        if self.pw_box.text() == self.confirm_box.text():
            self.sitename = self.site_name.text()
            self.username = self.user_box.text()
            self.password = self.pw_box.text()
            self.close()
        else:
            # shows error message if passwords do not match
            self.error_msg.show()
    
    def cancel(self):
        """Cancels and closes window"""
        self.close()

class Pwm(QMainWindow):
    """The main application window that interfaces with the user and handles the data

    Args:
        QMainWindow (type): The meta class from the PyQt library that instantiates a dialog box object
    """
    def __init__(self):
        # Initializing the window
        super().__init__()
        uic.loadUi('./ui/mainWindow.ui', self)
        self.setWindowIcon(QIcon('pwm.ico'))

        # Initializing the file structure
        self.filename = filename
        self.public = public
        self.private = private
        self.pin_location = '.\config\pin.pickle'
        initializer()

        # If user has added PIN protection, asks for PIN before opeing main window
        if path.isfile(self.pin_location):
            self.checkPin()
            if self.pinValid == 'incorrect':
                sys.exit()

        # Adding the functionality for the menu bar items
        self.actionPinChange.triggered.connect(self.changePin)
        self.actionDelete_PIN.triggered.connect(self.deletePin)
        self.actionDarkMode.triggered.connect(self.changeMode)
        self.actionChangeKeys.triggered.connect(self.changeKeys)

        # Adding the functionality for the buttons
        self.newPassword.clicked.connect(self.new_pass)
        self.loadPassword.clicked.connect(self.load_pass)
        self.setPassword.clicked.connect(self.set_pass)
        self.deletePassword.clicked.connect(self.delete_pass)

    def changePin(self):
        """Functionality to add or change the encrypted PIN
        """
        import pickle

        # opening pin change dialog box
        pin_dialog = PINChanger()
        pin_dialog.exec()

        # if the pin was set, making and/or updating the PIN file with the new PIN
        if pin_dialog.changed:
            pin = pin_dialog.pin.text()
            encrypted_pin = encryption(pin)
            if not path.isfile(self.pin_location):
                file = open(self.pin_location, 'x')
                file.close()
            file = open(self.pin_location, 'wb')
            pickle.dump(encrypted_pin, file)
    
    def deletePin(self):
        """Functionality to delete the encrypted PIN
        """
        # making sure PIN exists
        if path.isfile(self.pin_location):
            # running confirmation dialog
            confirmation = DelPin()
            confirmation.exec()

            # if deletion is confirmed, deleting PIN
            if confirmation.confirmed == True:
                remove(self.pin_location)

    def changeMode(self):
        """Functionality to change between dark and light mode
        """
        # initializing and getting the current mode setting
        modes = ['light', 'dark']
        config = configparser.ConfigParser()
        config.read(settings_location)
        curr_mode = config['Section 1']['Mode']

        # changing the mode to the opposite of the current and saving it in settings
        new_mode = (modes.index(curr_mode) + 1) % 2
        config['Section 1']['Mode'] = modes[new_mode]
        configfile = open(settings_location, 'w')
        config.write(configfile)
    
    def changeKeys(self):
        """Functionality to change the encryption keys in case data is compromised
        """
        import pickle

        # getting PIN information from file and unencrypting it
        pin_loc = open(self.pin_location, 'rb')
        encrypted_pin: bytes = pickle.load(pin_loc)
        pin_loc.close()
        curr_pin: str = decryption(encrypted_pin)

        # changing encryption keys and re-encrypting the password data
        newKeys()

        # re-encrypting PIN information with new encryption keys
        new_pin = encryption(curr_pin)
        pin_loc = open(self.pin_location, 'wb')
        pickle.dump(new_pin, pin_loc)

        # showing dialog that tells user everything has been sucessfully changed
        changed = KeysChanged()
        changed.exec()

    def checkPin(self):
        """If PIN exists, checking the user submitted PIN against the one on file to authorize/deny app access
        """
        # opening checker dialog box
        checker = PINChecker(self.pin_location)
        checker.exec()

        # checking dialog box attribute to see if pin is valid
        self.pinValid = checker.pinValid

    def new_pass(self):
        """Saves username and password data after generating a new password
        """
        # instantiates and runs dialog to get data to make password and save data
        newpass_dialog = NewPass()
        newpass_dialog.exec()

        if newpass_dialog.submitted == True:
            # creates password based on length and exclusions provided
            length = newpass_dialog.length
            exclusions = newpass_dialog.exclusions
            password = new_pass(length, exclusions)

            # saves and encrypts password
            site = newpass_dialog.site_name
            user = newpass_dialog.username
            save_pass(site, user, password)

            # instantiates and runs dialog to show password has been saved successfully
            saved_pass = SaveSuccess()
            saved_pass.exec()

            # opens the loaded pasword dialog so the user can access their new password immediately
            pass_dialog = LoadedPassDialog(site, user, password)
            pass_dialog.exec()

    def load_pass(self):
        """Loads previously saved user data
        """
        # instantiates dialog to get site/app name
        load_dialog = LoadDialog()
        load_dialog.exec()

        site  = load_dialog.sitename

        # checks to make sure user entered data
        if type(site) == str:
            # checks user PIN again to helps stop data leaks
            self.checkPin()
            if self.pinValid == 'correct':
                try:
                    # retrieving user data and showing it
                    site, user, pw = get_pass(site)
                    pass_dialog = LoadedPassDialog(site, user, pw)
                    pass_dialog.exec()
                except KeyError:
                    # if no data was found, showing that to user
                    error_dialog = PassError()
                    error_dialog.exec()

    def set_pass(self):
        """Setting or resetting user data either manually or automatically
        """
        # instantiates dialog to ask for manual or auto-generation
        set_dialog = SetDialog()
        set_dialog.exec()

        if set_dialog.method == 'auto':
            # if auto generation is selected, using pre-made new_pass function to set user data
            self.new_pass()
        elif set_dialog.method == 'manual':
            # Instantiating manual data entry dialog
            manual_dialog = ManualDialog()
            manual_dialog.exec()

            try:
                # getting user input from dialog and saving password
                site = manual_dialog.sitename
                user = manual_dialog.username
                password = manual_dialog.password
                save_pass(site, user, password)

                # instantiates and runs dialog to show data has been saved successfully
                saved_pass = SaveSuccess()
                saved_pass.exec()
            except AttributeError:
                # doing nothing if no data was entered
                pass
        else:
            # if user did not select a method to enter data, doing nothing
            pass

    def delete_pass(self):
        """Allows user to select data to delete from the database
        """
        # opens the dialog to enter information about deleting password
        deletion = DelDialog()
        deletion.exec()

        # stores either the name of the website or a -1 if no name is found
        site = deletion.sitename

        # if a site name was entered, executing the deletion
        if type(site) == str:
            try:
                delete_pass(site)

                # telling the user the deletion was successful
                delete_success = DeleteSuccess()
                delete_success.exec()
            except KeyError:
                error = PassError()
                error.exec()

def main():
    """Main entry point that starts the application when the file is the main file running
    """
    # Instantiates the QApplication object
    app = QApplication([])

    # determines which stylesheet to use based on the current setting
    config = configparser.ConfigParser()
    config.read(settings_location)
    print(config.sections())
    curr_mode = config['Section 1']['Mode']
    
    #sets the stylesheet to dark mode if dark moe is selected
    if curr_mode == 'dark':
        sheet = open("./ui/dark_sheet.stylesheet", 'r')
        app.setStyleSheet(sheet.read())

    # Makes an instance of the Password Manager GUI
    window = Pwm()

    # Shows the GUI to the screen
    window.show()

    # Allows the user to close and minimize/maximize the window
    sys.exit(app.exec())


if __name__ == '__main__':
    main()