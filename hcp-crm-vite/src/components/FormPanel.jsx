import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { 
  updateFormData, 
  logInteractionForm, 
  sendAgentMessage,
  applySuggestion, 
  clearError, 
  clearSuccess,
  resetForm
} from '../store/interactionSlice.js';

const FormPanel = () => {
  const dispatch = useDispatch();
  const { formData, suggestions, loading, error, success, lastInteraction } = useSelector(state => state.interaction);

  const handleInputChange = (field, value) => {
    dispatch(updateFormData({ [field]: value }));
  };

  const handleSubmit = async () => {
    if (!formData.hcpName.trim()) {
      return;
    }
    
    const submitData = {
      hcp_name: formData.hcpName,
      interaction_type: formData.interactionType,
      interaction_date: formData.interactionDate,
      interaction_time: formData.interactionTime,
      attendees: formData.attendees,
      topics_discussed: formData.topicsDiscussed,
      sentiment: formData.sentiment,
      outcomes: formData.outcomes,
      follow_up_actions: formData.followUpActions
    };
    
    // Log the interaction via form
    try {
      const result = await dispatch(logInteractionForm(submitData)).unwrap();
      
      // If successful, automatically get AI suggestions
      if (result && result.id) {
        setTimeout(() => {
          dispatch(sendAgentMessage({
            message: "Suggest follow-up actions for this interaction",
            interactionId: result.id
          }));
        }, 1000);
      }
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  const handleGetSuggestions = () => {
    if (lastInteraction && lastInteraction.id) {
      dispatch(sendAgentMessage({
        message: "Suggest follow-up actions for this interaction",
        interactionId: lastInteraction.id
      }));
    } else if (formData.hcpName.trim()) {
      // Use form data to generate suggestions
      dispatch(sendAgentMessage({
        message: `Suggest follow-up actions for a ${formData.interactionType} with ${formData.hcpName} discussing ${formData.topicsDiscussed || 'healthcare topics'}`,
        hcpName: formData.hcpName
      }));
    }
  };

  const handleSuggestionClick = (suggestion) => {
    dispatch(applySuggestion(suggestion));
  };

  const handleReset = () => {
    dispatch(resetForm());
    dispatch(clearError());
    dispatch(clearSuccess());
  };

  React.useEffect(() => {
    if (error || success) {
      const timer = setTimeout(() => {
        dispatch(clearError());
        dispatch(clearSuccess());
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, success, dispatch]);

  return (
    <div className="panel left">
      <div className="section-title">Interaction Details</div>
      
      <div className="row">
        <div className="field">
          <label>HCP Name</label>
          <input 
            type="text" 
            placeholder="Search or select HCP..."
            value={formData.hcpName}
            onChange={(e) => handleInputChange('hcpName', e.target.value)}
          />
        </div>
        <div className="field">
          <label>Interaction Type</label>
          <select 
            value={formData.interactionType}
            onChange={(e) => handleInputChange('interactionType', e.target.value)}
          >
            <option value="Meeting">Meeting</option>
            <option value="Call">Call</option>
            <option value="Email">Email</option>
            <option value="Conference">Conference</option>
          </select>
        </div>
      </div>

      <div className="row">
        <div className="field">
          <label>Date</label>
          <input 
            type="date" 
            value={formData.interactionDate}
            onChange={(e) => handleInputChange('interactionDate', e.target.value)}
          />
        </div>
        <div className="field">
          <label>Time</label>
          <input 
            type="time" 
            value={formData.interactionTime}
            onChange={(e) => handleInputChange('interactionTime', e.target.value)}
          />
        </div>
      </div>

      <div className="row">
        <div className="field">
          <label>Attendees</label>
          <input 
            type="text" 
            placeholder="Enter names or search..."
            value={formData.attendees}
            onChange={(e) => handleInputChange('attendees', e.target.value)}
          />
        </div>
      </div>

      <div className="row">
        <div className="field">
          <label>Topics Discussed</label>
          <div className="textarea-wrap">
            <textarea 
              placeholder="Enter key discussion points..."
              value={formData.topicsDiscussed}
              onChange={(e) => handleInputChange('topicsDiscussed', e.target.value)}
            />
            <span className="icon">🎤</span>
          </div>
        </div>
      </div>

      <button className="btn voice-btn">⛭ Summarize from Voice Note (Requires Consent)</button>

      <div className="section-title" style={{marginTop: '6px'}}>Materials Shared / Samples Distributed</div>
      
      <div className="row">
        <div className="field">
          <div className="btn-row">
            <span className="subfield-label">Materials Shared</span>
            <button className="btn">🔍 Search/Add</button>
          </div>
          <div className="muted">No materials added.</div>
        </div>
      </div>

      <div className="row">
        <div className="field">
          <div className="btn-row">
            <span className="subfield-label">Samples Distributed</span>
            <button className="btn">➕ Add Sample</button>
          </div>
          <div className="muted">No samples added.</div>
        </div>
      </div>

      <div className="subfield-label">Observed/Inferred HCP Sentiment</div>
      <div className="sentiment">
        <label>
          <input 
            type="radio" 
            name="sentiment" 
            checked={formData.sentiment === 'Positive'}
            onChange={() => handleInputChange('sentiment', 'Positive')}
          /> 🙂 Positive
        </label>
        <label>
          <input 
            type="radio" 
            name="sentiment" 
            checked={formData.sentiment === 'Neutral'}
            onChange={() => handleInputChange('sentiment', 'Neutral')}
          /> 😐 Neutral
        </label>
        <label>
          <input 
            type="radio" 
            name="sentiment" 
            checked={formData.sentiment === 'Negative'}
            onChange={() => handleInputChange('sentiment', 'Negative')}
          /> 🙁 Negative
        </label>
      </div>

      <div className="row">
        <div className="field">
          <label>Outcomes</label>
          <textarea 
            placeholder="Key outcomes or agreements..."
            value={formData.outcomes}
            onChange={(e) => handleInputChange('outcomes', e.target.value)}
          />
        </div>
      </div>

      <div className="row">
        <div className="field">
          <label>Follow-up Actions</label>
          <textarea 
            placeholder="Enter next steps or tasks..."
            value={formData.followUpActions}
            onChange={(e) => handleInputChange('followUpActions', e.target.value)}
          />
        </div>
      </div>

      {suggestions.length > 0 && (
        <div className="suggested">
          <p>AI Suggested Follow-ups:</p>
          <ul>
            {suggestions.map((suggestion, index) => (
              <li key={index}>
                <a onClick={() => handleSuggestionClick(suggestion)}>
                  + {suggestion}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div style={{display: 'flex', gap: '8px', marginBottom: '16px'}}>
        <button 
          className="btn" 
          onClick={handleGetSuggestions}
          disabled={loading || !formData.hcpName.trim()}
          style={{
            background: '#0969da', 
            color: '#fff', 
            border: 'none'
          }}
        >
          {loading ? '🤖 Getting...' : '💡 Get AI Suggestions'}
        </button>
      </div>

      {error && <div className="error">Error: {error}</div>}
      {success && <div className="success">{success}</div>}
      
      <div style={{display: 'flex', gap: '12px', marginTop: '16px'}}>
        <button 
          className="btn" 
          onClick={handleSubmit}
          disabled={loading || !formData.hcpName.trim()}
          style={{
            background: '#2ea043', 
            color: '#fff', 
            border: 'none',
            flex: 1
          }}
        >
          {loading ? 'Logging...' : 'Log Interaction'}
        </button>
        
        <button 
          className="btn" 
          onClick={handleReset}
          disabled={loading}
          style={{
            background: '#6e7781', 
            color: '#fff', 
            border: 'none'
          }}
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default FormPanel;