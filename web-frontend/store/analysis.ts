import { create } from 'zustand';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface AnalysisRequest {
  folder: string;
  limit: number;
  include_attachments: boolean;
  include_sentiment: boolean;
}

interface AnalysisStatus {
  analysis_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  current_step: string;
  error: string | null;
  created_at: string;
  updated_at: string;
}

interface EmailAnalysis {
  analysis_id: string;
  total_emails: number;
  date_range: {
    start: string;
    end: string;
  };
  total_size_mb: number;
  top_senders: Array<{
    email: string;
    name: string;
    count: number;
    percentage: number;
  }>;
  activity_by_time: {
    hourly: Record<string, number>;
    daily: Record<string, number>;
    monthly: Record<string, number>;
  };
  attachment_stats: {
    total_attachments: number;
    attachment_types: Record<string, number>;
    total_attachment_size_mb: number;
  };
  sentiment_analysis: {
    positive: number;
    negative: number;
    neutral: number;
    sentiment_distribution: Record<string, number>;
  };
  thread_analysis: {
    total_threads: number;
    average_thread_length: number;
    longest_thread: number;
    thread_topics: Array<{
      topic: string;
      count: number;
      emails: number;
    }>;
  };
  domain_analysis: {
    top_domains: Array<{
      domain: string;
      count: number;
      percentage: number;
    }>;
    domain_categories: Record<string, number>;
  };
  keyword_analysis: {
    most_common_words: Array<{
      word: string;
      count: number;
      frequency: number;
    }>;
    keyword_trends: Record<string, number[]>;
  };
  response_time_analysis: {
    average_response_time_hours: number;
    response_time_distribution: Record<string, number>;
  };
  email_size_distribution: {
    small: number;
    medium: number;
    large: number;
  };
  language_analysis: {
    primary_language: string;
    language_distribution: Record<string, number>;
  };
  created_at: string;
  processing_time_seconds: number;
}

interface AnalysisState {
  currentAnalysis: EmailAnalysis | null;
  analysisHistory: AnalysisStatus[];
  isLoading: boolean;
  error: string | null;
  startAnalysis: (request: AnalysisRequest) => Promise<string>;
  getAnalysisStatus: (analysisId: string) => Promise<AnalysisStatus>;
  getAnalysisResults: (analysisId: string) => Promise<EmailAnalysis>;
  getLastAnalysis: () => Promise<EmailAnalysis>;
  listAnalyses: (limit?: number, offset?: number) => Promise<AnalysisStatus[]>;
  deleteAnalysis: (analysisId: string) => Promise<void>;
  clearError: () => void;
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  currentAnalysis: null,
  analysisHistory: [],
  isLoading: false,
  error: null,

  startAnalysis: async (request) => {
    set({ isLoading: true, error: null });
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/analysis/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to start analysis');
      }

      const data = await response.json();
      set({ isLoading: false });
      return data.analysis_id;
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.message || 'Failed to start analysis',
      });
      throw error;
    }
  },

  getAnalysisStatus: async (analysisId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/analysis/${analysisId}/status`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to get analysis status');
      }

      const status = await response.json();
      return status;
    } catch (error: any) {
      set({ error: error.message || 'Failed to get analysis status' });
      throw error;
    }
  },

  getAnalysisResults: async (analysisId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/analysis/${analysisId}/results`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to get analysis results');
      }

      const data = await response.json();
      const analysis = data.analysis;
      
      set({ currentAnalysis: analysis });
      return analysis;
    } catch (error: any) {
      set({ error: error.message || 'Failed to get analysis results' });
      throw error;
    }
  },

  getLastAnalysis: async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/analysis/last`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('No analysis results found');
      }

      const data = await response.json();
      const analysis = data.analysis;
      
      set({ currentAnalysis: analysis });
      return analysis;
    } catch (error: any) {
      set({ error: error.message || 'Failed to get last analysis' });
      throw error;
    }
  },

  listAnalyses: async (limit = 10, offset = 0) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/analysis?limit=${limit}&offset=${offset}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to list analyses');
      }

      const data = await response.json();
      const analyses = data.analyses;
      
      set({ analysisHistory: analyses });
      return analyses;
    } catch (error: any) {
      set({ error: error.message || 'Failed to list analyses' });
      throw error;
    }
  },

  deleteAnalysis: async (analysisId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/analysis/${analysisId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete analysis');
      }

      // Remove from current analysis if it's the one being deleted
      const { currentAnalysis } = get();
      if (currentAnalysis?.analysis_id === analysisId) {
        set({ currentAnalysis: null });
      }

      // Update analysis history
      const { analysisHistory } = get();
      set({
        analysisHistory: analysisHistory.filter(analysis => analysis.analysis_id !== analysisId)
      });
    } catch (error: any) {
      set({ error: error.message || 'Failed to delete analysis' });
      throw error;
    }
  },

  clearError: () => {
    set({ error: null });
  },
})); 