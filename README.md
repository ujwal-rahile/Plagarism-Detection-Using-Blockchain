# Plagiarism Detection Using Blockchain 🛡️

A decentralized application (DApp) that ensures document authenticity and detects plagiarism using Ethereum smart contracts. This system guarantees that once a document is recorded on the blockchain, its content hash is immutable and can be used to verify future submissions.

## 🚀 Features

-   **Immutable Records**: Stores document uniqueness on a local Ethereum blockchain (Ganache).
-   **Plagiarism Detection**: Compares new submissions against registered content to detect copied text.
-   **Content Visualization**: Displays exactly which parts of the text are plagiarized.
-   **Modern UI**: Built with React, featuring a premium Glassmorphism design and dark mode.
-   **Secure**: Uses private key authentication for transactions.

## 🛠️ Tech Stack

-   **Frontend**: React.js, Vite, CSS Modules
-   **Backend**: Python Flask, Web3.py
-   **Blockchain**: Ganache (Local Ethereum Testnet), Solidity (Smart Contracts)
-   **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

## 🏁 Getting Started

The entire application is containerized. You can get it up and running with a single command.

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd Plagarism-Detection-Using-Blockchain
    ```

2.  **Start the Application**
    ```bash
    docker-compose up --build
    ```

    *This will start the Frontend, Backend, and Ganache blockchain services.*

3.  **Access the App**
    -   **Frontend**: [http://localhost:5173](http://localhost:5173)
    -   **Backend API**: [http://localhost:5000](http://localhost:5000)
    -   **Ganache RPC**: [http://localhost:8545](http://localhost:8545)

## 🔑 Usage

1.  **Login**: Use one of the pre-funded private keys from the Ganache logs.
    > **Default Key**: `0x0114cf546c4bf388ad6ba699bb61d2938f4b978201c5d8e83a8b57a5ed3bc7c0`

2.  **Upload Original Content**:
    -   Upload a `.txt`, `.pdf`, or `.docx` file.
    -   The system will hash its content and store it on the blockchain.

3.  **Check for Plagiarism**:
    -   Upload another document.
    -   The system will compare it against stored hashes and report any matches.

## 📂 Project Structure

```
.
├── backend/            # Flask API & Blockchain Logic
├── frontend/           # React Application
├── Smart contract/     # Solidity Contracts
├── docker-compose.yml  # Service Orchestration
└── README.md           # Project Documentation
```
