import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { Bell, Heart, UserPlus, CheckCircle, MessageSquare } from 'lucide-react';

export default function Notifications({ fullPage = false, onOpenProfile }) {
  const [notifications, setNotifications] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchNotifications = async () => {
    try {
      const data = await api.getNotifications();
      setNotifications(data);
    } catch (err) {
      console.error('Failed to load notifications');
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await api.markNotificationsRead();
      setNotifications([]);
    } catch (err) {
      console.error(err);
    }
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  if (fullPage) {
    return (
      <div className="notifications-view animate-slide-up">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Bell size={24} style={{ color: 'var(--accent-primary)' }} /> Notifications
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.2rem' }}>
              {unreadCount} unread interaction{unreadCount === 1 ? '' : 's'}
            </p>
          </div>
          {unreadCount > 0 && (
            <button className="secondary" onClick={handleMarkAllRead} style={{ fontSize: '0.8rem', padding: '0.4rem 0.9rem' }}>
              <CheckCircle size={15} /> Mark All as Read
            </button>
          )}
        </div>

        {notifications.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem 1.5rem', color: 'var(--text-secondary)' }}>
            <Bell size={36} style={{ margin: '0 auto 1rem', opacity: 0.3 }} />
            <h3 style={{ fontSize: '1.1rem', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>All caught up!</h3>
            <p style={{ fontSize: '0.85rem' }}>
              When people like your publications or start following you, notifications will appear here.
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {notifications.map((notif) => {
              const isLike = notif.type === 'like';
              return (
                <div 
                  key={notif.notification_id} 
                  className="post-card"
                  style={{ 
                    padding: '1.1rem 1.25rem', 
                    display: 'flex', 
                    alignItems: 'flex-start', 
                    gap: '1rem',
                    borderLeft: notif.is_read ? undefined : '3px solid var(--accent-primary)'
                  }}
                >
                  <div style={{ 
                    width: '36px', 
                    height: '36px', 
                    borderRadius: '50%', 
                    backgroundColor: isLike ? '#FEE2E2' : '#EEF2FF', 
                    color: isLike ? '#EF4444' : 'var(--accent-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    {isLike ? <Heart size={18} fill="#EF4444" /> : <UserPlus size={18} />}
                  </div>

                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '0.95rem', color: 'var(--text-primary)', lineHeight: '1.4' }}>
                      <span style={{ fontWeight: '700' }}>Someone</span> {isLike ? 'liked your publication' : 'started following you'}
                    </div>

                    {notif.post_snippet && (
                      <div style={{ 
                        marginTop: '0.4rem', 
                        padding: '0.5rem 0.75rem', 
                        backgroundColor: 'var(--bg-tertiary)', 
                        borderRadius: '8px', 
                        fontSize: '0.82rem', 
                        color: 'var(--text-secondary)',
                        fontStyle: 'italic',
                        maxLines: 2,
                        overflow: 'hidden'
                      }}>
                        "{notif.post_snippet}"
                      </div>
                    )}

                    <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginTop: '0.35rem' }}>
                      {new Date(notif.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
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

  // Floating popover mode
  return (
    <div style={{ position: 'relative' }}>
      <button className="icon-btn" onClick={() => setIsOpen(!isOpen)} title="Quick Notifications">
        <Bell size={20} />
        {unreadCount > 0 && (
          <span className="badge">{unreadCount}</span>
        )}
      </button>

      {isOpen && (
        <div className="notifications-panel glass" style={{ width: '300px', maxHeight: '360px', overflowY: 'auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: '700' }}>Notifications</h3>
            {unreadCount > 0 && (
              <span 
                style={{ fontSize: '0.75rem', color: 'var(--accent-primary)', cursor: 'pointer', fontWeight: '600' }}
                onClick={handleMarkAllRead}
              >
                Mark read
              </span>
            )}
          </div>
          {notifications.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>No new notifications</p>
          ) : (
            notifications.map((notif) => (
              <div key={notif.notification_id} className="notification-item">
                <div style={{ fontSize: '0.85rem' }}>
                  Someone {notif.type}d your post!
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                  {new Date(notif.created_at).toLocaleDateString()}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
