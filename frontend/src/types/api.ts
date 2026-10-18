/**
 * TypeScript types for the AI Sycophancy Lab frontend
 */

export interface SessionCreateRequest {
  study_id: string;
  test_mode: boolean;
  condition?: string;
}

export interface SessionResponse {
  session_id: string;
  study_id: string;
  condition: string;
  status: 'active' | 'ended' | 'error';
  created_at: string;
  message_count: number;
}

export interface SessionStateResponse {
  session_id: string;
  study_id: string;
  condition: string;
  status: 'active' | 'ended' | 'error';
  created_at: string;
  messages: Message[];
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  turn: number;
  model?: string;
  latency_ms?: number;
}

export interface MessageRequest {
  message: string;
}

export interface MessageResponse {
  session_id: string;
  turn_number: number;
  user_message: string;
  assistant_message: string;
  timestamp: string;
  response_latency_ms: number;
  strategy_triggered?: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  llm_provider: string;
  study_id: string;
}
