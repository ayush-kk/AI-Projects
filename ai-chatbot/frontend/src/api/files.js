import client from './client';

export async function uploadFile(file, conversationId) {
  const formData = new FormData();
  formData.append('file', file);
  if (conversationId) {
    formData.append('conversation_id', conversationId);
  }
  const res = await client.post('/files/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}

export async function searchWeb(query) {
  const res = await client.post('/search', { query, max_results: 5 });
  return res.data;
}

export function getDownloadUrl(filename, userId) {
  return `/api/v1/documents/download/${filename}?user_id=${userId}`;
}
