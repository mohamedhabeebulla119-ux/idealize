import React, { useState, useRef, useEffect } from 'react';
import { Send, Plus, Trash2, Menu, X } from 'lucide-react';
import { useChat } from '../context/ChatContext';
import { chatService } from '../services/chatService';
import '../styles/Chat.css';

const Chat = () => {
    const {
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
        deleteConversation,
    } = useChat();

    const [inputValue, setInputValue] = useState('');
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const messagesEndRef = useRef(null);

    // Auto-scroll to latest message
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [currentConversation?.messages]);

    // Initialize with a new conversation on first load
    useEffect(() => {
        if (!currentConversation && conversations.length === 0) {
            createNewConversation();
        }
    }, []);

    const handleSendMessage = async (e) => {
        e.preventDefault();

        if (!inputValue.trim()) return;
        if (!currentConversation) {
            createNewConversation();
            return;
        }

        // Add user message
        const userMessage = {
            id: Date.now().toString(),
            role: 'user',
            content: inputValue,
            timestamp: new Date().toISOString(),
        };

        addMessage(userMessage);
        setInputValue('');
        setIsLoading(true);
        setError(null);

        try {
            // Process message through chat service
            const result = await chatService.processMessage(
                inputValue,
                currentConversation.context
            );

            // Add assistant response
            let assistantContent = '';

            if (result.error) {
                assistantContent = `Error: ${result.error}`;
            } else if (result.response) {
                // Format the response based on intent
                assistantContent = formatResponse(result.response, result.intent);

                // Update context with new information
                updateContext({
                    lastIntent: result.intent,
                    lastResponse: result.response,
                });
            }

            const assistantMessage = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: assistantContent,
                intent: result.intent,
                timestamp: new Date().toISOString(),
            };

            addMessage(assistantMessage);
        } catch (err) {
            console.error('Error processing message:', err);
            setError(err.message);

            const errorMessage = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: `Sorry, I encountered an error: ${err.message}. Please try again.`,
                timestamp: new Date().toISOString(),
            };

            addMessage(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const formatResponse = (response, intent) => {
        // Handle different response types
        if (!response) return 'No response received.';

        if (response.error) {
            return `Error: ${response.error}`;
        }

        // Format based on intent
        if (intent === 'workflow' || intent === 'planning') {
            return formatWorkflowResponse(response);
        } else if (intent === 'compliance' || intent === 'regulations') {
            return formatComplianceResponse(response);
        } else if (intent === 'risk' || intent === 'risk_analysis') {
            return formatRiskResponse(response);
        } else if (intent === 'checklist' || intent === 'readiness') {
            return formatChecklistResponse(response);
        } else if (intent === 'tariff' || intent === 'pricing') {
            return formatTariffResponse(response);
        } else {
            return formatGenericResponse(response);
        }
    };

    const formatWorkflowResponse = (data) => {
        if (typeof data === 'string') return data;
        if (data.workflow) {
            if (data.workflow.length === 0) {
                return "I couldn't find specific workflow steps for this scenario based on my knowledge base. Please check the product or country name.";
            }
            return `Workflow Steps:\n${data.workflow.map(s => `${s.step}. ${s.title}`).join('\n')}`;
        }
        if (data.steps) {
            return `Workflow Steps:\n${data.steps.map((s, i) => `${i + 1}. ${s}`).join('\n')}`;
        }
        return JSON.stringify(data, null, 2);
    };

    const formatComplianceResponse = (data) => {
        if (typeof data === 'string') return data;
        let responseText = '';
        if (data.message) {
            responseText += data.message + '\n\n';
        }
        if (data.documents && data.documents.length === 0 && data.agencies && data.agencies.length === 0) {
            return responseText || data.note || "No compliance requirements found.";
        }
        if (data.documents || data.agencies || data.approvals) {
            if (data.documents && data.documents.length > 0) {
                responseText += `Required Documents:\n${data.documents.map(d => `• ${d}`).join('\n')}\n\n`;
            }
            if (data.agencies && data.agencies.length > 0) {
                responseText += `Government Agencies:\n${data.agencies.map(a => `• ${a}`).join('\n')}\n\n`;
            }
            if (data.approvals && data.approvals.length > 0) {
                responseText += `Approvals & Permits:\n${data.approvals.map(a => `• ${a}`).join('\n')}\n\n`;
            }
            return responseText.trim();
        }
        if (data.requirements) {
            return `Compliance Requirements:\n${Object.entries(data.requirements)
                .map(([key, value]) => `• ${key}: ${value}`)
                .join('\n')}`;
        }
        return JSON.stringify(data, null, 2);
    };

    const formatRiskResponse = (data) => {
        if (typeof data === 'string') return data;
        let responseText = '';
        if (data.message) {
            responseText += data.message + '\n\n';
        }
        if (data.risks && data.risks.length > 0) {
            responseText += `Risk Analysis:\n${data.risks
                .map((r) => `• ${r.type || 'Risk'}: ${r.description || r} (Severity: ${r.severity || data.risk_level || 'N/A'})`)
                .join('\n')}`;
            if (data.recommendations) {
                responseText += `\n\nRecommendations:\n${data.recommendations.map(r => `• ${r}`).join('\n')}`;
            }
            return responseText;
        }
        return JSON.stringify(data, null, 2);
    };

    const formatChecklistResponse = (data) => {
        if (typeof data === 'string') return data;
        let responseText = '';
        if (data.message) {
            responseText += data.message + '\n\n';
        }
        if (data.items) {
            return responseText + `Checklist:\n${data.items.map((item) => `☐ ${item}`).join('\n')}`;
        }
        return JSON.stringify(data, null, 2);
    };

    const formatTariffResponse = (data) => {
        if (typeof data === 'string') return data;
        let responseText = '';
        if (data.message) {
            responseText += data.message + '\n\n';
        }
        if (data.tariffs) {
            return responseText + `Tariff Information:\n${data.tariffs.map((t) => `• HS Code: ${t.code} - Rate: ${t.rate}`).join('\n')}`;
        }
        return JSON.stringify(data, null, 2);
    };

    const formatGenericResponse = (data) => {
        if (typeof data === 'string') return data;
        if (data.message) return data.message;
        return JSON.stringify(data, null, 2);
    };

    return (
        <div className="chat-container">
            {/* Sidebar */}
            <div className={`chat-sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
                <div className="sidebar-header">
                    <h1>TradePilot AI</h1>
                    <button
                        className="sidebar-toggle"
                        onClick={() => setSidebarOpen(false)}
                    >
                        <X size={20} />
                    </button>
                </div>

                <button
                    className="new-chat-btn"
                    onClick={() => {
                        createNewConversation();
                        setSidebarOpen(false);
                    }}
                >
                    <Plus size={18} />
                    New Chat
                </button>

                <div className="conversations-list">
                    <h3>Conversations</h3>
                    {conversations.length === 0 ? (
                        <p className="no-conversations">No conversations yet</p>
                    ) : (
                        conversations.map((conv) => (
                            <div
                                key={conv.id}
                                className={`conversation-item ${currentConversation?.id === conv.id ? 'active' : ''
                                    }`}
                                onClick={() => selectConversation(conv.id)}
                            >
                                <span className="conv-title">{conv.title}</span>
                                <button
                                    className="delete-btn"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        deleteConversation(conv.id);
                                    }}
                                >
                                    <Trash2 size={16} />
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="chat-main">
                {/* Header */}
                <div className="chat-header">
                    <button
                        className="menu-toggle"
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                    >
                        <Menu size={24} />
                    </button>
                    <h2>TradePilot AI Assistant</h2>
                    <div className="header-spacer" />
                </div>

                {/* Messages Area */}
                <div className="messages-container">
                    {!currentConversation || currentConversation.messages.length === 0 ? (
                        <div className="empty-state">
                            <div className="empty-icon">💬</div>
                            <h2>Start a new conversation</h2>
                            <p>
                                Ask me anything about import/export regulations, compliance, risks,
                                workflows, tariffs, and more!
                            </p>
                            <div className="example-prompts">
                                <button
                                    onClick={() => {
                                        setInputValue('What are the export requirements for tea to the UK?');
                                    }}
                                >
                                    📦 Export requirements
                                </button>
                                <button
                                    onClick={() => {
                                        setInputValue('What are the risks of importing motorcycles?');
                                    }}
                                >
                                    ⚠️ Risk analysis
                                </button>
                                <button
                                    onClick={() => {
                                        setInputValue('Give me a compliance checklist for cinnamon export');
                                    }}
                                >
                                    ✓ Compliance checklist
                                </button>
                                <button
                                    onClick={() => {
                                        setInputValue('What are the tariff codes for electronics?');
                                    }}
                                >
                                    💰 Tariff information
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="messages">
                            {currentConversation.messages.map((msg) => (
                                <div key={msg.id} className={`message ${msg.role}`}>
                                    <div className="message-avatar">
                                        {msg.role === 'user' ? '👤' : '🤖'}
                                    </div>
                                    <div className="message-content">
                                        <div className="message-text">
                                            {msg.content.split('\n').map((line, i) => (
                                                <div key={i}>{line}</div>
                                            ))}
                                        </div>
                                        {msg.intent && (
                                            <div className="message-intent">
                                                Intent: {msg.intent}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="message assistant">
                                    <div className="message-avatar">🤖</div>
                                    <div className="message-content">
                                        <div className="typing-indicator">
                                            <span></span>
                                            <span></span>
                                            <span></span>
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>
                    )}
                </div>

                {/* Error Message */}
                {error && (
                    <div className="error-message">
                        {error}
                        <button onClick={() => setError(null)}>×</button>
                    </div>
                )}

                {/* Input Area */}
                <div className="input-area">
                    <form onSubmit={handleSendMessage} className="input-form">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Ask about export/import requirements, compliance, risks, tariffs..."
                            disabled={isLoading}
                            className="chat-input"
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !inputValue.trim()}
                            className="send-button"
                        >
                            <Send size={20} />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Chat;
