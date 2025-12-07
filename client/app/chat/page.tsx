"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Send, Bot, User, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api-client";

interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: Date;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: "welcome",
            role: "assistant",
            content:
                "Hello! I'm your AI assistant for this codebase. Ask me anything about the repository structure, code patterns, or how specific features work!",
            timestamp: new Date(),
        },
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: "user",
            content: input,
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);

        try {
            const response = await api.post<{ response: string }>("/api/chat", {
                message: input,
                history: messages.map((m) => ({
                    role: m.role,
                    content: m.content,
                })),
            });

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: "assistant",
                content: response.data.response,
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            console.error("Chat error:", error);
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: "assistant",
                content:
                    "Sorry, I encountered an error. Please try again or rephrase your question.",
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            {/* Header */}
            <header className="flex h-14 w-full items-center justify-between border-b border-gray-200 px-6 lg:px-12 bg-white">
                <div className="flex items-center gap-3">
                    <Link href="/dashboard" className="flex items-center gap-3">
                        <div className="grid grid-cols-3 gap-1 w-6 h-6">
                            {[...Array(9)].map((_, i) => (
                                <div
                                    key={i}
                                    className={`w-1 h-1 rounded-full ${i % 2 === 0 ? "bg-black" : "bg-gray-400"
                                        }`}
                                />
                            ))}
                        </div>
                        <span className="text-xl font-semibold tracking-tight text-black">
                            Grokboard
                        </span>
                    </Link>
                </div>

                <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
                    <Link
                        href="/dashboard"
                        className="hover:text-black transition-colors"
                    >
                        Dashboard
                    </Link>
                    <Link href="/codebase" className="hover:text-black transition-colors">
                        Codebase
                    </Link>
                    <Link href="/chat" className="text-black">
                        Chat
                    </Link>
                </nav>

                <div className="w-8" /> {/* Spacer for alignment */}
            </header>

            {/* Main Content */}
            <main className="flex-1 max-w-4xl mx-auto w-full px-6 lg:px-12 py-8 flex flex-col">
                {/* Back Link */}
                <Link
                    href="/dashboard"
                    className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-black transition-colors mb-6"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Dashboard
                </Link>

                {/* Page Header */}
                <div className="mb-6">
                    <h1 className="text-3xl font-semibold text-black mb-2">
                        AI Assistant
                    </h1>
                    <p className="text-gray-600">
                        Ask questions about the codebase and get intelligent answers
                    </p>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 bg-white border border-gray-200 rounded-xl overflow-hidden flex flex-col">
                    <div className="flex-1 overflow-y-auto p-6 space-y-4">
                        {messages.map((message) => (
                            <div
                                key={message.id}
                                className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"
                                    }`}
                            >
                                {message.role === "assistant" && (
                                    <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0">
                                        <Bot className="w-5 h-5 text-purple-600" />
                                    </div>
                                )}

                                <div
                                    className={`max-w-[70%] rounded-2xl px-4 py-3 ${message.role === "user"
                                            ? "bg-black text-white"
                                            : "bg-gray-100 text-gray-900"
                                        }`}
                                >
                                    <p className="text-sm whitespace-pre-wrap">
                                        {message.content}
                                    </p>
                                    <span className="text-xs opacity-60 mt-1 block">
                                        {message.timestamp.toLocaleTimeString([], {
                                            hour: "2-digit",
                                            minute: "2-digit",
                                        })}
                                    </span>
                                </div>

                                {message.role === "user" && (
                                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
                                        <User className="w-5 h-5 text-gray-600" />
                                    </div>
                                )}
                            </div>
                        ))}

                        {isLoading && (
                            <div className="flex gap-3 justify-start">
                                <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0">
                                    <Bot className="w-5 h-5 text-purple-600" />
                                </div>
                                <div className="bg-gray-100 rounded-2xl px-4 py-3">
                                    <Loader2 className="w-5 h-5 text-gray-600 animate-spin" />
                                </div>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Form */}
                    <form
                        onSubmit={handleSubmit}
                        className="border-t border-gray-200 p-4 flex gap-2"
                    >
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask about the codebase..."
                            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
                            disabled={isLoading}
                        />
                        <Button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="bg-black hover:bg-gray-800 text-white px-6"
                        >
                            {isLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <Send className="w-5 h-5" />
                            )}
                        </Button>
                    </form>
                </div>
            </main>
        </div>
    );
}
