import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { ArrowUp, MessageSquare, Repeat, Bookmark, Share } from 'lucide-react';

export default function Feed({ userId, onOpenProfile, activeFeedTab = 'for-you', bookmarkedPostIds = [], onToggleBookmark }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFeed();
  }, []);

  const loadFeed = async () => {
    try {
      const data = await api.getFeed();
      setPosts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (postId) => {
    setPosts(posts.map(p => {
      if (p.post_id === postId) {
        return { ...p, like_count: (p.like_count || 0) + 1, has_liked: true };
      }
      return p;
    }));

    try {
      await api.likePost(postId);
    } catch (err) {
      loadFeed();
      alert(err.message);
    }
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>Loading feed...</div>;
  if (posts.length === 0) return <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>No posts in your feed yet!</div>;

  const filteredPosts = posts.filter(post => {
    if (activeFeedTab === 'for-you') return true;
    if (activeFeedTab === 'following') {
      return post.user_id !== parseInt(userId, 10);
    }
    const content = (post.content || '').toLowerCase();
    const tags = Array.isArray(post.tags) ? post.tags : [];
    if (activeFeedTab === 'deep-dives') {
      return content.includes('algorithm') || content.includes('strategy') || content.includes('retention') || content.includes('datamodeling') || tags.some(t => ['Algorithm', 'Strategy', 'Business', 'Retention', 'Digital Transformation'].includes(t));
    }
    if (activeFeedTab === 'tech-design') {
      return content.includes('ai') || content.includes('chatgpt') || content.includes('tech') || tags.some(t => ['Artificial Intelligence', 'AI Tools', 'Technology', 'Digitalization', 'Automation'].includes(t));
    }
    if (activeFeedTab === 'essays') {
      return content.length > 200 || (post.line_count && post.line_count > 6) || tags.some(t => ['Mental Health', 'Personal Growth', 'Motivation', 'Family', 'Leadership'].includes(t));
    }
    return true;
  });

  return (
    <div className="post-list">
      {filteredPosts.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-secondary)' }}>
          No publications found under this category.
        </div>
      ) : (
        filteredPosts.map(post => {
          const authorName = post.username || post.author || 'User';
          const isBookmarked = bookmarkedPostIds.includes(post.post_id);
          const tags = Array.isArray(post.tags) ? post.tags : [];

          return (
            <div key={post.post_id} className="post-card">
              <div className="post-header">
                <img 
                  src={`https://ui-avatars.com/api/?name=${encodeURIComponent(authorName)}&background=random`} 
                  className="avatar avatar-clickable" 
                  alt="Avatar" 
                  onClick={() => onOpenProfile && onOpenProfile(post.user_id)}
                  title={`View ${authorName}'s profile`}
                />
                <div className="post-meta">
                  <span 
                    className="post-author-name author-clickable"
                    onClick={() => onOpenProfile && onOpenProfile(post.user_id)}
                    title={`View ${authorName}'s profile`}
                  >
                    {authorName} <span style={{ color: 'var(--accent-primary)' }}>&#10003;</span>
                  </span>
                  <span 
                    className="post-author-handle author-clickable"
                    onClick={() => onOpenProfile && onOpenProfile(post.user_id)}
                  >
                    @{authorName.toLowerCase().replace(/\s+/g, '_')} • {new Date(post.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div style={{ marginLeft: 'auto', display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                  {post.language && post.language !== 'English' && (
                    <span style={{ 
                      fontSize: '0.68rem', 
                      padding: '0.15rem 0.45rem', 
                      borderRadius: '4px',
                      background: 'rgba(59, 130, 246, 0.15)',
                      color: '#60a5fa',
                      border: '1px solid rgba(59, 130, 246, 0.3)'
                    }}>
                      {post.language}
                    </span>
                  )}
                  {post.tone && post.tone !== 'General' && (
                    <span style={{ 
                      fontSize: '0.68rem', 
                      padding: '0.15rem 0.45rem', 
                      borderRadius: '4px',
                      background: 'rgba(168, 85, 247, 0.15)',
                      color: '#c084fc',
                      border: '1px solid rgba(168, 85, 247, 0.3)'
                    }}>
                      {post.tone}
                    </span>
                  )}
                </div>
              </div>
              
              <div className="post-content" style={{ whiteSpace: 'pre-wrap' }}>
                {post.content}
              </div>

              <div className="post-tags" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginTop: '0.75rem', marginBottom: '0.5rem' }}>
                {tags.length > 0 ? (
                  tags.map((tg, i) => (
                    <span key={i} className="tag">#{tg}</span>
                  ))
                ) : (
                  <>
                    <span className="tag">#KineticSocial</span>
                    <span className="tag">#DBMS</span>
                  </>
                )}
              </div>
              
              <div className="post-interaction-bar">
                <button 
                  className={`interaction-btn ${post.has_liked ? 'upvoted' : ''}`}
                  onClick={() => handleLike(post.post_id)}
                >
                  <ArrowUp size={18} />
                  <span>{post.like_count || 0}</span>
                </button>
                <button className="interaction-btn">
                  <MessageSquare size={18} />
                  <span>0</span>
                </button>
                <button className="interaction-btn">
                  <Repeat size={18} />
                  <span>0</span>
                </button>

                <div style={{ marginLeft: 'auto', display: 'flex', gap: '0.5rem' }}>
                  <button 
                    className={`interaction-btn ${isBookmarked ? 'upvoted' : ''}`}
                    onClick={() => onToggleBookmark && onToggleBookmark(post)}
                    style={{ color: isBookmarked ? 'var(--accent-primary)' : undefined }}
                    title={isBookmarked ? 'Remove Bookmark' : 'Save Publication'}
                  >
                    <Bookmark size={18} fill={isBookmarked ? 'currentColor' : 'none'} />
                  </button>
                  <button className="interaction-btn">
                    <Share size={18} />
                  </button>
                </div>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}
