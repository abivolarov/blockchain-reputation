import sys
import time
from web3 import Web3, exceptions
from Constants import HELP_MSG
from AbiParser import AbiParser
from EventListener import EventListener
from EventReport import EventReport
import Logger


class Connector:
    """
        The class is used to create a connection to the blockchain using the web3.py library
    """

    def __init__(self):

        # The Abi File parser
        self.__abiParser = AbiParser()

        # The Event Listener class instance
        self.__eventListener = EventListener()

        # The Event Report class instance
        self.__eventReport = EventReport()

        # Variable to store the action chosen
        self.__action = None



    def connectToWeb3(self, privateKey, provider, abipath, contAddr):

        """
            This method creates a connection to blockchain using the Web3 library
        """

        w3 = Web3(Web3.HTTPProvider(provider))

        # A bool to check if a connection was made
        checkConnection = w3.isConnected()

        if not checkConnection:
            Logger.fatal("Couldn't connect to the provider")
            print(HELP_MSG)
            return

        # The length of the private key provided by the user
        pkLen = len(privateKey)

        if pkLen != 64:
            Logger.fatal("You have entered an unvalid private key")
            return

        pk = "0x" + privateKey

        account = w3.eth.account.privateKeyToAccount(pk)
        accountAddress = account.address

        # Web3 method to get all accounts on blockchain
        accounts = w3.eth.accounts

        # Check is the account derived from the private key is a legitime address
        if(accountAddress not in accounts):
            Logger.fatal("Your public address is not a valid address on the blockchain")
            return

        # Get the contract's compiled ABI file
        abi = AbiParser().parseAbi(abipath)

        # Check if the contract is valid on the blockchain
        try:
            w3.eth.getCode(contAddr)
        except exceptions.InvalidAddress:
            Logger.fatal("You have entered an invalid smart contract address")
            return

        contractAddress = w3.toChecksumAddress(contAddr)

        # Initialize a contract instance
        contract = w3.eth.contract(address=contractAddress, abi=abi)



        # Set the access account of the blockchain
        print("")
        w3.eth.defaultAccount = accountAddress
        Logger.info("You are now logged in with address: " + w3.eth.defaultAccount)

        # Start the program
        while True:
            try:
                print("")
                self.initializeAction(contract, w3, accountAddress, pk)
                time.sleep(2)
            except KeyboardInterrupt:
                Logger.info("Program interrupted! Exiting...")
                break


    def getAction(self, prompt):
        """
            This method grabs the user's choice
        """

        while True:
            action = input(prompt).strip().lower()
            if action in ('1', '2', '3'):
                return int(action)
            else:
                Logger.info("Invalid choice! Please try again")


    def initializeAction(self, contract, web3, address,privateKey):
        """
            The method initializes the screen
        """
        print("Choose what you would like to do: ")
        print("[1] : Report an event")
        print("[2] : Listen for current events")
        print("[3] : Exit")

        try:
            self.__action = self.getAction("Choose an action: ")
        except EOFError:
            Logger.info("Program interrupted here! Exiting...")
            sys.exit()

        if self.__action == 1:
            self.__eventReport.reportEvent(contract, web3, address, privateKey)
        elif self.__action == 2:
            self.__eventListener.listenForEvents(contract, web3)
        elif self.__action == 3:
            Logger.info("Exiting...")
            sys.exit()
