"use client";

import { Play } from "lucide-react";
import { useState } from "react";

interface ActivityVideoProps {
  videoUrl: string;
  title: string;
}

export default function ActivityVideo({ videoUrl, title }: ActivityVideoProps) {
  const [showVideo, setShowVideo] = useState(false);

  // Extract YouTube video ID if YouTube URL
  const getYouTubeId = (url: string) => {
    const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&]+)/);
    return match ? match[1] : null;
  };

  const youtubeId = getYouTubeId(videoUrl);

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">Preview</h2>
      <div className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden">
        {showVideo ? (
          youtubeId ? (
            <iframe
              src={`https://www.youtube.com/embed/${youtubeId}`}
              title={title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="w-full h-full"
            />
          ) : (
            <video src={videoUrl} controls className="w-full h-full">
              Your browser does not support the video tag.
            </video>
          )
        ) : (
          <button
            onClick={() => setShowVideo(true)}
            className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 hover:bg-opacity-50 transition-all group"
          >
            <div className="bg-white rounded-full p-4 group-hover:scale-110 transition-transform">
              <Play className="w-12 h-12 text-primary fill-primary" />
            </div>
          </button>
        )}
      </div>
    </div>
  );
}
