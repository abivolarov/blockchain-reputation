import Logger


class EventReport:
    """
        The class is used to report a new road event and publish it on the blockchain
    """

    def getAction(self, prompt):
        """
            Ensures that the user is chosen event 1, 2 or 3
        """
        while True:
            action = input(prompt).strip().lower()
            if action in ('1', '2', '3'):
                return int(action)
            else:
                print("Invalid choice! Please try again")


    def reportEvent(self, contract, web3, address, privateKey):
        """
            Used to save the chosen event on the blockchain. Here the transaction is signed with the private key
        """

        print("")
        print("Choose an event to report: ")
        print("[1] : Traffic Congestion")
        print("[2] : Emergency")
        print("[3] : Road closed")

        action = self.getAction("Choose an action: ")

        try:

            # Building the transaction first
            txHash = contract.functions.submitRoadEvent(action).buildTransaction({
                'nonce':web3.eth.getTransactionCount(address)
            })

            # Then signing the transaction
            signed_txn = web3.eth.account.signTransaction(txHash, privateKey)

            # And sending it to the blockchain
            web3.eth.sendRawTransaction(signed_txn.rawTransaction)

            # Checking the latest event on the blockchain
            numberOfEvent = int(contract.functions.getNumberOfEvents().call())
            latestEvent = contract.functions.getLatestEventByIndex(numberOfEvent).call()
            accountAddressEvent = contract.functions.getTheAddressOfTheLatestEvent(numberOfEvent).call()

            Logger.info("Your road event report was successfully saved on the blockchain!")
            Logger.info("Number: {}, your address: {}, type: {}".format(numberOfEvent, accountAddressEvent, latestEvent.decode("utf-8")))

        except Exception as e:
            Logger.fatal("Something went wrong: {}".format(e))

        Logger.info("Now going back to the start screen")
