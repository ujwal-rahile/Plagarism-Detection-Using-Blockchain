import React, { useState } from 'react';
import { uploadFile } from '../services/api';
import './Dashboard.css';

const Dashboard = ({ user, logout, setUser }) => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setResult(null);
        setError('');
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a file first");
            return;
        }

        setLoading(true);
        setError('');

        try {
            const data = await uploadFile(file, user.address);
            setResult(data);
            // Update balance in global state
            setUser({ ...user, balance: data.final_balance });
        } catch (err) {
            setError(err.error || "Upload failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1 className="dashboard-title">Plagiarism Guard</h1>
                <span className="dashboard-balance">
                    Balance: <span className="dashboard-balance-value">{user?.balance} ETH</span>
                </span>
                <button onClick={logout} className="dashboard-logout-btn">Logout</button>
            </header>

            <main className="dashboard-main">
                <div className="dashboard-card">
                    <h3 className="dashboard-card-title">Check Document</h3>
                    <p className="dashboard-card-description">Upload a document to verify its authenticity on the blockchain.</p>

                    <div className="dashboard-upload-area">
                        <input
                            type="file"
                            onChange={handleFileChange}
                            accept=".txt,.pdf,.docx"
                            className="dashboard-file-input"
                            id="file-upload"
                        />
                        <label htmlFor="file-upload" className="dashboard-file-label">
                            {file ? file.name : "Choose File"}
                        </label>
                    </div>

                    <button
                        onClick={handleUpload}
                        disabled={loading || !file}
                        className="dashboard-button"
                    >
                        {loading ? 'Processing...' : 'Upload & Check'}
                    </button>

                    {error && (
                        <div className="dashboard-error-container">
                            <p className="dashboard-error">{error}</p>
                        </div>
                    )}
                </div>

                {result && (
                    <div className="dashboard-results-card">
                        <h3 className="dashboard-results-title">Analysis Results</h3>

                        <div className={result.is_valid ? "dashboard-success-box" : "dashboard-fail-box"}>
                            <div className="dashboard-status-row">
                                <span className="dashboard-status-label">Status:</span>
                                <span className="dashboard-status-value">{result.is_valid ? "ACCEPTED" : "REJECTED"}</span>
                            </div>

                            <div className="dashboard-score-row">
                                <span className="dashboard-score-label">Plagiarism Score:</span>
                                <span className="dashboard-score-value">{result.plagiarism_percent}%</span>
                            </div>

                            <div className="dashboard-divider"></div>

                            {result.plagiarized_content && result.plagiarized_content.length > 0 && (
                                <div className="dashboard-chunks-section">
                                    <p className="dashboard-chunks-label">Plagiarized Segments:</p>
                                    <div className="dashboard-chunks-list">
                                        {result.plagiarized_content.map((segment, index) => (
                                            <div key={index} className="dashboard-chunk-item">
                                                "{segment}"
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            <div className="dashboard-meta-info">
                                <p>Transaction Cost: <span className="dashboard-mono">{(parseFloat(result.initial_balance) - parseFloat(result.final_balance)).toFixed(6)} ETH</span></p>
                                <p>Final Balance: <span className="dashboard-mono">{result.final_balance} ETH</span></p>
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default Dashboard;
