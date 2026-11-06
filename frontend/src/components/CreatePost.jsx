import React, { useState } from 'react';
import { api } from '../api';
import { Image, Code, BarChart2, Globe } from 'lucide-react';

export default function CreatePost({ onPostCreated }) {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;
    
    setLoading(true);
    try {
      // Auto-extract hashtags from text
      const extractedTags = (content.match(/#[\w-]+/g) || []).map(t => t.replace('#', ''));
      await api.createPost({ content, tags: extractedTags });
      setContent('');
      onPostCreated();
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-post-card">
      <form onSubmit={handleSubmit}>
        <div className="create-input-area">
          <img src="https://ui-avatars.com/api/?name=User&background=random" className="avatar" alt="Avatar" />
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Share an insight, project, or thought..."
            disabled={loading}
          />
        </div>
        
        <div className="create-actions">
          <div className="create-tools">
            <button type="button" className="tool-btn">
              <Image size={16} className="text-accent-secondary" /> Media
            </button>
            <button type="button" className="tool-btn">
              <Code size={16} /> Snippet
            </button>
            <button type="button" className="tool-btn">
              <BarChart2 size={16} /> Poll
            </button>
          </div>
          
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
              <Globe size={14} /> Everyone
            </div>
            <button type="submit" className="primary" disabled={loading || !content.trim()}>
              {loading ? 'Publishing...' : 'Publish'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
