

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
		from: "0x89ce3feccf32d07eff867d3139aa1f3795f5ebec", // use the account-id generated during the setup process
		gas: 1000000
    
	}
   
  },

  // Set default mocha options here, use special reporters etc.
  mocha: {
    // timeout: 100000
  },

  // Configure your compilers
  compilers: {
    solc: {
      // version: "0.5.1",    // Fetch exact version from solc-bin (default: truffle's version)
      // docker: true,        // Use "0.5.1" you've installed locally with docker (default: false)
      // settings: {          // See the solidity docs for advice about optimization and evmVersion
      //  optimizer: {
      //    enabled: false,
      //    runs: 200
      //  },
      //  evmVersion: "byzantium"
      // }
    }
  }
}
