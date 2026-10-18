/**
 * API client for communicating with the AI Sycophancy Lab backend
 */

import axios from 'axios';
import type {
  SessionCreateRequest,
  SessionResponse,
  SessionStateResponse,
  MessageRequest,
  MessageResponse,
  HealthResponse,
} from '../types/api';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = {
  /**
   * Health check
   */
  async getHealth(): Promise<HealthResponse> {
    const response = await api.get<HealthResponse>('/health');
    return response.data;
  },

  /**
   * Create a new session
   */
  async createSession(request: SessionCreateRequest): Promise<SessionResponse> {
    const response = await api.post<SessionResponse>('/sessions', request);
    return response.data;
  },

  /**
   * Get session state and messages
   */
  async getSessionState(sessionId: string): Promise<SessionStateResponse> {
    const response = await api.get<SessionStateResponse>(`/sessions/${sessionId}`);
    return response.data;
  },

  /**
   * Send a message
   */
  async sendMessage(sessionId: string, request: MessageRequest): Promise<MessageResponse> {
    const response = await api.post<MessageResponse>(`/sessions/${sessionId}/messages`, request);
    return response.data;
  },

  /**
   * End a session
   */
  async endSession(sessionId: string): Promise<void> {
    await api.post(`/sessions/${sessionId}/end`);
  },
};
