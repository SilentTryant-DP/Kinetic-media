import React, { useState, useEffect } from 'react';
import Landing from './components/Landing';
import Login from './components/Login';
import Feed from './components/Feed';
import CreatePost from './components/CreatePost';
import Sidebar from './components/Sidebar';
import RightPanel from './components/RightPanel';
import Notifications from './components/Notifications';
import Profile from './components/Profile';
import Communities from './components/Communities';
import Messages from './components/Messages';
import Bookmarks from './components/Bookmarks';
import { api } from './api';

function App() {
  const [view, setView] = useState('landing');
  const [userId, setUserId] = useState(null);
  const [currentUsername, setCurrentUsername] = useState('');
  const [activeTab, setActiveTab] = useState('home'); // 'home' | 'communities' | 'notifications' | 'messages' | 'bookmarks' | 'profile'
  const [activeFeedTab, setActiveFeedTab] = useState('for-you'); // 'for-you' | 'following' | 'deep-dives' | 'tech-design' | 'essays'
  const [selectedProfileUserId, setSelectedProfileUserId] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [bookmarkedPosts, setBookmarkedPosts] = useState([]);

  useEffect(() => {
    const storedId = localStorage.getItem('userId');
    if (storedId) {
      setUserId(storedId);
      setView('app');
      fetchCurrentUser(storedId);
    }

    try {
      const savedBookmarks = localStorage.getItem('kinetic_bookmarks');
      if (savedBookmarks) {
        setBookmarkedPosts(JSON.parse(savedBookmarks));
      }
    } catch (e) {
      console.error(e);
    }
  }, []);

  const fetchCurrentUser = async (id) => {
    try {
      const data = await api.getUserProfile(id);
      if (data && data.username) {
        setCurrentUsername(data.username);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleLoginSuccess = (id) => {
    setUserId(id);
    setView('app');
    fetchCurrentUser(id);
  };

  const handleLogout = () => {
    localStorage.removeItem('userId');
    setUserId(null);
    setCurrentUsername('');
    setSelectedProfileUserId(null);
    setActiveTab('home');
    setView('landing');
  };

  const handleRefreshFeed = () => {
    setRefreshKey(prev => prev + 1);
  };

  const handleOpenProfile = (targetUserId) => {
    setSelectedProfileUserId(targetUserId);
    setActiveTab('profile');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleTabChange = (tab) => {
    if (tab === 'profile') {
      setSelectedProfileUserId(userId);
      setActiveTab('profile');
    } else {
      setSelectedProfileUserId(null);
      setActiveTab(tab);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleBackToFeed = () => {
    setSelectedProfileUserId(null);
    setActiveTab('home');
  };

  const handleToggleBookmark = (post) => {
    setBookmarkedPosts(prev => {
      const exists = prev.some(p => p.post_id === post.post_id);
      let updated;
      if (exists) {
        updated = prev.filter(p => p.post_id !== post.post_id);
      } else {
        updated = [...prev, post];
      }
      localStorage.setItem('kinetic_bookmarks', JSON.stringify(updated));
      return updated;
    });
  };

  if (view === 'landing') {
    return <Landing onGetStarted={() => setView('auth')} />;
  }

  if (view === 'auth') {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app-layout animate-slide-up">
      <Sidebar 
        activeTab={activeTab} 
        onLogout={handleLogout} 
        onTabChange={handleTabChange}
        currentUsername={currentUsername}
      />
      
      <main className="feed-column">
        {activeTab === 'profile' && (
          <Profile 
            userId={selectedProfileUserId || userId} 
            currentUserId={userId} 
            onBack={handleBackToFeed}
            onOpenProfile={handleOpenProfile}
          />
        )}

        {activeTab === 'communities' && (
          <Communities onOpenProfile={handleOpenProfile} />
        )}

        {activeTab === 'notifications' && (
          <Notifications fullPage={true} onOpenProfile={handleOpenProfile} />
        )}

        {activeTab === 'messages' && (
          <Messages onOpenProfile={handleOpenProfile} />
        )}

        {activeTab === 'bookmarks' && (
          <Bookmarks 
            bookmarkedPosts={bookmarkedPosts} 
            onToggleBookmark={handleToggleBookmark} 
            onOpenProfile={handleOpenProfile} 
          />
        )}

        {activeTab === 'home' && (
          <>
            {/* Live Stories Banner */}
            <div style={{ display: 'flex', gap: '1rem', overflowX: 'auto', paddingBottom: '0.5rem', marginBottom: '1rem', alignItems: 'center' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <div style={{ width: 6, height: 6, borderRadius: '50%', backgroundColor: 'var(--accent-primary)' }}></div> LIVE & STORIES
              </div>
              <div style={{ marginLeft: 'auto', fontSize: '0.8rem', fontWeight: '600', cursor: 'pointer', color: 'var(--text-secondary)' }}>Explore all &rarr;</div>
            </div>

            <CreatePost onPostCreated={handleRefreshFeed} />
            
            {/* Feed Filter Tabs */}
            <div className="feed-tabs">
              {[
                { id: 'for-you', label: 'For You' },
                { id: 'following', label: 'Following' },
                { id: 'deep-dives', label: 'Deep Dives' },
                { id: 'tech-design', label: 'Tech & Design' },
                { id: 'essays', label: 'Essays' }
              ].map(tab => (
                <div 
                  key={tab.id}
                  className={`feed-tab ${activeFeedTab === tab.id ? 'active' : ''}`}
                  onClick={() => setActiveFeedTab(tab.id)}
                >
                  {tab.label}
                </div>
              ))}
            </div>

            <Feed 
              key={`${refreshKey}-${activeFeedTab}`} 
              userId={userId} 
              activeFeedTab={activeFeedTab}
              onOpenProfile={handleOpenProfile} 
              bookmarkedPostIds={bookmarkedPosts.map(p => p.post_id)}
              onToggleBookmark={handleToggleBookmark}
            />
          </>
        )}
      </main>

      <RightPanel onOpenProfile={handleOpenProfile} onTabChange={handleTabChange} />
      
      <div style={{ position: 'fixed', bottom: '20px', left: '20px', zIndex: 50 }}>
        <Notifications fullPage={false} onOpenProfile={handleOpenProfile} />
      </div>
    </div>
  );
}

export default App;
