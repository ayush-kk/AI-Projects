import { useEffect } from 'react';
import { useChat } from '../../context/ChatContext';

export default function ModelSelector() {
  const { availableModels, selectedModel, setSelectedModel, loadModels } = useChat();

  useEffect(() => {
    loadModels();
  }, [loadModels]);

  const ollamaModels = availableModels.filter((m) => m.provider === 'ollama');
  const groqModels = availableModels.filter((m) => m.provider === 'groq');

  return (
    <select
      value={selectedModel}
      onChange={(e) => setSelectedModel(e.target.value)}
      className="text-xs px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent max-w-[180px] cursor-pointer"
    >
      {groqModels.length > 0 && (
        <optgroup label="Cloud (Groq)">
          {groqModels.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </optgroup>
      )}
      {ollamaModels.length > 0 && (
        <optgroup label="Local (Ollama)">
          {ollamaModels.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </optgroup>
      )}
      {availableModels.length === 0 && <option value="">No models available</option>}
    </select>
  );
}
