import client from './client';

export async function getModels() {
  const res = await client.get('/models');
  return res.data;
}

export async function refreshOllamaModels() {
  const res = await client.get('/models/ollama/refresh');
  return res.data;
}
