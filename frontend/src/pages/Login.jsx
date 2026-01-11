
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../services/api';
import './Login.css';

const Login = ({ setUser }) => {
    const [passkey, setPasskey] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const data = await loginUser(passkey);
            // Expected data: { address, balance, message }
            setUser(data);
            navigate('/dashboard');
        } catch (err) {
            setError(err.error || "Login failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2 className="login-title">Plagiarism Guard</h2>
                <h3 className="login-subtitle">Welcome Back</h3>

                <form onSubmit={handleLogin} className="login-form">
                    <div className="login-input-group">
                        <label className="login-label">Private Key</label>
                        <input
                            type="password"
                            placeholder="Enter your private key"
                            value={passkey}
                            onChange={(e) => setPasskey(e.target.value)}
                            className="login-input"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="login-button"
                    >
                        {loading ? 'Authenticating...' : 'Login'}
                    </button>
                </form>

                {error && (
                    <div className="login-error-container">
                        <p className="login-error">{error}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Login;
