import { motion } from 'framer-motion';
import { HiOutlineMicrophone } from 'react-icons/hi2';

export default function VoiceButton({ isRecording, onStart, onStop }) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={isRecording ? onStop : onStart}
      className={`p-2 rounded-xl transition-all ${
        isRecording
          ? 'bg-red-500 text-white shadow-lg shadow-red-200'
          : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700'
      }`}
      title={isRecording ? 'Stop recording' : 'Voice input'}
    >
      <HiOutlineMicrophone className="w-5 h-5" />
      {isRecording && (
        <motion.div
          className="absolute inset-0 rounded-xl border-2 border-red-400"
          animate={{ scale: [1, 1.3, 1], opacity: [1, 0, 1] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        />
      )}
    </motion.button>
  );
}
