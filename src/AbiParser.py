import fnmatch
import Logger

class AbiParser:
    """
        The class is used to parse the smart contract's ABI from a path.
    """

    # Method to parse the abi file into the program
    def parseAbi(self, path):
        abi = ''
        if self.__check_abi(path):
            with open(path, 'r') as file:
                abi += file.read()
                file.close()
            return abi
        else:
            Logger.fatal("Not an ABI file! Exiting the program...")
            return

    # Method to check the Abi
    def __check_abi(self, path, extension="*.abi"):
        if fnmatch.fnmatch(path, extension):
            return True
        return False
