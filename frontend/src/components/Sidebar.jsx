import React from 'react';
import { Home, Bell, MessageSquare, Bookmark, User, Edit3, LogOut, Compass } from 'lucide-react';

export default function Sidebar({ activeTab, onLogout, onTabChange, currentUsername }) {
  const displayName = currentUsername || 'My Profile';

  return (
    <aside className="sidebar">
      <div className="brand" onClick={() => onTabChange('home')} style={{ cursor: 'pointer' }}>
        <div className="brand-dot"></div>
        Kinetic
      </div>

      <button className="primary" style={{ marginBottom: '2rem', width: '100%' }} onClick={() => onTabChange('home')}>
        <Edit3 size={18} /> New Post
      </button>

      <nav className="nav-menu">
        <button 
          className={`nav-item ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => onTabChange('home')}
        >
          <Home size={20} /> Home
        </button>
        <button 
          className={`nav-item ${activeTab === 'communities' ? 'active' : ''}`}
          onClick={() => onTabChange('communities')}
        >
          <Compass size={20} /> Communities
        </button>
        <button 
          className={`nav-item ${activeTab === 'notifications' ? 'active' : ''}`}
          onClick={() => onTabChange('notifications')}
        >
          <Bell size={20} /> Notifications
        </button>
        <button 
          className={`nav-item ${activeTab === 'messages' ? 'active' : ''}`}
          onClick={() => onTabChange('messages')}
        >
          <MessageSquare size={20} /> Messages
        </button>
        <button 
          className={`nav-item ${activeTab === 'bookmarks' ? 'active' : ''}`}
          onClick={() => onTabChange('bookmarks')}
        >
          <Bookmark size={20} /> Bookmarks
        </button>
        <button 
          className={`nav-item ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => onTabChange('profile')}
        >
          <User size={20} /> Profile
        </button>
      </nav>

      <div 
        className="user-profile-badge" 
        onClick={() => onTabChange('profile')}
        style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <img src={`https://ui-avatars.com/api/?name=${displayName}&background=random`} className="avatar" alt="Avatar" />
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontWeight: '600', fontSize: '0.85rem' }}>{displayName}</span>
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.72rem' }}>View Profile</span>
          </div>
        </div>
        <button 
          onClick={(e) => { e.stopPropagation(); onLogout(); }}
          style={{ background: 'transparent', padding: '0.4rem', color: 'var(--text-secondary)' }}
          title="Log Out"
        >
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
}
