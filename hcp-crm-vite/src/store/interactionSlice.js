import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_BASE = '/api';

// Async thunks for API calls
export const logInteractionChat = createAsyncThunk(
  'interaction/logChat',
  async (message, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_BASE}/interactions/chat`, {
        message: message
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const logInteractionForm = createAsyncThunk(
  'interaction/logForm',
  async (formData, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_BASE}/interactions/form`, formData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const editInteraction = createAsyncThunk(
  'interaction/edit',
  async ({ message, interactionId, hcpName }, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_BASE}/interactions/edit`, {
        message,
        interaction_id: interactionId,
        hcp_name: hcpName
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const sendAgentMessage = createAsyncThunk(
  'interaction/agentMessage',
  async ({ message, hcpName, interactionId }, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_BASE}/agent/message`, {
        message,
        hcp_name: hcpName,
        interaction_id: interactionId
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

const getCurrentDateTime = () => {
  const now = new Date();
  return {
    date: now.toISOString().split('T')[0],
    time: now.toTimeString().slice(0, 5)
  };
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: {
    formData: {
      hcpName: '',
      interactionType: 'Meeting',
      interactionDate: getCurrentDateTime().date,
      interactionTime: getCurrentDateTime().time,
      attendees: '',
      topicsDiscussed: '',
      sentiment: 'Neutral',
      outcomes: '',
      followUpActions: ''
    },
    chatMessages: [],
    suggestions: [],
    loading: false,
    error: null,
    lastInteraction: null,
    success: null
  },
  reducers: {
    updateFormData: (state, action) => {
      state.formData = { ...state.formData, ...action.payload };
    },
    addChatMessage: (state, action) => {
      state.chatMessages.push(action.payload);
    },
    clearChatMessages: (state) => {
      state.chatMessages = [];
    },
    addSuggestion: (state, action) => {
      if (!state.suggestions.includes(action.payload)) {
        state.suggestions.push(action.payload);
      }
    },
    applySuggestion: (state, action) => {
      const suggestion = action.payload;
      const current = state.formData.followUpActions;
      state.formData.followUpActions = current ? current + '\n' + suggestion : suggestion;
    },
    clearError: (state) => {
      state.error = null;
    },
    clearSuccess: (state) => {
      state.success = null;
    },
    resetForm: (state) => {
      const { date, time } = getCurrentDateTime();
      state.formData = {
        hcpName: '',
        interactionType: 'Meeting',
        interactionDate: date,
        interactionTime: time,
        attendees: '',
        topicsDiscussed: '',
        sentiment: 'Neutral',
        outcomes: '',
        followUpActions: ''
      };
    }
  },
  extraReducers: (builder) => {
    builder
      // Chat logging
      .addCase(logInteractionChat.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.success = null;
      })
      .addCase(logInteractionChat.fulfilled, (state, action) => {
        state.loading = false;
        state.lastInteraction = action.payload;
        state.success = `✓ Logged interaction with ${action.payload.hcp_name}`;
        
        // Add clean response to chat
        state.chatMessages.push({
          type: 'ai',
          content: `✅ Interaction Logged Successfully!

🆔 ID: ${action.payload.id}
👤 HCP: ${action.payload.hcp_name}
📞 Type: ${action.payload.interaction_type}
😊 Sentiment: ${action.payload.sentiment}
💭 Topics: ${action.payload.topics_discussed || 'N/A'}
📦 Materials: ${action.payload.materials_shared || 'None'}
🎯 Outcomes: ${action.payload.outcomes || 'None'}
📝 Follow-ups: ${action.payload.follow_up_actions || 'None'}

📋 JSON Response:
${JSON.stringify(action.payload, null, 2)}`,
          timestamp: new Date().toISOString(),
          isJson: true
        });
        
        // Update suggestions if any returned directly from log response
        if (action.payload.suggestions) {
          action.payload.suggestions.forEach(suggestion => {
            if (!state.suggestions.includes(suggestion)) {
              state.suggestions.push(suggestion);
            }
          });
        }
      })
      .addCase(logInteractionChat.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.error || action.payload || 'Failed to log interaction';
      })
      // Form logging
      .addCase(logInteractionForm.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.success = null;
      })
      .addCase(logInteractionForm.fulfilled, (state, action) => {
        state.loading = false;
        state.lastInteraction = action.payload;
        state.success = `✓ Interaction logged successfully via form`;
      })
      .addCase(logInteractionForm.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.error || action.payload || 'Failed to log interaction';
      })
      // Edit interaction
      .addCase(editInteraction.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(editInteraction.fulfilled, (state, action) => {
        state.loading = false;
        state.chatMessages.push({
          type: 'ai',
          content: `✅ Interaction Updated!

🔄 Updated Fields: ${action.payload.updated_fields?.join(', ') || 'interaction updated'}

📋 JSON Response:
${JSON.stringify(action.payload, null, 2)}`,
          timestamp: new Date().toISOString(),
          isJson: true
        });
      })
      .addCase(editInteraction.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.error || action.payload || 'Failed to edit interaction';
      })
      // Agent message
      .addCase(sendAgentMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendAgentMessage.fulfilled, (state, action) => {
        state.loading = false;
        const result = action.payload;
        let responseText = '';
        
        if (result.suggestions) {
          responseText = `💡 Follow-up Suggestions:

${result.suggestions.map(s => `• ${s}`).join('\n')}`;
          result.suggestions.forEach(suggestion => {
            if (!state.suggestions.includes(suggestion)) {
              state.suggestions.push(suggestion);
            }
          });
        } else if (result.summary) {
          responseText = `📊 HCP History Summary:

👤 HCP: ${result.hcp_name}
📈 Total Interactions: ${result.total_interactions}
📝 Summary: ${result.summary}`;
        } else if (result.flagged !== undefined) {
          responseText = result.flagged 
            ? `⚠️ Compliance Issue Detected!

🚫 Reason: ${result.reason}`
            : `✅ Compliance Check Passed

No issues detected with your message.`;
        } else if (result.total_interactions !== undefined) {
          responseText = `📊 Interaction History:

👤 HCP: ${result.hcp_name}
📈 Total: ${result.total_interactions}
📝 ${result.summary}`;
        }
        
        responseText += `

📋 JSON Response:
${JSON.stringify(result, null, 2)}`;
        
        state.chatMessages.push({
          type: 'ai',
          content: responseText,
          timestamp: new Date().toISOString(),
          isJson: true
        });
      })
      .addCase(sendAgentMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.error || action.payload || 'Failed to process agent message';
      });
  }
});

export const {
  updateFormData,
  addChatMessage,
  clearChatMessages,
  addSuggestion,
  applySuggestion,
  clearError,
  clearSuccess,
  resetForm
} = interactionSlice.actions;

export default interactionSlice.reducer;