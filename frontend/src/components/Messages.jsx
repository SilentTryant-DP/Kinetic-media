import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { Send, User, MessageSquare } from 'lucide-react';

export default function Messages({ onOpenProfile }) {
  const [contacts, setContacts] = useState([]);
  const [activeContact, setActiveContact] = useState(null);
  const [messages, setMessages] = useState({});
  const [inputMessage, setInputMessage] = useState('');

  useEffect(() => {
    loadContacts();
  }, []);

  const loadContacts = async () => {
    try {
      const users = await api.getUsers();
      const currentUserId = parseInt(localStorage.getItem('userId'), 10);
      const others = users.filter(u => u.user_id !== currentUserId);
      setContacts(others);
      if (others.length > 0) {
        setActiveContact(others[0]);
        // Seed default initial chat histories
        setMessages({
          [others[0].user_id]: [
            { sender: 'them', text: `Hi! Loved your update on the MariaDB 3NF schema architecture.`, time: '10:14 AM' },
            { sender: 'me', text: 'Thanks! The composite indexes helped reduce latency by over 80%.', time: '10:16 AM' }
          ]
        });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || !activeContact) return;

    const contactId = activeContact.user_id;
    const currentList = messages[contactId] || [];
    const newMsg = {
      sender: 'me',
      text: inputMessage.trim(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages({
      ...messages,
      [contactId]: [...currentList, newMsg]
    });
    setInputMessage('');
  };

  return (
    <div className="messages-view animate-slide-up">
      <div style={{ marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <MessageSquare size={24} style={{ color: 'var(--accent-primary)' }} /> Direct Messages
        </h2>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: '1rem', height: '620px', background: 'var(--bg-secondary)', borderRadius: '16px', border: '1px solid var(--border-color)', overflow: 'hidden' }}>
        {/* Contact List */}
        <div style={{ borderRight: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', background: 'var(--bg-primary)' }}>
          <div style={{ padding: '1rem', fontWeight: '700', fontSize: '0.9rem', borderBottom: '1px solid var(--border-color)' }}>
            Contacts ({contacts.length})
          </div>
          <div style={{ overflowY: 'auto', flex: 1 }}>
            {contacts.map((contact) => {
              const isSelected = activeContact?.user_id === contact.user_id;
              return (
                <div 
                  key={contact.user_id} 
                  onClick={() => setActiveContact(contact)}
                  style={{ 
                    padding: '0.75rem 1rem', 
                    cursor: 'pointer', 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '0.6rem',
                    backgroundColor: isSelected ? 'var(--bg-secondary)' : 'transparent',
                    borderLeft: isSelected ? '3px solid var(--accent-primary)' : '3px solid transparent'
                  }}
                >
                  <img 
                    src={`https://ui-avatars.com/api/?name=${contact.username}&background=random`} 
                    style={{ width: '32px', height: '32px', borderRadius: '50%' }} 
                    alt={contact.username} 
                  />
                  <div style={{ overflow: 'hidden' }}>
                    <div style={{ fontWeight: '600', fontSize: '0.85rem', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                      {contact.username}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.72rem', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                      {contact.bio || `@${contact.username}`}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Chat Thread */}
        {activeContact ? (
          <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            {/* Thread Header */}
            <div style={{ padding: '0.85rem 1.25rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <img 
                  src={`https://ui-avatars.com/api/?name=${activeContact.username}&background=random`} 
                  style={{ width: '36px', height: '36px', borderRadius: '50%' }} 
                  alt={activeContact.username} 
                />
                <div>
                  <div style={{ fontWeight: '700', fontSize: '0.95rem' }}>{activeContact.username}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem' }}>@{activeContact.username}</div>
                </div>
              </div>
              <button 
                className="secondary" 
                onClick={() => onOpenProfile && onOpenProfile(activeContact.user_id)}
                style={{ fontSize: '0.8rem', padding: '0.35rem 0.8rem' }}
              >
                <User size={14} /> View Profile
              </button>
            </div>

            {/* Messages Body */}
            <div style={{ flex: 1, padding: '1.25rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {(messages[activeContact.user_id] || []).length === 0 ? (
                <div style={{ textAlign: 'center', color: 'var(--text-tertiary)', marginTop: '2rem', fontSize: '0.9rem' }}>
                  No messages yet. Send a greeting to start discourse!
                </div>
              ) : (
                (messages[activeContact.user_id] || []).map((msg, idx) => (
                  <div 
                    key={idx} 
                    style={{ 
                      alignSelf: msg.sender === 'me' ? 'flex-end' : 'flex-start',
                      maxWidth: '75%',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: msg.sender === 'me' ? 'flex-end' : 'flex-start'
                    }}
                  >
                    <div style={{ 
                      backgroundColor: msg.sender === 'me' ? 'var(--accent-primary)' : 'var(--bg-tertiary)',
                      color: msg.sender === 'me' ? '#FFFFFF' : 'var(--text-primary)',
                      padding: '0.65rem 1rem',
                      borderRadius: msg.sender === 'me' ? '14px 14px 2px 14px' : '14px 14px 14px 2px',
                      fontSize: '0.9rem',
                      lineHeight: '1.4'
                    }}>
                      {msg.text}
                    </div>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', marginTop: '0.2rem', padding: '0 0.2rem' }}>
                      {msg.time}
                    </span>
                  </div>
                ))
              )}
            </div>

            {/* Input Bar */}
            <form onSubmit={handleSendMessage} style={{ padding: '0.85rem 1.25rem', borderTop: '1px solid var(--border-color)', display: 'flex', gap: '0.5rem' }}>
              <input 
                type="text" 
                placeholder={`Message @${activeContact.username}...`}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                style={{ flex: 1, padding: '0.65rem 1rem', borderRadius: '9999px', border: '1px solid var(--border-color)', fontSize: '0.9rem' }}
              />
              <button type="submit" className="primary" style={{ borderRadius: '50%', width: '40px', height: '40px', padding: 0 }}>
                <Send size={16} />
              </button>
            </form>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
            Select a contact to view discourse.
          </div>
        )}
      </div>
    </div>
  );
}
