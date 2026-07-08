import React, { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { 
  logInteractionChat, 
  addChatMessage, 
  editInteraction, 
  sendAgentMessage,
  clearError 
} from '../store/interactionSlice.js';

const ChatPanel = () => {
  const dispatch = useDispatch();
  const { chatMessages, loading, error, lastInteraction } = useSelector(state => state.interaction);
  const [inputValue, setInputValue] = useState('');
  const chatBodyRef = useRef(null);

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [chatMessages, loading]);

  const handleSubmit = async () => {
    if (!inputValue.trim() || loading) return;

    // Add user message to chat
    dispatch(addChatMessage({
      type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    }));

    // Determine the intent and call appropriate API
    const message = inputValue.toLowerCase();
    
    if (message.includes('edit') || message.includes('update') || message.includes('change') || message.includes('correct')) {
      // Edit interaction
      dispatch(editInteraction({ 
        message: inputValue,
        interactionId: lastInteraction?.id 
      }));
    } else if (message.includes('history') || message.includes('past') || message.includes('previous') || message.includes('show me')) {
      // Get history - extract HCP name if mentioned
      const hcpMatch = inputValue.match(/(?:dr\.?\s+|doctor\s+)(\w+)/i);
      const hcpName = hcpMatch ? `Dr. ${hcpMatch[1]}` : null;
      dispatch(sendAgentMessage({ 
        message: inputValue,
        hcpName: hcpName
      }));
    } else if (message.includes('suggest') || message.includes('follow') || message.includes('next') || message.includes('recommendation')) {
      // Get suggestions
      dispatch(sendAgentMessage({ 
        message: inputValue,
        interactionId: lastInteraction?.id 
      }));
    } else if (message.includes('compliance') || message.includes('check') || message.includes('safe') || message.includes('okay to say')) {
      // Compliance check
      dispatch(sendAgentMessage({ 
        message: inputValue 
      }));
    } else {
      // Log new interaction (default)
      const result = await dispatch(logInteractionChat(inputValue));
      
      // Auto-fetch AI suggestions after logging
      if (result.payload && result.payload.id) {
        setTimeout(() => {
          dispatch(sendAgentMessage({
            message: "Suggest follow-up actions for this interaction",
            interactionId: result.payload.id
          }));
        }, 1000);
      }
    }

    setInputValue('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const clearChat = () => {
    dispatch(clearError());
  };

  return (
    <div className="panel right">
      <div className="assistant-header">
        <div className="dot">AI</div>
        <div className="titles">
          <div>AI Assistant</div>
          <div>Log interaction via chat</div>
        </div>
      </div>
      
      <div className="chat-body" ref={chatBodyRef}>
        {chatMessages.length === 0 ? (
          <div>
            Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.
            <br/><br/>
            <strong>Try these commands:</strong>
            <ul style={{marginTop: '8px', paddingLeft: '16px'}}>
              <li>"Met Dr. Johnson, positive meeting about OncoBoost"</li>
              <li>"Edit last interaction sentiment to negative"</li>
              <li>"Show history for Dr. Smith"</li>
              <li>"Suggest follow-ups for last meeting"</li>
              <li>"Is it okay to say our drug cures cancer?"</li>
            </ul>
          </div>
        ) : (
          chatMessages.map((message, index) => (
            <div key={index} className={`chat-message ${message.type}`}>
              <small style={{opacity: 0.7, fontSize: '11px', display: 'block', marginBottom: '4px'}}>
                {new Date(message.timestamp).toLocaleTimeString()}
              </small>
              <div style={{
                fontFamily: message.isJson ? '"Consolas", "Monaco", monospace' : 'inherit',
                fontSize: '12px',
                whiteSpace: 'pre-wrap',
                lineHeight: '1.4',
                maxHeight: '500px',
                overflow: 'auto'
              }}>
                {message.content.split('📋 JSON Response:').map((part, i) => {
                  if (i === 0) return part;
                  return (
                    <div key={i}>
                      <div style={{fontWeight: '600', marginBottom: '4px', color: '#0969da'}}>
                        📋 JSON Response:
                      </div>
                      <div style={{
                        background: '#f6f8fa',
                        padding: '8px',
                        borderRadius: '4px',
                        border: '1px solid #d0d7de',
                        fontSize: '11px',
                        fontFamily: '"Consolas", "Monaco", monospace'
                      }}>
                        {part}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))
        )}
        
        {loading && (
          <div className="chat-message ai loading">
            <div>AI is processing your request...</div>
          </div>
        )}
        
        {error && (
          <div className="chat-message ai" style={{background: '#ffeaea'}}>
            <div style={{color: '#d1242f'}}>
              ❌ Error: {error}
              <br/>
              <button 
                onClick={clearChat} 
                style={{
                  marginTop: '4px', 
                  padding: '2px 6px', 
                  fontSize: '11px', 
                  background: '#d1242f', 
                  color: 'white', 
                  border: 'none', 
                  borderRadius: '3px',
                  cursor: 'pointer'
                }}
              >
                Clear
              </button>
            </div>
          </div>
        )}
      </div>
      
      <div className="chat-input-row">
        <input 
          type="text" 
          placeholder="Describe interaction or ask for help..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button 
          className="log-btn" 
          onClick={handleSubmit} 
          disabled={loading || !inputValue.trim()}
          title="Send message to AI assistant"
        >
          {loading ? '⏳' : '⚡'} Log
        </button>
      </div>
    </div>
  );
};

export default ChatPanel;