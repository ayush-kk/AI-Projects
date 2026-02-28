import { useState, useCallback } from 'react';
import { uploadFile } from '../api/files';
import toast from 'react-hot-toast';

export default function useFileUpload() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleUpload = useCallback(async (acceptedFiles, conversationId) => {
    setUploading(true);
    const uploaded = [];
    for (const file of acceptedFiles) {
      try {
        const result = await uploadFile(file, conversationId);
        uploaded.push(result);
        toast.success(`${file.name} uploaded`);
      } catch (err) {
        toast.error(`Failed to upload ${file.name}`);
      }
    }
    setFiles((prev) => [...prev, ...uploaded]);
    setUploading(false);
    return uploaded;
  }, []);

  const clearFiles = useCallback(() => setFiles([]), []);

  return { files, uploading, handleUpload, clearFiles };
}
