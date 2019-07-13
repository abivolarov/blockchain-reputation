import time
import threading
from EventReport import EventReport
import Logger

class EventListener:
    """
        The class is used to listen for new road events on the blockchain and give a feedback about the credibility of these events.
    """

    def __init__(self):

        self.__submittedFeedback = {}

        self.__submittedEvent = {}

        self.__eventNumber = None

        self.__address = None

        self.__event = None


    def getCredibility(self, prompt):
        """
            The function grabs the user's choice of credibility. It can be only true or false.
        """

        while True:
            try:
                return {"y":True, "n":False}[input(prompt).strip().lower()]
            except KeyError:
                print("Invalid input! Please submit if the message is credible or not.")
            except EOFError:
                Logger.info("Program interrupted here! Going to the main screen now...")
                return


    def getReputation(self, contract, address):
        """
            The function returns the repution of an address
        """
        try:
            reputation = contract.functions.getReputation(address).call()
            Logger.info("Account: " + address + " has " + self.getImplication(reputation))
        except Exception as e:
            Logger.warn("Reputation is not provided")


    def newEvents(self, contract, web3):
        """
            The function listens for new road events on the blockchain. Credibility of the message can be submitted here.
        """

        try:
            while True:

                self.__eventNumber = contract.functions.getNumberOfEvents().call()

                if self.__eventNumber != 0:

                    self.__event = contract.functions.getLatestEventByIndex(self.__eventNumber).call().decode("utf-8").strip()
                    self.__address = str(contract.functions.getTheAddressOfTheLatestEvent(self.__eventNumber).call())

                    if (web3.eth.defaultAccount != self.__address and (self.__eventNumber not in self.__submittedEvent) and (self.__address not in self.__submittedEvent)):

                        Logger.info("Address " + self.__address + " reported event: " + self.__event)

                        self.__submittedEvent[self.__eventNumber] = self.__address

                        reputation = self.getReputation(contract, self.__address)

                time.sleep(2)

        except KeyboardInterrupt:
            Logger.info("Going to the credibility submission...")
            return

    """
        The function listens for changes on the blockchain network
    """
    def listenForEvents(self, contract, web3):
        print("\n")
        Logger.info("Listening for events...")

        thread = threading.Thread(target=self.newEvents(contract, web3))
        thread.daemon = True
        thread.start()

        try:

            if self.__event is not None and self.__address is not None and web3.eth.defaultAccount != self.__address and self.__eventNumber not in self.__submittedFeedback:

                try:
                    Logger.info("Give a feedback for event: " + self.__event + " from address: " + self.__address)
                    isCredible = self.getCredibility("Is the message credible?: (y/n) ")

                except KeyboardInterrupt:
                    Logger.info("Credibility submission was interrupted! Going to the main screen...")
                    return

                try:
                    txHash = contract.functions.submitFeedback(self.__address, isCredible).transact()

                    self.__submittedFeedback[self.__eventNumber] = self.__address

                    web3.eth.waitForTransactionReceipt(txHash)

                    Logger.info("Feedback submitted!")

                    self.getReputation(contract, self.__address)

                except Exception as e:
                    Logger.fatal("Exception occuried: {}".format(e))
            else:
                return

        except KeyboardInterrupt:
            Logger.info("Credibility submission was interrupted! Exiting now...")
            return



    def getImplication(self, score):
        """
            The function returns the meaning of the score numericals
        """

        if(score == 1):
            return "a very dangerous reputation. Do not proceed!"
        elif(score == 2):
            return "a dangerous reputation. "
        elif(score == 3):
            return "a suspicious reputation. Proceed with extreme caution"
        elif(score == 4):
            return "a very good reputation!"
        elif(score == 5):
            return "an excellent reputation!"
        else:
            return "No reputation for this account"
