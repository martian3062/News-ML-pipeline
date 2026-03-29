"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import api from "@/lib/api";

export default function VideoStudio() {
    const [status, setStatus] = useState<"idle" | "loading" | "complete" | "error">("idle");
    const [loadingMsg, setLoadingMsg] = useState("");
    const [videoUrl, setVideoUrl] = useState<string | null>(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [articleSlug, setArticleSlug] = useState("isro-successfully-tests-reusable-launch-vehicle-in-orbital-return-mission");

    const generateVideo = async () => {
        setStatus("loading");
        setLoadingMsg("Orchestrating AI Pipeline...");
        setVideoUrl(null);
        setErrorMessage("");

        const loadingSteps = [
            "Prompting Groq (Llama-3.3-70B) for Script Generation...",
            "Synthesizing Audio via Edge TTS...",
            "Gathering Contextual Pexels Stock Footage...",
            "Validating Frames via Llama-4-Scout Vision Model...",
            "Compositing Final Video with FFmpeg...",
            "Finalizing MP4 Render..."
        ];

        let i = 0;
        const interval = setInterval(() => {
            if (i < loadingSteps.length) {
                setLoadingMsg(loadingSteps[i]);
                i++;
            }
        }, 8000);

        try {
            const res = await api.post("/api/video-studio/generate/", { 
                article_slug: articleSlug 
            }, { timeout: 60000 }); // Longer timeout for video generation

            clearInterval(interval);
            
            if (res.data.video_url) {
                // Ensure the URL is absolute for the video player
                const baseUrl = api.defaults.baseURL || "";
                setVideoUrl(`${baseUrl}${res.data.video_url}`);
                setStatus("complete");
            } else {
                setErrorMessage("Failed to generate video.");
                setStatus("error");
            }
        } catch (error: any) {
            clearInterval(interval);
            console.error("Video Generation Error:", error);
            setErrorMessage(error.response?.data?.error || "Failed to connect to backend AI server.");
            setStatus("error");
        }
    };

    return (
        <main className="main-content" style={{ minHeight: '100vh', padding: '100px 24px 48px', position: 'relative', overflow: 'hidden' }}>
            {/* Background elements */}
            <div className="animate-float" style={{ position: 'absolute', top: '25%', left: '25%', width: '400px', height: '400px', background: 'var(--gradient-glow)', borderRadius: '50%', filter: 'blur(80px)', pointerEvents: 'none', opacity: 0.6 }} />

            <div className="container relative z-10" style={{ maxWidth: '1200px', margin: '0 auto' }}>
                <header style={{ marginBottom: '48px', textAlign: 'center' }}>
                    <h1 className="text-4xl" style={{ fontWeight: 800, marginBottom: '16px', letterSpacing: '-1px' }}>
                        News<span className="text-gradient">AI</span> Video Studio
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '18px', maxWidth: '600px', margin: '0 auto' }}>
                        Fully automated Broadcast Generator powered by Groq Text & Vision models natively composited in the backend.
                    </p>
                </header>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '32px' }}>
                    {/* Control Panel */}
                    <div className="glass-card" style={{ padding: '32px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: '400px' }}>
                        <div>
                            <h2 className="text-xl" style={{ fontWeight: 700, marginBottom: '24px', color: 'var(--text-primary)' }}>Pipeline Controls</h2>
                            
                            <div style={{ marginBottom: '32px' }}>
                                <label style={{ display: 'block', fontSize: '14px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>Target Article Slug</label>
                                <input 
                                    type="text"
                                    value={articleSlug}
                                    onChange={(e) => setArticleSlug(e.target.value)}
                                    className="glass-input" 
                                    style={{ width: '100%', wordBreak: 'break-all', outline: 'none' }}
                                    placeholder="Enter article-slug-here"
                                />
                            </div>

                            <button
                                onClick={generateVideo}
                                disabled={status === "loading"}
                                className={status === "loading" ? "btn-ghost" : "btn-primary"}
                                style={{ width: '100%', justifyContent: 'center', padding: '16px', fontSize: '16px' }}
                            >
                                {status === "loading" ? "Generators Active..." : "▶ Start AI Generation"}
                            </button>
                        </div>
                        
                        <div style={{ marginTop: '32px', fontSize: '12px', color: 'var(--text-tertiary)', borderTop: '1px solid var(--glass-border)', paddingTop: '16px' }}>
                            <p style={{ marginBottom: '8px' }}>⚡ Text Engine: <strong style={{ color: 'var(--accent-crimson)' }}>llama-4-scout-17b-16e-instruct</strong></p>
                            <p>👁 Vision Checks: <strong style={{ color: 'var(--accent-crimson)' }}>llama-4-scout-17b-16e-instruct</strong></p>
                        </div>
                    </div>

                    {/* Preview Player / Loading State */}
                    <div className="glass-card" style={{ gridColumn: 'span 2', minHeight: '500px', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden' }}>
                        {status === "idle" && (
                            <div style={{ textAlign: 'center', padding: '40px' }}>
                                <div style={{ fontSize: '64px', marginBottom: '16px', opacity: 0.8, filter: 'drop-shadow(0 4px 12px rgba(220, 38, 38, 0.2))' }}>🎬</div>
                                <h3 className="text-2xl" style={{ fontWeight: 600, marginBottom: '12px', color: 'var(--text-primary)' }}>Ready to Synthesize</h3>
                                <p style={{ color: 'var(--text-secondary)', maxWidth: '400px', margin: '0 auto', fontSize: '15px' }}>
                                    Click generate to extract the article script, download Pexels context, perform visual validation natively via Groq, and composite the final MP4.
                                </p>
                            </div>
                        )}

                        {status === "loading" && (
                            <motion.div 
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                style={{ textAlign: 'center', padding: '40px', width: '100%' }}
                            >
                                <div className="animate-pulse-glow" style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'var(--gradient-primary)', margin: '0 auto 32px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: 'var(--shadow-glow-crimson)' }}>
                                    <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'var(--glass-bg)' }} />
                                </div>
                                <h3 className="text-2xl" style={{ fontWeight: 600, marginBottom: '16px', color: 'var(--text-primary)' }}>{loadingMsg}</h3>
                                <p style={{ color: 'var(--text-secondary)' }}>Please wait. Groq LLMs & FFmpeg are running natively.</p>
                            </motion.div>
                        )}

                        {status === "error" && (
                            <div style={{ textAlign: 'center', padding: '40px' }}>
                                <div style={{ fontSize: '56px', marginBottom: '16px' }}>⚠️</div>
                                <h3 className="text-2xl" style={{ color: 'var(--accent-crimson)', fontWeight: 600, marginBottom: '12px' }}>Pipeline Failed</h3>
                                <p style={{ color: 'var(--text-secondary)' }}>{errorMessage}</p>
                            </div>
                        )}

                        {status === "complete" && videoUrl && (
                            <motion.div 
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}
                            >
                                <video 
                                    src={videoUrl || undefined}
                                    controls
                                    autoPlay
                                    preload="auto"
                                    playsInline
                                    style={{ width: '100%', height: '100%', objectFit: 'contain', maxHeight: '600px', background: 'rgba(0,0,0,0.05)' }}
                                />
                                <div style={{ position: 'absolute', top: '24px', right: '24px', background: 'var(--glass-bg)', backdropFilter: 'blur(12px)', padding: '6px 16px', borderRadius: '20px', fontSize: '12px', fontWeight: 700, color: 'var(--accent-crimson)', border: '1px solid var(--glass-border)', boxShadow: 'var(--shadow-sm)' }}>
                                    ● LIVE AI FEED
                                </div>
                            </motion.div>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
}
