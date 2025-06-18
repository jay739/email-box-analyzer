import { create } from 'zustand';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface EmailProvider {
  id: string;
  name: string;
  imap_host: string;
  imap_port: number;
  smtp_host: string;
  smtp_port: number;
  use_ssl: boolean;
  use_tls: boolean;
  oauth2_supported: boolean;
}

interface EmailStats {
  total_emails: number;
  unread_emails: number;
  total_size_mb: number;
  oldest_email: string;
  newest_email: string;
}

interface EmailFolder {
  name: string;
  path: string;
  message_count: number;
  unread_count: number;
  flags: string[];
}

interface EmailState {
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
  providers: EmailProvider[];
  stats: EmailStats | null;
  folders: EmailFolder[];
  connect: (connectionData: { email: string; password?: string; use_oauth2?: boolean }) => Promise<void>;
  disconnect: () => Promise<void>;
  getProviders: () => Promise<EmailProvider[]>;
  getStats: (folder?: string) => Promise<EmailStats>;
  getFolders: () => Promise<EmailFolder[]>;
  clearError: () => void;
}

export const useEmailStore = create<EmailState>((set, get) => ({
  isConnected: false,
  isLoading: false,
  error: null,
  providers: [],
  stats: null,
  folders: [],

  connect: async (connectionData) => {
    set({ isLoading: true, error: null });
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/email/connect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(connectionData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Connection failed');
      }

      const data = await response.json();
      
      set({
        isConnected: data.connected,
        stats: data.stats,
        folders: data.folders,
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.message || 'Connection failed',
      });
      throw error;
    }
  },

  disconnect: async () => {
    set({ isLoading: true });
    try {
      const token = localStorage.getItem('access_token');
      await fetch(`${API_BASE_URL}/api/email/disconnect`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      set({
        isConnected: false,
        stats: null,
        folders: [],
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.message || 'Disconnect failed',
      });
      throw error;
    }
  },

  getProviders: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/providers/public`);

      if (!response.ok) {
        throw new Error('Failed to fetch providers');
      }

      const providers = await response.json();
      set({ providers });
      return providers;
    } catch (error: any) {
      set({ error: error.message || 'Failed to fetch providers' });
      throw error;
    }
  },

  getStats: async (folder = 'INBOX') => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/email/stats?folder=${folder}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch stats');
      }

      const stats = await response.json();
      set({ stats });
      return stats;
    } catch (error: any) {
      set({ error: error.message || 'Failed to fetch stats' });
      throw error;
    }
  },

  getFolders: async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/email/folders`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch folders');
      }

      const folders = await response.json();
      set({ folders });
      return folders;
    } catch (error: any) {
      set({ error: error.message || 'Failed to fetch folders' });
      throw error;
    }
  },

  clearError: () => {
    set({ error: null });
  },
})); 