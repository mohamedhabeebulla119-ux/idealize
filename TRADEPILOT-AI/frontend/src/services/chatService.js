const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Helper function to extract information from query
const extractQueryInfo = (query) => {
    const lowerQuery = query.toLowerCase();

    // Check for trade type
    const tradeType = lowerQuery.includes('import') ? 'import' :
        lowerQuery.includes('export') ? 'export' : null;

    // Check for country
    const countryMatch = query.match(/(?:to|from|with|in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/);
    const country = countryMatch ? countryMatch[1] : 'Sri Lanka';

    // Extract product (very basic extraction)
    const productMatch = query.match(/(?:for|of|export|import)\s+([a-zA-Z\s]+?)(?:\s+to|\s+from|$)/i);
    const product = productMatch ? productMatch[1].trim() : 'general product';

    return { tradeType, country, product };
};

export const chatService = {
    // Determine user intent
    async getIntent(message) {
        try {
            const response = await fetch(`${API_BASE_URL}/intent/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message }),
            });

            if (!response.ok) throw new Error('Intent detection failed');
            return await response.json();
        } catch (error) {
            console.error('Intent error:', error);
            return { intent: 'general', confidence: 0.5 };
        }
    },

    // Get workflow recommendations
    async getWorkflow(data) {
        try {
            const requestData = {
                trade_type: data.trade_type || 'export',
                product: data.product || 'general product',
                country: data.country || 'Sri Lanka',
            };

            const response = await fetch(`${API_BASE_URL}/workflow/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (!response.ok) throw new Error('Workflow request failed');
            return await response.json();
        } catch (error) {
            console.error('Workflow error:', error);
            return { error: error.message };
        }
    },

    // Check compliance
    async checkCompliance(data) {
        try {
            const requestData = {
                trade_type: data.trade_type || 'export',
                product: data.product || 'general product',
                country: data.country || 'Sri Lanka',
            };

            const response = await fetch(`${API_BASE_URL}/compliance/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (!response.ok) throw new Error('Compliance check failed');
            return await response.json();
        } catch (error) {
            console.error('Compliance error:', error);
            return { error: error.message };
        }
    },

    // Get risk analysis
    async getRiskAnalysis(data) {
        try {
            const requestData = {
                trade_type: data.trade_type || 'export',
                product: data.product || 'general product',
                country: data.country || 'Sri Lanka',
            };

            const response = await fetch(`${API_BASE_URL}/risk/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (!response.ok) throw new Error('Risk analysis failed');
            return await response.json();
        } catch (error) {
            console.error('Risk error:', error);
            return { error: error.message };
        }
    },

    // Get checklist
    async getChecklist(data) {
        try {
            const requestData = {
                trade_type: data.trade_type || 'export',
                product: data.product || 'general product',
                country: data.country || 'Sri Lanka',
            };

            const response = await fetch(`${API_BASE_URL}/checklist/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (!response.ok) throw new Error('Checklist generation failed');
            return await response.json();
        } catch (error) {
            console.error('Checklist error:', error);
            return { error: error.message };
        }
    },

    // Get tariff information
    async searchTariff(data) {
        try {
            const requestData = {
                product: data.product || 'tea',
                hs_code: data.hs_code || '0902',
            };

            const response = await fetch(`${API_BASE_URL}/tariff-search/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (!response.ok) throw new Error('Tariff search failed');
            return await response.json();
        } catch (error) {
            console.error('Tariff error:', error);
            return { error: error.message };
        }
    },

    // Process user message through appropriate agent
    async processMessage(message, context = {}) {
        try {
            // First get intent
            const intentResult = await this.getIntent(message);
            const intent = (intentResult.intent || intentResult.type || 'general').toLowerCase();

            // If greeting or general query, return final_response from intent agent directly
            if (intent === 'greeting' || intent === 'general') {
                return {
                    intent: intent,
                    response: intentResult.final_response || 'No response generated.',
                    timestamp: new Date().toISOString(),
                };
            }

            // Extract additional info from query
            const queryInfo = extractQueryInfo(message);

            // Route to appropriate agent based on intent
            let response;

            switch (intent) {
                case 'workflow':
                case 'planning':
                    response = await this.getWorkflow({
                        query: message,
                        ...queryInfo,
                    });
                    break;

                case 'compliance':
                case 'regulations':
                case 'requirement':
                    response = await this.checkCompliance({
                        query: message,
                        ...queryInfo,
                    });
                    break;

                case 'risk':
                case 'risk_analysis':
                case 'hazard':
                    response = await this.getRiskAnalysis({
                        query: message,
                        ...queryInfo,
                    });
                    break;

                case 'checklist':
                case 'readiness':
                case 'preparation':
                    response = await this.getChecklist({
                        query: message,
                        ...queryInfo,
                    });
                    break;

                case 'tariff':
                case 'pricing':
                case 'cost':
                case 'hs_code':
                    response = await this.searchTariff({
                        product: queryInfo.product || 'product',
                        hs_code: '0902',
                    });
                    break;

                default:
                    // Fallback for general queries if they mention export/import
                    if (queryInfo.tradeType) {
                        response = await this.getWorkflow({
                            query: message,
                            ...queryInfo,
                        });
                    } else {
                        response = await this.checkCompliance({
                            query: message,
                            ...queryInfo,
                        });
                    }
            }

            return {
                intent,
                response,
                timestamp: new Date().toISOString(),
            };
        } catch (error) {
            console.error('Message processing error:', error);
            return {
                error: error.message,
                timestamp: new Date().toISOString(),
            };
        }
    },
};
