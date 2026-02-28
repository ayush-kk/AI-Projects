import client from './client';

export async function getConversations() {
  const res = await client.get('/chat/conversations');
  return res.data;
}

export async function createConversation(title, modelName) {
  const res = await client.post('/chat/conversations', {
    title,
    model_name: modelName,
  });
  return res.data;
}

export async function getConversation(id) {
  const res = await client.get(`/chat/conversations/${id}`);
  return res.data;
}

export async function deleteConversation(id) {
  await client.delete(`/chat/conversations/${id}`);
}

export async function updateConversation(id, title) {
  const res = await client.patch(`/chat/conversations/${id}`, { title });
  return res.data;
}

export async function sendMessage(conversationId, message, model, searchEnabled) {
  const res = await client.post(`/chat/conversations/${conversationId}/messages`, {
    message,
    model,
    search_enabled: searchEnabled,
  });
  return res.data;
}
