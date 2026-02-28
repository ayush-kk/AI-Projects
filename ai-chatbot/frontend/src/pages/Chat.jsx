import { useEffect, useCallback, useRef } from 'react';
import MainLayout from '../components/layout/MainLayout';
import ChatWindow from '../components/chat/ChatWindow';
import { useChat } from '../context/ChatContext';
import useWebSocket from '../hooks/useWebSocket';

export default function Chat() {
  const {
    currentConversation,
    selectedModel,
    searchEnabled,
    addMessage,
    createNewConversation,
    loadConversations,
    setCurrentConversation,
  } = useChat();
  const { connect, sendMessage, disconnect } = useWebSocket();
  const wsConnected = useRef(false);

  useEffect(() => {
    if (!wsConnected.current) {
      connect();
      wsConnected.current = true;
    }
    return () => {
      disconnect();
      wsConnected.current = false;
    };
  }, [connect, disconnect]);

  const handleSendMessage = useCallback(
    async (text) => {
      let convId = currentConversation?.id;

      if (!convId) {
        const newConv = await createNewConversation();
        if (!newConv) return;
        convId = newConv.id;
      }

      addMessage({
        id: Date.now(),
        role: 'user',
        content: text,
        created_at: new Date().toISOString(),
      });

      sendMessage({
        conversation_id: convId,
        message: text,
        model: selectedModel,
        search_enabled: searchEnabled,
      });

      loadConversations();
    },
    [currentConversation, selectedModel, searchEnabled, addMessage, sendMessage, createNewConversation, loadConversations]
  );

  return (
    <MainLayout>
      <ChatWindow onSendMessage={handleSendMessage} />
    </MainLayout>
  );
}
