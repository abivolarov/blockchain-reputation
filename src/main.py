import sys
from os import path
from Constants import HELP_MSG
from Connector import Connector
import Logger

class DecentralizedTrustManagement:
    """
        The main class of the blockchain reputation system
    """

    def __init__(self):

        # Private Key to identify the account
        self.__pKey = None

        # RPC Provider's address in order to connect to the blockchain
        self.__provider = None

        # The Smart Contract ABI's
        self.__ABI = None

        # The Smart Contract address
        self.__contAddr = None

        # Connection to blockchain
        self.__connector = Connector()

    def run(self):
    # After the  Initialization process, this method runs the system.
        if self.__pKey is None:
            Logger.fatal("Without private key you can not be identified in the system!\n")
            print(HELP_MSG)
            return
        if self.__provider is None:
            Logger.fatal("The Web3 provider is not set! - unable to connect to the network\n")
            print(HELP_MSG)
            return
        if self.__ABI is None:
            Logger.fatal("The smart contract's abi path must be provided!\n")
            print(HELP_MSG)
            return
        if self.__contAddr is None:
            Logger.fatal("The smart contract's address must be provided!\n")
            print(HELP_MSG)
            return

        if not path.isfile(self.__ABI):
            Logger.fatal("File path does not exist!\n")
            return

        # Connection to the provider
        self.__connector.connectToWeb3(self.__pKey, self.__provider, self.__ABI, self.__contAddr)


    # Method to set the private key
    def setPrivateKey(self, privateKey):
        self.__pKey = privateKey

    # Method to set the provider
    def setProvider(self, provider):
        self.__provider = provider

    # Method to set the path to the smart contract's abi
    def setAbiPath(self, path):
        self.__ABI = path

    # Method to set the smart contract's address on the blockchain
    def setContractAddress(self, address):
        self.__contAddr = address


if __name__ == "__main__":

    DTM = DecentralizedTrustManagement()
    for i in range(1, len(sys.argv)):
        if sys.argv[i] in ["-pk", "--private-key"]:
            DTM.setPrivateKey(sys.argv[i+1])
        elif sys.argv[i] in ["-rpc", "--rpc-provider"]:
            DTM.setProvider(sys.argv[i+1])
        elif sys.argv[i] in ["-abi", "--abipath"]:
            DTM.setAbiPath(sys.argv[i+1])
        elif sys.argv[i] in ["-ca", "--contract-address"]:
            DTM.setContractAddress(sys.argv[i+1])
        elif sys.argv[i] in ["-h", "--help"]:
            print(HELP_MSG)
            sys.exit()
            break
    DTM.run()
