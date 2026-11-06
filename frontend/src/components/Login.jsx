import React, { useState } from 'react';
import { api } from '../api';

export default function Login({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    bio: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        const res = await api.login({ email: formData.email, password: formData.password });
        localStorage.setItem('userId', res.userId);
        onLoginSuccess(res.userId);
      } else {
        const res = await api.register(formData);
        localStorage.setItem('userId', res.userId);
        onLoginSuccess(res.userId);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container animate-slide-up">
      <div className="card glass">
        <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
        
        {error && <div style={{ color: 'var(--danger-color)', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="input-group">
              <label>Username</label>
              <input type="text" name="username" value={formData.username} onChange={handleChange} required />
            </div>
          )}
          
          <div className="input-group">
            <label>Email</label>
            <input type="email" name="email" value={formData.email} onChange={handleChange} required />
          </div>
          
          <div className="input-group">
            <label>Password</label>
            <input type="password" name="password" value={formData.password} onChange={handleChange} required />
          </div>

          {!isLogin && (
            <div className="input-group">
              <label>Bio (Optional)</label>
              <textarea name="bio" value={formData.bio} onChange={handleChange}></textarea>
            </div>
          )}

          <button type="submit" className="primary" disabled={loading}>
            {loading ? 'Please wait...' : (isLogin ? 'Log In' : 'Sign Up')}
          </button>
        </form>
        
        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button className="toggle-link" onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? 'Sign up' : 'Log in'}
          </button>
        </div>
      </div>
    </div>
  );
}
