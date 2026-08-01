import React, { createContext, useContext, useState, useEffect } from 'react';

const ChatContext = createContext();

export const useChat = () => useContext(ChatContext);

export const ChatProvider = ({ children }) => {
    const [conversations, setConversations] = useState([]);
    const [currentConversation, setCurrentConversation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    // Initialize with a default conversation if empty
    useEffect(() => {
        if (conversations.length === 0) {
            createNewConversation();
        }
    }, []);

    const createNewConversation = () => {
        const newConv = {
            id: Date.now().toString(),
            title: 'New Chat',
            messages: [{
                id: Date.now().toString() + '-init',
                role: 'assistant',
                content: 'Hello! I am TradePilot AI. How can I assist you with import/export compliance today?'
            }],
            context: {}
        };
        setConversations(prev => [newConv, ...prev]);
        setCurrentConversation(newConv);
    };

    const addMessage = (message) => {
        setCurrentConversation(prev => {
            if (!prev) return prev;
            const updated = {
                ...prev,
                messages: [...prev.messages, message]
            };
            
            // Update in conversations array
            setConversations(all => all.map(c => c.id === updated.id ? updated : c));
            return updated;
        });
    };

    const updateContext = (newContext) => {
        setCurrentConversation(prev => {
            if (!prev) return prev;
            const updated = {
                ...prev,
                context: { ...prev.context, ...newContext }
            };
            setConversations(all => all.map(c => c.id === updated.id ? updated : c));
            return updated;
        });
    };

    const selectConversation = (id) => {
        const conv = conversations.find(c => c.id === id);
        if (conv) {
            setCurrentConversation(conv);
            setError(null);
        }
    };

    const deleteConversation = (id) => {
        setConversations(prev => {
            const filtered = prev.filter(c => c.id !== id);
            if (currentConversation?.id === id) {
                if (filtered.length > 0) {
                    setCurrentConversation(filtered[0]);
                } else {
                    setCurrentConversation(null);
                }
            }
            return filtered;
        });
        if (conversations.length <= 1) {
            createNewConversation();
        }
    };

    const value = {
        conversations,
        currentConversation,
        isLoading,
        setIsLoading,
        error,
        setError,
        createNewConversation,
        addMessage,
        updateContext,
        selectConversation,
        deleteConversation
    };

    return (
        <ChatContext.Provider value={value}>
            {children}
        </ChatContext.Provider>
    );
};
