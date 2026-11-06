import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { ArrowLeft, Calendar, Users, Edit2, Check, ArrowUp, MessageSquare, Repeat, Bookmark, Share, UserPlus, UserCheck } from 'lucide-react';

export default function Profile({ userId, currentUserId, onBack, onOpenProfile }) {
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [followersList, setFollowersList] = useState([]);
  const [followingList, setFollowingList] = useState([]);
  const [activeSubTab, setActiveSubTab] = useState('posts'); // 'posts' | 'followers' | 'following'
  const [loading, setLoading] = useState(true);
  const [listLoading, setListLoading] = useState(false);
  const [isEditingBio, setIsEditingBio] = useState(false);
  const [bioInput, setBioInput] = useState('');
  const [isSavingBio, setIsSavingBio] = useState(false);
  const [isFollowing, setIsFollowing] = useState(false);
  const [followersCount, setFollowersCount] = useState(0);

  const isSelf = parseInt(currentUserId, 10) === parseInt(userId, 10);

  useEffect(() => {
    loadProfileData();
    setActiveSubTab('posts');
  }, [userId]);

  const loadProfileData = async () => {
    setLoading(true);
    try {
      const [profileData, userPosts] = await Promise.all([
        api.getUserProfile(userId),
        api.getUserPosts(userId)
      ]);
      setProfile(profileData);
      setPosts(userPosts);
      setBioInput(profileData.bio || '');
      setIsFollowing(profileData.is_following);
      setFollowersCount(profileData.followers_count || 0);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubTabChange = async (tab) => {
    setActiveSubTab(tab);
    if (tab === 'followers' && followersList.length === 0) {
      setListLoading(true);
      try {
        const data = await api.getFollowers(userId);
        setFollowersList(data);
      } catch (err) {
        console.error(err);
      } finally {
        setListLoading(false);
      }
    } else if (tab === 'following' && followingList.length === 0) {
      setListLoading(true);
      try {
        const data = await api.getFollowing(userId);
        setFollowingList(data);
      } catch (err) {
        console.error(err);
      } finally {
        setListLoading(false);
      }
    }
  };

  const handleToggleFollow = async () => {
    try {
      if (isFollowing) {
        setIsFollowing(false);
        setFollowersCount(prev => Math.max(0, prev - 1));
        await api.unfollowUser(userId);
      } else {
        setIsFollowing(true);
        setFollowersCount(prev => prev + 1);
        await api.followUser(userId);
      }
    } catch (err) {
      console.error(err);
      setIsFollowing(profile.is_following);
      setFollowersCount(profile.followers_count);
      alert(err.message);
    }
  };

  const handleSaveBio = async () => {
    setIsSavingBio(true);
    try {
      await api.updateBio(bioInput);
      setProfile(prev => ({ ...prev, bio: bioInput }));
      setIsEditingBio(false);
    } catch (err) {
      alert(err.message);
    } finally {
      setIsSavingBio(false);
    }
  };

  const handleLikePost = async (postId) => {
    setPosts(posts.map(p => {
      if (p.post_id === postId) {
        return { ...p, like_count: (p.like_count || 0) + 1, has_liked: true };
      }
      return p;
    }));

    try {
      await api.likePost(postId);
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
        Loading profile...
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
        <p>User profile not found.</p>
        <button className="primary" onClick={onBack} style={{ marginTop: '1rem' }}>
          Back to Feed
        </button>
      </div>
    );
  }

  const username = profile.username || 'User';

  return (
    <div className="profile-view animate-slide-up">
      {/* Top Header & Back Button */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
        <button 
          onClick={onBack}
          style={{ 
            backgroundColor: 'var(--bg-secondary)', 
            border: '1px solid var(--border-color)', 
            borderRadius: '50%', 
            width: '38px', 
            height: '38px', 
            padding: 0 
          }}
          title="Back to Feed"
        >
          <ArrowLeft size={18} />
        </button>
        <div>
          <h2 style={{ fontSize: '1.25rem', lineHeight: '1.2' }}>{username}</h2>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            {posts.length} {posts.length === 1 ? 'publication' : 'publications'}
          </span>
        </div>
      </div>

      {/* Main Profile Header Card */}
      <div className="profile-card">
        <div className="profile-banner"></div>
        <div className="profile-body">
          <div className="profile-avatar-row">
            <img 
              src={`https://ui-avatars.com/api/?name=${username}&background=random&size=128`} 
              className="profile-avatar" 
              alt={username} 
            />
            <div>
              {isSelf ? (
                <button 
                  className="secondary" 
                  onClick={() => setIsEditingBio(prev => !prev)}
                >
                  <Edit2 size={16} /> {isEditingBio ? 'Cancel' : 'Edit Bio'}
                </button>
              ) : (
                <button 
                  className={isFollowing ? 'secondary' : 'primary'}
                  onClick={handleToggleFollow}
                >
                  {isFollowing ? <><UserCheck size={16} /> Following</> : <><UserPlus size={16} /> Follow</>}
                </button>
              )}
            </div>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              {username} <span style={{ color: 'var(--accent-primary)', fontSize: '1.1rem' }}>&#10003;</span>
            </h1>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              @{username.toLowerCase().replace(/\s+/g, '_')}
            </div>
          </div>

          {/* Bio Section */}
          {isEditingBio ? (
            <div style={{ marginBottom: '1.25rem' }}>
              <textarea 
                value={bioInput}
                onChange={(e) => setBioInput(e.target.value)}
                rows={3}
                style={{ 
                  width: '100%', 
                  padding: '0.75rem', 
                  borderRadius: '8px', 
                  border: '1px solid var(--accent-primary)', 
                  fontFamily: 'Inter, sans-serif',
                  fontSize: '0.9rem',
                  resize: 'vertical',
                  marginBottom: '0.5rem'
                }}
                placeholder="Write your bio..."
              />
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button 
                  className="primary" 
                  disabled={isSavingBio}
                  onClick={handleSaveBio}
                >
                  <Check size={16} /> {isSavingBio ? 'Saving...' : 'Save Bio'}
                </button>
                <button 
                  className="secondary" 
                  onClick={() => setIsEditingBio(false)}
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem', lineHeight: '1.5', marginBottom: '1rem' }}>
              {profile.bio || <span style={{ color: 'var(--text-tertiary)', fontStyle: 'italic' }}>No bio provided yet.</span>}
            </p>
          )}

          {/* Mutual Followers (Stored Procedure Result) with Clickable Connections */}
          {!isSelf && profile.mutual_followers && profile.mutual_followers.length > 0 && (
            <div className="mutual-pill" style={{ flexWrap: 'wrap' }}>
              <Users size={16} />
              <span>Mutual connections: </span>
              {profile.mutual_followers.map((m, idx) => (
                <span 
                  key={m.user_id} 
                  className="author-clickable" 
                  onClick={() => onOpenProfile(m.user_id)}
                  title={`View ${m.username}'s profile`}
                  style={{ fontWeight: '700' }}
                >
                  {m.username}{idx < profile.mutual_followers.length - 1 ? ', ' : ''}
                </span>
              ))}
            </div>
          )}

          {/* Joined date & Meta */}
          <div style={{ display: 'flex', gap: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <Calendar size={15} />
              <span>Joined {new Date(profile.created_at).toLocaleDateString(undefined, { month: 'short', year: 'numeric' })}</span>
            </div>
            {profile.email && isSelf && (
              <div style={{ color: 'var(--text-secondary)' }}>
                {profile.email}
              </div>
            )}
          </div>

          {/* Interactive Numerical Stats Row (Click to toggle subtabs) */}
          <div className="profile-stats-row">
            <div 
              className="stat-item author-clickable" 
              onClick={() => handleSubTabChange('posts')}
              style={{ cursor: 'pointer' }}
            >
              <span className="stat-number">{profile.posts_count || posts.length}</span>
              <span className="stat-label" style={{ color: activeSubTab === 'posts' ? 'var(--accent-primary)' : undefined }}>
                Publications
              </span>
            </div>
            <div 
              className="stat-item author-clickable" 
              onClick={() => handleSubTabChange('followers')}
              style={{ cursor: 'pointer' }}
            >
              <span className="stat-number">{followersCount}</span>
              <span className="stat-label" style={{ color: activeSubTab === 'followers' ? 'var(--accent-primary)' : undefined }}>
                Followers
              </span>
            </div>
            <div 
              className="stat-item author-clickable" 
              onClick={() => handleSubTabChange('following')}
              style={{ cursor: 'pointer' }}
            >
              <span className="stat-number">{profile.following_count || 0}</span>
              <span className="stat-label" style={{ color: activeSubTab === 'following' ? 'var(--accent-primary)' : undefined }}>
                Following
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Subtab navigation */}
      <div className="feed-tabs" style={{ marginBottom: '1.5rem' }}>
        <div 
          className={`feed-tab ${activeSubTab === 'posts' ? 'active' : ''}`}
          onClick={() => handleSubTabChange('posts')}
        >
          Publications ({posts.length})
        </div>
        <div 
          className={`feed-tab ${activeSubTab === 'followers' ? 'active' : ''}`}
          onClick={() => handleSubTabChange('followers')}
        >
          Followers ({followersCount})
        </div>
        <div 
          className={`feed-tab ${activeSubTab === 'following' ? 'active' : ''}`}
          onClick={() => handleSubTabChange('following')}
        >
          Following ({profile.following_count || 0})
        </div>
      </div>

      {/* 1. Subtab: Followers List */}
      {activeSubTab === 'followers' && (
        <div>
          {listLoading ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>Loading followers...</div>
          ) : followersList.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
              No followers yet.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {followersList.map(follower => (
                <div 
                  key={follower.user_id} 
                  className="post-card"
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem' }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                    <img 
                      src={`https://ui-avatars.com/api/?name=${follower.username}&background=random`} 
                      className="avatar avatar-clickable" 
                      alt={follower.username} 
                      onClick={() => onOpenProfile(follower.user_id)}
                      title={`View ${follower.username}'s profile`}
                    />
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <span 
                        className="author-clickable" 
                        style={{ fontWeight: '700', fontSize: '0.95rem' }}
                        onClick={() => onOpenProfile(follower.user_id)}
                      >
                        {follower.username}
                      </span>
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                        @{follower.username.toLowerCase().replace(/\s+/g, '_')}
                      </span>
                      {follower.bio && (
                        <span style={{ color: 'var(--text-primary)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
                          {follower.bio}
                        </span>
                      )}
                    </div>
                  </div>
                  <button 
                    className="secondary" 
                    onClick={() => onOpenProfile(follower.user_id)}
                    style={{ fontSize: '0.8rem', padding: '0.4rem 0.9rem' }}
                  >
                    View Profile
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* 2. Subtab: Following List */}
      {activeSubTab === 'following' && (
        <div>
          {listLoading ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>Loading following...</div>
          ) : followingList.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
              Not following anyone yet.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {followingList.map(following => (
                <div 
                  key={following.user_id} 
                  className="post-card"
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem' }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                    <img 
                      src={`https://ui-avatars.com/api/?name=${following.username}&background=random`} 
                      className="avatar avatar-clickable" 
                      alt={following.username} 
                      onClick={() => onOpenProfile(following.user_id)}
                      title={`View ${following.username}'s profile`}
                    />
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <span 
                        className="author-clickable" 
                        style={{ fontWeight: '700', fontSize: '0.95rem' }}
                        onClick={() => onOpenProfile(following.user_id)}
                      >
                        {following.username}
                      </span>
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                        @{following.username.toLowerCase().replace(/\s+/g, '_')}
                      </span>
                      {following.bio && (
                        <span style={{ color: 'var(--text-primary)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
                          {following.bio}
                        </span>
                      )}
                    </div>
                  </div>
                  <button 
                    className="secondary" 
                    onClick={() => onOpenProfile(following.user_id)}
                    style={{ fontSize: '0.8rem', padding: '0.4rem 0.9rem' }}
                  >
                    View Profile
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* 3. Subtab: User's Posts */}
      {activeSubTab === 'posts' && (
        <div>
          {posts.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
              No posts published by this author yet.
            </div>
          ) : (
            <div className="post-list">
              {posts.map(post => (
                <div key={post.post_id} className="post-card">
                  <div className="post-header">
                    <img 
                      src={`https://ui-avatars.com/api/?name=${username}&background=random`} 
                      className="avatar" 
                      alt={username} 
                    />
                    <div className="post-meta">
                      <span className="post-author-name">{username} <span style={{ color: 'var(--accent-primary)' }}>&#10003;</span></span>
                      <span className="post-author-handle">
                        @{username.toLowerCase().replace(/\s+/g, '_')} • {new Date(post.created_at).toLocaleDateString()}
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

                  {Array.isArray(post.tags) && post.tags.length > 0 && (
                    <div className="post-tags" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginTop: '0.75rem', marginBottom: '0.5rem' }}>
                      {post.tags.map((tg, i) => (
                        <span key={i} className="tag">#{tg}</span>
                      ))}
                    </div>
                  )}

                  <div className="post-interaction-bar">
                    <button 
                      className={`interaction-btn ${post.has_liked ? 'upvoted' : ''}`}
                      onClick={() => handleLikePost(post.post_id)}
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
                      <button className="interaction-btn">
                        <Bookmark size={18} />
                      </button>
                      <button className="interaction-btn">
                        <Share size={18} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
