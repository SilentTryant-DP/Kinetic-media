import React from 'react';
import { ArrowRight, Globe, Database, Zap } from 'lucide-react';

export default function Landing({ onGetStarted }) {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '2rem', textAlign: 'center' }}>
      <div className="post-card animate-slide-up" style={{ padding: '4rem', maxWidth: '800px', width: '100%', border: 'none', boxShadow: '0 20px 40px rgba(0,0,0,0.08)' }}>
        <h1 style={{ fontSize: '3.5rem', fontWeight: '800', marginBottom: '1.5rem', color: 'var(--text-primary)', lineHeight: '1.2' }}>
          Connect with the <span style={{ color: 'var(--accent-primary)' }}>World</span>
        </h1>
        <p style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', marginBottom: '3.5rem', maxWidth: '600px', margin: '0 auto 3.5rem auto' }}>
          Experience a next-generation social platform powered by a robust SQL database. Share your thoughts, follow friends, and engage in real-time.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem', marginBottom: '3.5rem' }}>
          <div style={{ padding: '1.5rem', backgroundColor: 'var(--bg-tertiary)', borderRadius: '16px' }}>
            <Globe style={{ color: 'var(--accent-primary)', marginBottom: '1rem', width: '32px', height: '32px', margin: '0 auto 1rem auto' }} />
            <h3 style={{ marginBottom: '0.5rem', fontWeight: '700' }}>Global Feed</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>See what your network is talking about instantly.</p>
          </div>
          
          <div style={{ padding: '1.5rem', backgroundColor: 'var(--bg-tertiary)', borderRadius: '16px' }}>
            <Zap style={{ color: '#f59e0b', marginBottom: '1rem', width: '32px', height: '32px', margin: '0 auto 1rem auto' }} />
            <h3 style={{ marginBottom: '0.5rem', fontWeight: '700' }}>Instant Interactions</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Like and follow with lightning fast responses.</p>
          </div>

          <div style={{ padding: '1.5rem', backgroundColor: 'var(--bg-tertiary)', borderRadius: '16px' }}>
            <Database style={{ color: '#10b981', marginBottom: '1rem', width: '32px', height: '32px', margin: '0 auto 1rem auto' }} />
            <h3 style={{ marginBottom: '0.5rem', fontWeight: '700' }}>SQL Powered</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Built on a rock-solid normalized database schema.</p>
          </div>
        </div>

        <button className="primary" onClick={onGetStarted} style={{ padding: '1.25rem 3.5rem', fontSize: '1.1rem', borderRadius: '50px' }}>
          Get Started <ArrowRight size={20} />
        </button>
      </div>
    </div>
  );
}
