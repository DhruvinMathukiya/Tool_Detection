import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Upload, Camera, LayoutDashboard, Image as ImageIcon, Video } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [detectionResult, setDetectionResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [streamData, setStreamData] = useState({ image: null, count: 0 });
  
  const [isStreaming, setIsStreaming] = useState(false);
  const eventSourceRef = useRef(null);

  // Handle Real-time SSE Connection
  useEffect(() => {
    if (activeTab === 'realtime' && isStreaming) {
      const eventSource = new EventSource(`${API_BASE_URL}/stream`);
      
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setStreamData(data);
      };

      eventSource.onerror = (err) => {
        console.error("SSE Error:", err);
        setIsStreaming(false);
        eventSource.close();
      };

      eventSourceRef.current = eventSource;
    } else {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    }

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [activeTab, isStreaming]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewImage(URL.createObjectURL(file));
      setDetectionResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/detect`, formData);
      setDetectionResult(response.data);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Error uploading image");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-2">
          <LayoutDashboard className="text-blue-600" size={28} />
          <h1 className="text-xl font-bold tracking-tight">Detection Dashboard</h1>
        </div>
        <div className="flex gap-4">
          <button 
            onClick={() => setActiveTab('upload')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 ${activeTab === 'upload' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            <ImageIcon size={18} /> Upload Image
          </button>
          <button 
            onClick={() => setActiveTab('realtime')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 ${activeTab === 'realtime' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            <Video size={18} /> Real-time
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto p-8">
        {activeTab === 'upload' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Upload Section */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Upload size={20} className="text-blue-500" /> Upload Image
              </h2>
              <div className="border-2 border-dashed border-gray-200 rounded-xl p-8 flex flex-col items-center justify-center bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer relative">
                <input 
                  type="file" 
                  onChange={handleFileChange} 
                  className="absolute inset-0 opacity-0 cursor-pointer"
                  accept="image/*"
                />
                {previewImage ? (
                  <img src={previewImage} alt="Preview" className="max-h-64 rounded-lg shadow-md" />
                ) : (
                  <>
                    <ImageIcon size={48} className="text-gray-400 mb-3" />
                    <p className="text-gray-500 text-sm">Click or drag image to upload</p>
                  </>
                )}
              </div>
              <button 
                onClick={handleUpload}
                disabled={!selectedFile || isLoading}
                className="w-full mt-6 bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-200"
              >
                {isLoading ? 'Processing...' : 'Run Detection'}
              </button>
            </div>

            {/* Result Section */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col">
              <h2 className="text-lg font-semibold mb-4">Detection Result</h2>
              {detectionResult ? (
                <div className="flex flex-col flex-1">
                  <div className="relative rounded-xl overflow-hidden shadow-inner bg-black flex items-center justify-center min-h-[300px]">
                    <img src={detectionResult.image} alt="Result" className="max-w-full h-auto" />
                  </div>
                  <div className="mt-4 p-4 bg-blue-50 rounded-xl border border-blue-100">
                    <p className="text-blue-800 font-bold text-xl">
                      Detected Objects: {detectionResult.count}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="flex-1 border-2 border-gray-100 rounded-xl border-dashed flex items-center justify-center text-gray-400 italic">
                  Run detection to see results
                </div>
              )}
            </div>
          </div>
        ) : (
          /* Real-time Section */
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <Camera size={24} className="text-red-500 animate-pulse" /> Live Detection Stream
              </h2>
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setIsStreaming(!isStreaming)}
                  className={`px-6 py-2 rounded-xl font-bold transition-all shadow-md ${
                    isStreaming 
                    ? 'bg-red-500 text-white hover:bg-red-600' 
                    : 'bg-green-500 text-white hover:bg-green-600'
                  }`}
                >
                  {isStreaming ? 'Stop Streaming' : 'Start Streaming'}
                </button>
                <div className={`px-4 py-2 rounded-full text-sm font-bold flex items-center gap-2 ${
                  isStreaming ? 'bg-red-50 text-red-700' : 'bg-gray-100 text-gray-500'
                }`}>
                  <span className={`w-2 h-2 rounded-full ${isStreaming ? 'bg-red-600 animate-ping' : 'bg-gray-400'}`}></span>
                  {isStreaming ? 'LIVE' : 'OFFLINE'}
                </div>
              </div>
            </div>
            
            <div className="relative aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl flex items-center justify-center">
              {!isStreaming ? (
                <div className="text-gray-500 flex flex-col items-center gap-2">
                  <Video size={48} className="opacity-20" />
                  <p>Click "Start Streaming" to begin</p>
                </div>
              ) : streamData.image ? (
                <img src={streamData.image} alt="Live Stream" className="w-full h-full object-contain" />
              ) : (
                <div className="text-white flex flex-col items-center gap-4">
                  <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin"></div>
                  <p className="text-gray-400">Initializing camera and model...</p>
                </div>
              )}
              
              {streamData.image && isStreaming && (
                <div className="absolute bottom-6 left-6 bg-black/60 backdrop-blur-md px-6 py-3 rounded-xl border border-white/20">
                  <p className="text-white font-bold text-lg">
                    Current Count: {streamData.count}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
      
      {/* <footer className="mt-auto py-8 text-center text-gray-400 text-sm">
        &copy; 2026 Tool Detection System • Powered by YOLOv8 & FastAPI
      </footer> */}
    </div>
  );
}

export default App;
