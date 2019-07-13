const Transmission = artifacts.require("Transmission");

module.exports = function(deployer) {
  deployer.deploy(Transmission);
};
