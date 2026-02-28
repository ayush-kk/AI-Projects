import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { HiOutlinePaperAirplane } from 'react-icons/hi2';
import VoiceButton from '../controls/VoiceButton';
import FileUpload from '../controls/FileUpload';
import useVoiceInput from '../../hooks/useVoiceInput';
import useFileUpload from '../../hooks/useFileUpload';
import { useChat } from '../../context/ChatContext';

export default function ChatInput({ onSend }) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);
  const { isStreaming, currentConversation } = useChat();
  const { isRecording, transcript, startRecording, stopRecording, clearTranscript } = useVoiceInput();
  const { files, uploading, handleUpload, clearFiles } = useFileUpload();

  useEffect(() => {
    if (transcript) {
      setText((prev) => (prev ? prev + ' ' + transcript : transcript));
      clearTranscript();
    }
  }, [transcript, clearTranscript]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [text]);

  const handleSubmit = () => {
    if (!text.trim() || isStreaming) return;
    onSend(text.trim());
    setText('');
    clearFiles();
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileUpload = (acceptedFiles) => {
    handleUpload(acceptedFiles, currentConversation?.id);
  };

  return (
    <div className="border-t border-slate-200 bg-white/80 backdrop-blur-lg p-3 sm:p-4">
      <div className="max-w-3xl mx-auto">
        <div className="flex items-end gap-2 bg-slate-50 rounded-2xl border border-slate-200 p-2 focus-within:border-indigo-300 focus-within:ring-2 focus-within:ring-indigo-100 transition-all">
          <FileUpload
            files={files}
            onUpload={handleFileUpload}
            uploading={uploading}
          />

          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message NexusAI..."
            rows={1}
            className="flex-1 resize-none bg-transparent border-0 focus:outline-none text-sm text-slate-800 placeholder-slate-400 py-2 px-1 max-h-[150px]"
          />

          <div className="flex items-center gap-1">
            <VoiceButton
              isRecording={isRecording}
              onStart={startRecording}
              onStop={stopRecording}
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSubmit}
              disabled={!text.trim() || isStreaming}
              className="p-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <HiOutlinePaperAirplane className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
        <p className="text-center text-xs text-slate-400 mt-2">
          NexusAI can make mistakes. Verify important information.
        </p>
      </div>
    </div>
  );
}
