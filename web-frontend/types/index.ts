// Email-related types
export interface Email {
  id: string;
  subject: string;
  sender: EmailAddress;
  recipients: EmailAddress[];
  cc: EmailAddress[];
  bcc: EmailAddress[];
  date: Date;
  body: string;
  htmlBody?: string;
  attachments: Attachment[];
  flags: string[];
  size: number;
  threadId?: string;
  messageId: string;
}

export interface EmailAddress {
  name: string;
  email: string;
}

export interface Attachment {
  id: string;
  filename: string;
  contentType: string;
  size: number;
  data?: Buffer;
  url?: string;
}

export interface EmailFolder {
  name: string;
  path: string;
  messageCount: number;
  unreadCount: number;
  flags: string[];
}

// Email provider types
export interface EmailProvider {
  id: string;
  name: string;
  imapHost: string;
  imapPort: number;
  smtpHost: string;
  smtpPort: number;
  useSSL: boolean;
  useTLS: boolean;
  oauth2?: OAuth2Config;
}

export interface OAuth2Config {
  clientId: string;
  clientSecret: string;
  authUrl: string;
  tokenUrl: string;
  redirectUri: string;
  scope: string[];
}

// Analysis result types
export interface EmailAnalysis {
  totalEmails: number;
  dateRange: {
    start: Date;
    end: Date;
  };
  totalSizeMB: number;
  topSenders: SenderStats[];
  activityByTime: TimeActivityStats;
  activityByDay: DayActivityStats;
  activityByMonth: MonthActivityStats;
  attachmentStats: AttachmentStats;
  sentimentAnalysis: SentimentStats;
  threadAnalysis: ThreadStats;
  domainAnalysis: DomainStats;
  keywordAnalysis: KeywordStats;
  responseTimeAnalysis: ResponseTimeStats;
  emailSizeDistribution: SizeDistribution;
  languageAnalysis: LanguageStats;
}

export interface SenderStats {
  email: string;
  name: string;
  count: number;
  percentage: number;
  totalSize: number;
  averageSize: number;
}

export interface TimeActivityStats {
  hourly: { [hour: number]: number };
  daily: { [day: string]: number };
  weekly: { [week: string]: number };
  monthly: { [month: string]: number };
}

export interface DayActivityStats {
  [day: string]: number;
}

export interface MonthActivityStats {
  [month: string]: number;
}

export interface AttachmentStats {
  totalAttachments: number;
  totalSize: number;
  byType: { [type: string]: number };
  bySize: { [sizeRange: string]: number };
  topTypes: { type: string; count: number }[];
}

export interface SentimentStats {
  positive: number;
  negative: number;
  neutral: number;
  averageSentiment: number;
  bySender: { [sender: string]: number };
  byTime: { [timeRange: string]: number };
}

export interface ThreadStats {
  totalThreads: number;
  averageThreadLength: number;
  longestThread: number;
  threadDistribution: { [length: number]: number };
  activeThreads: { threadId: string; messageCount: number }[];
}

export interface DomainStats {
  topDomains: { domain: string; count: number }[];
  domainDistribution: { [domain: string]: number };
  internalVsExternal: {
    internal: number;
    external: number;
  };
}

export interface KeywordStats {
  topKeywords: { keyword: string; count: number }[];
  keywordTrends: { [keyword: string]: { [date: string]: number } };
  subjectKeywords: { keyword: string; count: number }[];
  bodyKeywords: { keyword: string; count: number }[];
}

export interface ResponseTimeStats {
  averageResponseTime: number;
  responseTimeDistribution: { [range: string]: number };
  fastestResponders: { email: string; averageTime: number }[];
  slowestResponders: { email: string; averageTime: number }[];
}

export interface SizeDistribution {
  small: number; // < 1KB
  medium: number; // 1KB - 100KB
  large: number; // 100KB - 1MB
  veryLarge: number; // > 1MB
  averageSize: number;
  medianSize: number;
}

export interface LanguageStats {
  detectedLanguages: { [language: string]: number };
  primaryLanguage: string;
  languageConfidence: number;
}

// Chart and visualization types
export interface ChartData {
  type: 'line' | 'bar' | 'pie' | 'scatter' | 'area' | 'heatmap';
  title: string;
  data: any[];
  options?: any;
  filePath?: string;
}

export interface ChartCollection {
  [chartName: string]: ChartData;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface ConnectionResponse {
  connected: boolean;
  folders?: EmailFolder[];
  stats?: {
    totalMessages: number;
    unreadMessages: number;
    recentMessages: number;
  };
}

export interface AnalysisRequest {
  folder: string;
  limit: number;
  includeAttachments: boolean;
  includeSentiment: boolean;
  dateRange?: {
    start: Date;
    end: Date;
  };
}

// UI state types
export interface AppState {
  isConnected: boolean;
  currentProvider?: EmailProvider;
  currentFolder?: string;
  analysisInProgress: boolean;
  lastAnalysis?: EmailAnalysis;
  error?: string;
}

export interface ConnectionState {
  isConnecting: boolean;
  isConnected: boolean;
  error?: string;
  folders?: EmailFolder[];
  stats?: {
    totalMessages: number;
    unreadMessages: number;
    recentMessages: number;
  };
}

export interface AnalysisState {
  isAnalyzing: boolean;
  progress: number;
  currentStep: string;
  results?: EmailAnalysis;
  error?: string;
}

// Form types
export interface ConnectionFormData {
  providerId: string;
  email: string;
  password: string;
  useOAuth2: boolean;
}

export interface AnalysisFormData {
  folder: string;
  limit: number;
  includeAttachments: boolean;
  includeSentiment: boolean;
  dateRange?: {
    start: Date;
    end: Date;
  };
}

// Authentication types
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  preferences: UserPreferences;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  timezone: string;
  emailRefreshInterval: number;
  defaultAnalysisLimit: number;
  autoSaveResults: boolean;
}

export interface AuthState {
  user?: User;
  isAuthenticated: boolean;
  isLoading: boolean;
  error?: string;
}

// Export types
export interface ExportOptions {
  format: 'json' | 'csv' | 'excel' | 'pdf';
  includeCharts: boolean;
  includeRawData: boolean;
  dateRange?: {
    start: Date;
    end: Date;
  };
}

export interface ExportResult {
  success: boolean;
  fileUrl?: string;
  fileName?: string;
  error?: string;
} 