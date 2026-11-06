import React, { useState } from 'react';
import { Users, MessageSquare, Compass, Check, ArrowRight } from 'lucide-react';

export default function Communities({ onOpenProfile }) {
  const [joinedCommunities, setJoinedCommunities] = useState({ 1: true, 3: true });
  const [filter, setFilter] = useState('all');

  const communities = [
    {
      id: 1,
      name: 'Relational Architects & 3NF',
      category: 'database',
      members: '3,840',
      description: 'Discourse on relational database theory, B-Tree index optimization, MariaDB storage engines, and high-concurrency schema design.',
      lead: 'marcus_thorne',
      leadId: 4,
      discussions: 142
    },
    {
      id: 2,
      name: 'Brutalist Web & Editorial UI',
      category: 'design',
      members: '6,210',
      description: 'Challenging homogenized web aesthetics. Raw typography grids, intentional friction, monospaced accents, and tactile design tokens.',
      lead: 'elena_rostova',
      leadId: 3,
      discussions: 289
    },
    {
      id: 3,
      name: 'Autonomous Agent Networks',
      category: 'ai',
      members: '4,150',
      description: 'Investigating deterministic consensus, multi-agent code orchestration, and computational sociology in generative models.',
      lead: 'ananya_sen',
      leadId: 7,
      discussions: 198
    },
    {
      id: 4,
      name: 'Tactile Controls & Hardware Cabins',
      category: 'design',
      members: '2,940',
      description: 'Physical dial interfaces, micro-spring haptics, and automotive ergonomics in modern digital-physical cockpits.',
      lead: 'selah_kim',
      leadId: 5,
      discussions: 95
    },
    {
      id: 5,
      name: 'Distributed Systems & SRE',
      category: 'infrastructure',
      members: '5,100',
      description: 'Linux kernel tuning, socket connection pooling, containerized schema migrations, and zero-downtime reliability.',
      lead: 'dev_arjun',
      leadId: 8,
      discussions: 214
    }
  ];

  const filteredCommunities = filter === 'all' 
    ? communities 
    : communities.filter(c => c.category === filter);

  const toggleJoin = (id) => {
    setJoinedCommunities(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  return (
    <div className="communities-view animate-slide-up">
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Compass size={24} style={{ color: 'var(--accent-primary)' }} /> Communities & Guilds
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          Explore curated focus guilds and deep dive into specialized technical discourse.
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="feed-tabs" style={{ marginBottom: '1.5rem' }}>
        {['all', 'database', 'design', 'ai', 'infrastructure'].map((cat) => (
          <div 
            key={cat} 
            className={`feed-tab ${filter === cat ? 'active' : ''}`}
            onClick={() => setFilter(cat)}
            style={{ textTransform: 'capitalize' }}
          >
            {cat === 'all' ? 'All Guilds' : cat}
          </div>
        ))}
      </div>

      {/* Communities Grid */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filteredCommunities.map((c) => (
          <div key={c.id} className="post-card" style={{ padding: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                  {c.name}
                </h3>
                <div style={{ display: 'flex', gap: '1rem', fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                    <Users size={14} /> {c.members} members
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                    <MessageSquare size={14} /> {c.discussions} threads
                  </span>
                </div>
              </div>
              <button 
                className={joinedCommunities[c.id] ? 'secondary' : 'primary'}
                onClick={() => toggleJoin(c.id)}
                style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
              >
                {joinedCommunities[c.id] ? <><Check size={14} /> Joined</> : 'Join Guild'}
              </button>
            </div>

            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.5', marginBottom: '1rem' }}>
              {c.description}
            </p>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-color)', paddingTop: '0.75rem', fontSize: '0.8rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ color: 'var(--text-tertiary)' }}>Guild Lead:</span>
                <span 
                  className="author-clickable" 
                  style={{ fontWeight: '600' }}
                  onClick={() => onOpenProfile && onOpenProfile(c.leadId)}
                >
                  @{c.lead}
                </span>
              </div>
              <span style={{ color: 'var(--accent-primary)', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                Enter Discussions <ArrowRight size={14} />
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
