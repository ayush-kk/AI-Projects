import { createContext, useContext, useState, useCallback } from 'react';
import {
  getConversations as apiGetConversations,
  createConversation as apiCreateConversation,
  getConversation as apiGetConversation,
  deleteConversation as apiDeleteConversation,
} from '../api/chat';
import { getModels as apiGetModels } from '../api/models';

const ChatContext = createContext(null);

export function ChatProvider({ children }) {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [availableModels, setAvailableModels] = useState([]);
  const [searchEnabled, setSearchEnabled] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');

  const loadConversations = useCallback(async () => {
    try {
      const data = await apiGetConversations();
      setConversations(data);
    } catch (err) {
      console.error('Failed to load conversations:', err);
    }
  }, []);

  const loadModels = useCallback(async () => {
    try {
      const data = await apiGetModels();
      setAvailableModels(data.models || []);
      if (data.models?.length > 0 && !selectedModel) {
        setSelectedModel(data.models[0].id);
      }
    } catch (err) {
      console.error('Failed to load models:', err);
    }
  }, [selectedModel]);

  const selectConversation = useCallback(async (id) => {
    try {
      const data = await apiGetConversation(id);
      setCurrentConversation(data);
      setMessages(data.messages || []);
    } catch (err) {
      console.error('Failed to load conversation:', err);
    }
  }, []);

  const createNewConversation = useCallback(async () => {
    try {
      const data = await apiCreateConversation('New Chat', selectedModel);
      setConversations((prev) => [data, ...prev]);
      setCurrentConversation(data);
      setMessages([]);
      return data;
    } catch (err) {
      console.error('Failed to create conversation:', err);
      return null;
    }
  }, [selectedModel]);

  const removeConversation = useCallback(async (id) => {
    try {
      await apiDeleteConversation(id);
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (currentConversation?.id === id) {
        setCurrentConversation(null);
        setMessages([]);
      }
    } catch (err) {
      console.error('Failed to delete conversation:', err);
    }
  }, [currentConversation]);

  const addMessage = useCallback((message) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  const toggleSearch = useCallback(() => {
    setSearchEnabled((prev) => !prev);
  }, []);

  return (
    <ChatContext.Provider
      value={{
        conversations,
        currentConversation,
        messages,
        selectedModel,
        availableModels,
        searchEnabled,
        isStreaming,
        streamingMessage,
        setSelectedModel,
        setIsStreaming,
        setStreamingMessage,
        setCurrentConversation,
        setMessages,
        setConversations,
        loadConversations,
        loadModels,
        selectConversation,
        createNewConversation,
        removeConversation,
        addMessage,
        toggleSearch,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (!context) throw new Error('useChat must be used within ChatProvider');
  return context;
}
