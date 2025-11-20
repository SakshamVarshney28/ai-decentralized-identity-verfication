const FaceAuth = artifacts.require("FaceAuth");

module.exports = function (deployer) {
  deployer.deploy(FaceAuth);
};

