const FaceAuth = artifacts.require("FaceAuth");

contract("FaceAuth", (accounts) => {
  let faceAuth;
  const owner = accounts[0];
  const user1 = accounts[1];
  const user2 = accounts[2];

  beforeEach(async () => {
    faceAuth = await FaceAuth.new({ from: owner });
  });

  describe("User Registration", () => {
    it("should register a new user successfully", async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";

      const tx = await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
      
      assert.equal(tx.logs.length, 1);
      assert.equal(tx.logs[0].event, "UserRegistered");
      assert.equal(tx.logs[0].args.username, username);
      assert.equal(tx.logs[0].args.passwordHash, passwordHash);
      assert.equal(tx.logs[0].args.faceHash, faceHash);

      const isRegistered = await faceAuth.isRegistered(username);
      assert.equal(isRegistered, true);
    });

    it("should not register user with empty username", async () => {
      const username = "";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";

      try {
        await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
        assert.fail("Expected revert");
      } catch (error) {
        assert.include(error.message, "Username cannot be empty");
      }
    });

    it("should not register user with empty password hash", async () => {
      const username = "testuser";
      const passwordHash = "";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";

      try {
        await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
        assert.fail("Expected revert");
      } catch (error) {
        assert.include(error.message, "Password hash cannot be empty");
      }
    });

    it("should not register user with empty face hash", async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "";

      try {
        await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
        assert.fail("Expected revert");
      } catch (error) {
        assert.include(error.message, "Face hash cannot be empty");
      }
    });

    it("should not register duplicate user", async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";

      await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });

      try {
        await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
        assert.fail("Expected revert");
      } catch (error) {
        assert.include(error.message, "User already exists");
      }
    });
  });

  describe("User Queries", () => {
    beforeEach(async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";
      await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
    });

    it("should return user data correctly", async () => {
      const username = "testuser";
      const [passwordHash, faceHash] = await faceAuth.getUserHash(username);
      
      assert.equal(passwordHash, "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8");
      assert.equal(faceHash, "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3");
    });

    it("should return false for non-existent user", async () => {
      const isRegistered = await faceAuth.isRegistered("nonexistent");
      assert.equal(isRegistered, false);
    });

    it("should return true for existing user", async () => {
      const isRegistered = await faceAuth.isRegistered("testuser");
      assert.equal(isRegistered, true);
    });

    it("should get user count correctly", async () => {
      const count = await faceAuth.getUserCount();
      assert.equal(count, 1);

      // Register another user
      await faceAuth.registerUser("user2", "hash2", "face2", { from: owner });
      const newCount = await faceAuth.getUserCount();
      assert.equal(newCount, 2);
    });
  });

  describe("User Verification", () => {
    beforeEach(async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";
      await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
    });

    it("should verify user with correct credentials", async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";

      const result = await faceAuth.verifyUser(username, passwordHash, faceHash);
      assert.equal(result, true);
    });

    it("should reject user with incorrect password", async () => {
      const username = "testuser";
      const passwordHash = "wrongpasswordhash";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";

      const result = await faceAuth.verifyUser(username, passwordHash, faceHash);
      assert.equal(result, false);
    });

    it("should reject user with incorrect face hash", async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "wrongfacehash";

      const result = await faceAuth.verifyUser(username, passwordHash, faceHash);
      assert.equal(result, false);
    });

    it("should reject non-existent user", async () => {
      const username = "nonexistent";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";

      const result = await faceAuth.verifyUser(username, passwordHash, faceHash);
      assert.equal(result, false);
    });
  });

  describe("Face Hash Update", () => {
    beforeEach(async () => {
      const username = "testuser";
      const passwordHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8";
      const faceHash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";
      await faceAuth.registerUser(username, passwordHash, faceHash, { from: owner });
    });

    it("should update face hash for existing user", async () => {
      const username = "testuser";
      const newFaceHash = "newfacehash123456789";

      const tx = await faceAuth.updateFaceHash(username, newFaceHash, { from: owner });
      
      assert.equal(tx.logs.length, 1);
      assert.equal(tx.logs[0].event, "UserRegistered");

      const [passwordHash, faceHash] = await faceAuth.getUserHash(username);
      assert.equal(faceHash, newFaceHash);
    });

    it("should not update face hash for non-existent user", async () => {
      const username = "nonexistent";
      const newFaceHash = "newfacehash123456789";

      try {
        await faceAuth.updateFaceHash(username, newFaceHash, { from: owner });
        assert.fail("Expected revert");
      } catch (error) {
        assert.include(error.message, "User does not exist");
      }
    });
  });
});

