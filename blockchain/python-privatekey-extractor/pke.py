import sys
import binascii
import getpass
from web3.auto import w3
from Constants import HELP_MSG

class PrivateKeyExtractor:
    """ The program extracts the private key from a geth keystore file """

    def __init__(self):
        self.__path = None

    def retrievePrivateKey(self):

        if self.__path is None:
            print("NO PATH PROVIDED\n")
            print(HELP_MSG)
            return


        try:
            password = getpass.getpass("Enter the password of the keystore file: ")

            with open(self.__path) as file:
                encryptedKey = file.read()
                privateKey =  w3.eth.account.decrypt(encryptedKey, password)

            pk = str(binascii.b2a_hex(privateKey))

            private_key = pk.partition("b'")[2].partition("'")[0]

            print("Your private key is: " + private_key)

        except ValueError:
            print("This password is wrong! Exiting")


    def setPath(self, path):
        self.__path = path

if __name__ == "__main__":

    PKE = PrivateKeyExtractor()
    for i in range(1, len(sys.argv)):
        if sys.argv[i] in ["-p"]:
            PKE.setPath(sys.argv[i+1])
        elif sys.argv[i] in ["-h", "--help"]:
            print(HELP_MSG)
            sys.exit()
            break
    PKE.retrievePrivateKey()
