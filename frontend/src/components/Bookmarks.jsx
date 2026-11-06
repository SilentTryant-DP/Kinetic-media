import React from 'react';
import { Bookmark, ArrowUp, MessageSquare, Repeat, Share, Trash2 } from 'lucide-react';

export default function Bookmarks({ bookmarkedPosts = [], onToggleBookmark, onOpenProfile, onLikePost }) {
  return (
    <div className="bookmarks-view animate-slide-up">
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Bookmark size={24} style={{ color: 'var(--accent-primary)' }} /> Bookmarks & Saved Publications
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          {bookmarkedPosts.length} saved {bookmarkedPosts.length === 1 ? 'publication' : 'publications'} for quick reference.
        </p>
      </div>

      {bookmarkedPosts.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem 1.5rem', color: 'var(--text-secondary)' }}>
          <Bookmark size={36} style={{ margin: '0 auto 1rem', opacity: 0.3 }} />
          <h3 style={{ fontSize: '1.1rem', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>No bookmarked publications</h3>
          <p style={{ fontSize: '0.85rem', maxWidth: '360px', margin: '0 auto' }}>
            Click the bookmark icon on any post in your feed to save essays and technical discussions here.
          </p>
        </div>
      ) : (
        <div className="post-list">
          {bookmarkedPosts.map((post) => {
            const authorName = post.username || post.author || 'User';
            return (
              <div key={post.post_id} className="post-card">
                <div className="post-header">
                  <img 
                    src={`https://ui-avatars.com/api/?name=${authorName}&background=random`} 
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
                  <button 
                    onClick={() => onToggleBookmark(post)}
                    style={{ marginLeft: 'auto', background: 'transparent', color: 'var(--accent-primary)', padding: '0.3rem' }}
                    title="Remove from bookmarks"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>

                <div className="post-content">
                  {post.content}
                </div>

                <div className="post-interaction-bar">
                  <button 
                    className={`interaction-btn ${post.has_liked ? 'upvoted' : ''}`}
                    onClick={() => onLikePost && onLikePost(post.post_id)}
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
                      className="interaction-btn"
                      onClick={() => onToggleBookmark(post)}
                      style={{ color: 'var(--accent-primary)' }}
                      title="Remove Bookmark"
                    >
                      <Bookmark size={18} fill="currentColor" />
                    </button>
                    <button className="interaction-btn">
                      <Share size={18} />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
