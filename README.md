# Blockchain reputation management system


## Abstract

The system was designed to show trust management by reputation using distributed ledger technologies. The
system was implemented for an Ethereum PoA network. It was written in Python 3.7.3 and Solidity 0.5.11. The project 
was tested with Python 3.7.3

## Specification

Prerequisites:
In order to work with this project there are several dependencies:

```
    npm           https://nodejs.org/en/download/
    geth          https://geth.ethereum.org/downloads/
    truffle       npm install -g truffle
    solcjs        npm install -g solc
    web3.py       pip install web3
```

### Creating the Ethereum PoA Network

After installing the prerequisites we need to create the first accounts in networtk in order to itilialize 
a blockchain network:

	1. Create a folder with the name * *vanet* *

	2. Create a folder inside the * *vanet* * folder a new folder with name * *account* *

	3. Run the following command in the * *vanet* * folder:

```
  geth --datadir account/ account new 
```

After entering a prefered password the new account address should be printed on the screen. Then we need to
create a new Ethereum network. For this purpose we are going to use the **puppeth** tool from Ethereum to 
create the genesis file, which is the first block in blockchain network. In a console just type:

``` 
	puppeth

```

Then we are going to follow the steps:

```
	
	Please specify a network name to administer (no spaces, hyphens or capital letters please)
	> vanet

	Sweet, you can set this via --network=vanet next time!

	What would you like to do? (default = stats)
	 1. Show network stats
	 2. Configure new genesis
	 3. Track new remote server
	 4. Deploy network components
	> 2

	What would you like to do? (default = create)
	 1. Create new genesis from scratch
	 2. Import already existing genesis
	> 1

	Which consensus engine to use? (default = clique)
	 1. Ethash - proof-of-work
	 2. Clique - proof-of-authority
	> 2

	How many seconds should blocks take? (default = 15)
	> 5

	Which accounts are allowed to seal? (mandatory at least one) -- Here we add the address of the account
	which we already created
	> 0x2807ea8cebe149ef2489937d9a711045bbc3ba4b
	> 0x

	Which accounts should be pre-funded? (advisable at least one)
	> 0x2807ea8cebe149ef2489937d9a711045bbc3ba4b
	> 0x

	Should the precompile-addresses (0x1 .. 0xff) be pre-funded with 1 wei? (advisable yes)
	> yes

	Specify your chain/network ID if you want an explicit one (default = random)
	> 5775
	INFO[07-10|17:15:55.053] Configured new genesis block

	What would you like to do? (default = stats)
	 1. Show network stats
	 2. Manage existing genesis
	 3. Track new remote server
	 4. Deploy network components
	> 2

	 1. Modify existing fork rules
	 2. Export genesis configurations
	 3. Remove genesis configuration
	> 2

	Which folder to save the genesis specs into? (default = current)
	  Will create vanet.json, vanet-aleth.json, vanet-harmony.json, vanet-parity.jso
	n
	>

```

If we need another predefined accounts we must specify them here. Note: accounts that are here specified would be chosen
to be the sealers of the blocks mined in the network

Now we must initialize the account with the newly created **vanet.json** file:

```
	geth --datadir account/ init vanet.json
	
```
 
#### NOTE: 
The private key of the account is located in the folder ~/account/keystore/


Now we are able to start the private Ethereum PoA blockchain network command with the newly created account:

```
	geth --port 3000 --networkid 5775 --datadir=./account --maxpeers=5  --rpc --rpcport 8543 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console 

```

The blockchain network is live and we are able from the console to interact with it. We now can check the coinbase 
and signers in the network:

```
	> eth.coinbase
	"0x2807ea8cebe149ef2489937d9a711045bbc3ba4b"	


	> clique.getSigners()
	"0x2807ea8cebe149ef2489937d9a711045bbc3ba4b"

```

It is very important to see your address as a signer in order to mine blocks. Now we must unlock our account:


```
	> personal.unlockAccount(eth.coinbase, ”<your-password>”, 9999999)
	true
	
```

Then we can create new account on the same node in order to start the mining:

```
	> personal.newAccount(“<your-password>”)
	"0x1b0c49d5dfc8674fb5113b10570eba0e7ed55c95"
	
	
	> personal.unlockAccount(eth.accounts[1], ”<your-password>”, 9999999)
	true

```



#### NOTE:

In order a contract to be deployed on the network, node must be mining blocks.

### Connecting multiple nodes:

We need to create a new account and initialize it with the same genesis file **vaner.json**:


```
	geth --datadir account2/ init vanet.json

```

```
	geth --port 3001 --networkid 5775 --datadir=./account2 --maxpeers=5  --rpc --rpcport 8544 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner" console

```

#### NOTE:

Port and rpc port must always be different.

The connecting node needs to know * *enode* * of the node it is connecting to (node 2 -> node 1):

On Node 2 in the Ehtereum console you need the following command to enter in order to get the enode address:

```
	> admin.nodeInfo.enode
	“enode://76fb6251733cc706f84e7f7cb8a0d382644572c64f4d6c2268e3783fcc0a31756f9a311c8d7e93e1990cb5be716c57303759ff510bb8a2bc375c0dc00be5c0ab@[::]:3001”
```

The [::] in the enode URI should be replaced with the IP address of the machine on which the node is running. Now on Node 1 
you need to add the enode as a peer:

```
	> admin.addPeer("enode://76fb6251733cc706f84e7f7cb8a0d382644572c64f4d6c2268e3783fcc0a31756f9a311c8d7e93e1990cb5be716c57303759ff510bb8a2bc375c0dc00be5c0ab@192.168.0.30:3001")
	true
```

Now, you can check if the two nodes are connected with command:

```
	admin.peers
```

And start the mining: 

```
	> miner.start()

```


In order to deploy the smart contract with truffle we need to supply the information about the private network in the 
**truffle-config.js** file. In the network field of the file we need to add:


```
	module.exports = {
	 
	   rpc: {
			host:"localhost",
			port:8543
		},
	   
		networks: {
		
			development: {
				host: "localhost", //our network is running on localhost
				port: 8543, // port where your blockchain is running
				network_id: "*",
				from: "0x2807ea8cebe149ef2489937d9a711045bbc3ba4b", // use the account-id generated during the setup process
				gas: 1000000
			
			}
	   
		},
	  ...
	}
```


Also the mining must be started in order the contract to be deployed on the blockchain. Deploying the smart contract is started
with the command:

```
	truffle migrate
```

After the successful migration of the contract, you need to extract the smart contract's address from the
migration command output.

Then you need to compile the ABI of the solidity source code which is used by the program as a command-line
argument in order to connect to the deployed contract. The command is:

```
	solcjs --abi contracts/Transmission.sol
```
From there the program can be started with the command:

```
	python src/main.py -pk <your-private-key-here> -rpc <your-connection-choice-here> -abi <path-to-the-transmission-contract-abi> -ca <contract-address-on-the-blockchain-here>
```

Example:


```
	python src/main.py -pk 4958f5f9be75da558b0edb98cf5d887878013bae3aadb1e285732da64bf58f2c -rpc http://127.0.0.1:8543 -abi ./contracts/Transmission_sol_Transmission.abi -ca 0x8c20f00b98cb1F9E3d86fe349e0818A57d782Ad6
```

For additional help run the command:


```
	python src/main.py -h
	
```


### Addtional commands:

Proposing new PoA sealers on the blockchain (Only sealers listed as signers can propose another sealers):
	

```
	clique.propose("0x1b0c49d5dfc8674fb5113b10570eba0e7ed55c95", true)	
```

#### Important: In other to access accounts on different machines, key files must be added to geth!

