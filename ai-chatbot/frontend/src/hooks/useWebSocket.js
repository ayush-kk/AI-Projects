import { useRef, useCallback } from 'react';
import { WS_BASE } from '../utils/constants';
import { useChat } from '../context/ChatContext';

export default function useWebSocket() {
  const wsRef = useRef(null);
  const { setIsStreaming, setStreamingMessage, addMessage, setConversations, setCurrentConversation } = useChat();

  const connect = useCallback(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    const ws = new WebSocket(`${WS_BASE}/ws/chat`);
    wsRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({ token }));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case 'connected':
          break;
        case 'start':
          setIsStreaming(true);
          setStreamingMessage('');
          break;
        case 'token':
          setStreamingMessage((prev) => prev + data.content);
          break;
        case 'complete':
          setIsStreaming(false);
          setStreamingMessage((prev) => {
            if (prev) {
              addMessage({
                id: data.message_id,
                role: 'assistant',
                content: prev,
                created_at: new Date().toISOString(),
              });
            }
            return '';
          });
          if (data.conversation_id) {
            setCurrentConversation((prev) =>
              prev ? { ...prev, id: data.conversation_id } : prev
            );
          }
          break;
        case 'error':
          setIsStreaming(false);
          setStreamingMessage('');
          console.error('WS error:', data.message);
          break;
        default:
          break;
      }
    };

    ws.onclose = () => {
      setTimeout(() => {
        if (wsRef.current === ws) connect();
      }, 3000);
    };

    ws.onerror = () => ws.close();

    return ws;
  }, [setIsStreaming, setStreamingMessage, addMessage, setConversations, setCurrentConversation]);

  const sendMessage = useCallback((payload) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'chat_message', ...payload }));
    }
  }, []);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  return { connect, sendMessage, disconnect, wsRef };
}
