// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PlagiarismChecker {
    // Mapping to store all unique hashes globally
    mapping(bytes32 => bool) private _storedHashes;
    bytes32[] private _allHashes; // Optional: Maintains insertion order

    // Threshold for plagiarism (20%)
    uint256 public constant PLAGIARISM_THRESHOLD = 20;
    uint256 public minimumHashesRequired = 1; // Minimum hashes to check

    // Events
    event PlagiarismDetected(address indexed sender, uint256[] plagiarizedIndices, uint256 similarityPercentage);
    event DocumentStored(address indexed sender, bytes32[] hashes, uint256 storedCount);

    /**
     * @dev Checks hashes against stored database and handles storage if unique
     * @param contentHashes Array of content hashes to check
     * @return isPlagiarized True if similarity >= 20%
     * @return plagiarizedIndices Array of 0-based indices of plagiarized hashes
     * @return similarityPercentage Match percentage (0-100)
     */
    function checkAndStoreHashes(bytes32[] calldata contentHashes)
        external
        returns (
            bool isPlagiarized,
            uint256[] memory plagiarizedIndices,
            uint256 similarityPercentage
        )
    {
        require(contentHashes.length >= minimumHashesRequired, "Insufficient hashes");
        require(contentHashes.length <= 5000, "Too many hashes"); // Prevent gas issues

        uint256 matchCount;
        plagiarizedIndices = new uint256[](contentHashes.length);
        uint256 index = 0;

        // Check each hash against stored database
        for (uint256 i = 0; i < contentHashes.length; i++) {
            if (_storedHashes[contentHashes[i]]) {
                matchCount++;
                plagiarizedIndices[index++] = i; // 0-based index
            }
        }

        // Calculate similarity percentage
        similarityPercentage = (matchCount * 100) / contentHashes.length;
        isPlagiarized = similarityPercentage >= PLAGIARISM_THRESHOLD;

        // Trim plagiarizedIndices array
        uint256[] memory trimmedIndices = new uint256[](matchCount);
        for (uint256 i = 0; i < matchCount; i++) {
            trimmedIndices[i] = plagiarizedIndices[i];
        }
        plagiarizedIndices = trimmedIndices;

        // Emit plagiarism detection event
        emit PlagiarismDetected(msg.sender, plagiarizedIndices, similarityPercentage);

        // Store new hashes if not plagiarized
        if (!isPlagiarized) {
            uint256 storedCount = 0;
            for (uint256 i = 0; i < contentHashes.length; i++) {
                bytes32 currentHash = contentHashes[i];
                if (!_storedHashes[currentHash]) {
                    _storedHashes[currentHash] = true;
                    _allHashes.push(currentHash);
                    storedCount++;
                }
            }
            emit DocumentStored(msg.sender, contentHashes, storedCount);
        }

        return (isPlagiarized, plagiarizedIndices, similarityPercentage);
    }

    /**
     * @dev Returns all stored hashes (for verification)
     */
    function getAllStoredHashes() external view returns (bytes32[] memory) {
        return _allHashes;
    }

    /**
     * @dev Updates minimum hashes required for similarity calculation
     */
    function setMinimumHashesRequired(uint256 newMinimum) external {
        require(newMinimum > 0, "Minimum must be > 0");
        minimumHashesRequired = newMinimum;
    }
}