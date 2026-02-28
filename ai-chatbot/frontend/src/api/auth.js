import client from './client';

export async function login(username, password) {
  const res = await client.post('/auth/login', { username, password });
  return res.data;
}

export async function register(username, password) {
  const res = await client.post('/auth/register', { username, password });
  return res.data;
}

export async function getMe() {
  const res = await client.get('/auth/me');
  return res.data;
}
