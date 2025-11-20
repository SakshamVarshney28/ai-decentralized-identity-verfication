// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title FaceAuth
 * @dev Smart contract for face-based authentication system
 * @notice Stores user credentials (username, password hash, face hash) on blockchain
 */
contract FaceAuth {
    // Struct to store user data
    struct User {
        string username;
        string passwordHash;
        string faceHash;
        bool exists;
    }
    
    // Mapping from username to User struct
    mapping(string => User) public users;
    
    // Array to store all registered usernames
    string[] public registeredUsers;
    
    // Events
    event UserRegistered(string indexed username, string passwordHash, string faceHash);
    event UserVerified(string indexed username, bool success);
    
    /**
     * @dev Register a new user with username, password hash, and face hash
     * @param username The username of the user
     * @param passwordHash SHA-256 hash of the user's password
     * @param faceHash SHA-256 hash of the user's face encoding
     */
    function registerUser(
        string memory username,
        string memory passwordHash,
        string memory faceHash
    ) public {
        require(!users[username].exists, "User already exists");
        require(bytes(username).length > 0, "Username cannot be empty");
        require(bytes(passwordHash).length > 0, "Password hash cannot be empty");
        require(bytes(faceHash).length > 0, "Face hash cannot be empty");
        
        users[username] = User({
            username: username,
            passwordHash: passwordHash,
            faceHash: faceHash,
            exists: true
        });
        
        registeredUsers.push(username);
        
        emit UserRegistered(username, passwordHash, faceHash);
    }
    
    /**
     * @dev Get user data by username
     * @param username The username to query
     * @return passwordHash The password hash
     * @return faceHash The face hash
     */
    function getUserHash(string memory username) public view returns (string memory passwordHash, string memory faceHash) {
        require(users[username].exists, "User does not exist");
        return (users[username].passwordHash, users[username].faceHash);
    }
    
    /**
     * @dev Check if a user is registered
     * @param username The username to check
     * @return exists True if user exists, false otherwise
     */
    function isRegistered(string memory username) public view returns (bool exists) {
        return users[username].exists;
    }
    
    /**
     * @dev Get user data by username
     * @param username The username to query
     * @return user The complete user data
     */
    function getUser(string memory username) public view returns (User memory user) {
        require(users[username].exists, "User does not exist");
        return users[username];
    }
    
    /**
     * @dev Get the total number of registered users
     * @return count The number of registered users
     */
    function getUserCount() public view returns (uint256 count) {
        return registeredUsers.length;
    }
    
    /**
     * @dev Get all registered usernames
     * @return usernames Array of all registered usernames
     */
    function getAllUsers() public view returns (string[] memory usernames) {
        return registeredUsers;
    }
    
    /**
     * @dev Verify user credentials
     * @param username The username to verify
     * @param passwordHash The password hash to verify
     * @param faceHash The face hash to verify
     * @return success True if credentials match, false otherwise
     */
    function verifyUser(
        string memory username,
        string memory passwordHash,
        string memory faceHash
    ) public view returns (bool success) {
        if (!users[username].exists) {
            return false;
        }

        User memory user = users[username];

        // Compare password hash and face hash
        bool passwordMatch = keccak256(bytes(user.passwordHash)) == keccak256(bytes(passwordHash));
        bool faceMatch = keccak256(bytes(user.faceHash)) == keccak256(bytes(faceHash));

        bool success_result = passwordMatch && faceMatch;

        return success_result;
    }

    
    /**
     * @dev Update user's face hash (for re-enrollment)
     * @param username The username of the user
     * @param newFaceHash The new face hash
     */
    function updateFaceHash(string memory username, string memory newFaceHash) public {
        require(users[username].exists, "User does not exist");
        require(bytes(newFaceHash).length > 0, "Face hash cannot be empty");
        
        users[username].faceHash = newFaceHash;
        
        emit UserRegistered(username, users[username].passwordHash, newFaceHash);
    }
}

