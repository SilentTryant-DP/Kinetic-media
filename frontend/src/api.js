const API_URL = 'http://localhost:3000';

const request = async (endpoint, options = {}) => {
  const userId = localStorage.getItem('userId');
  const headers = {
    'Content-Type': 'application/json',
    ...(userId ? { 'x-user-id': userId } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Something went wrong');
  }

  return response.json();
};

export const api = {
  login: (data) => request('/login', { method: 'POST', body: JSON.stringify(data) }),
  register: (data) => request('/register', { method: 'POST', body: JSON.stringify(data) }),
  getFeed: () => request('/feed'),
  createPost: (data) => request('/posts', { method: 'POST', body: JSON.stringify(data) }),
  likePost: (id) => request(`/posts/${id}/like`, { method: 'POST' }),
  unlikePost: (id) => request(`/posts/${id}/like`, { method: 'DELETE' }),
  getNotifications: () => request('/notifications'),
  followUser: (id) => request(`/users/${id}/follow`, { method: 'POST' }),
  unfollowUser: (id) => request(`/users/${id}/follow`, { method: 'DELETE' }),
  getUsers: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/users${query ? `?${query}` : ''}`);
  },
  getUserProfile: (id) => request(`/users/${id}`),
  getUserPosts: (id) => request(`/users/${id}/posts`),
  getFollowers: (id) => request(`/users/${id}/followers`),
  getFollowing: (id) => request(`/users/${id}/following`),
  markNotificationsRead: () => request('/notifications/mark-read', { method: 'PUT' }),
  updateBio: (bio) => request('/users/profile', { method: 'PUT', body: JSON.stringify({ bio }) })
};
