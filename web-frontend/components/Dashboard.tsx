'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/auth';
import { useEmailStore } from '@/store/email';
import { useAnalysisStore } from '@/store/analysis';
import LoadingSpinner from './LoadingSpinner';

export default function Dashboard() {
  const { user, logout } = useAuthStore();
  const { isConnected, disconnect, stats } = useEmailStore();
  const { currentAnalysis, startAnalysis, isLoading } = useAnalysisStore();
  const [activeTab, setActiveTab] = useState('overview');

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleDisconnect = async () => {
    try {
      await disconnect();
    } catch (error) {
      console.error('Disconnect failed:', error);
    }
  };

  const handleStartAnalysis = async () => {
    try {
      await startAnalysis({
        folder: 'INBOX',
        limit: 1000,
        include_attachments: true,
        include_sentiment: true
      });
    } catch (error) {
      console.error('Analysis failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                Email Box Analyzer
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600 dark:text-gray-300">
                Welcome, {user?.name}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Connection Status */}
        {isConnected && (
          <div className="mb-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <span className="text-green-800 dark:text-green-200 font-medium">
                  Connected to email account
                </span>
              </div>
              <button
                onClick={handleDisconnect}
                className="text-sm text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-200"
              >
                Disconnect
              </button>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
          <nav className="-mb-px flex space-x-8">
            {['overview', 'analysis', 'charts', 'export'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-2 px-1 border-b-2 font-medium text-sm capitalize ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Email Stats */}
              {stats && (
                <>
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      Total Emails
                    </h3>
                    <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                      {stats.total_emails?.toLocaleString() || '0'}
                    </p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      Unread Emails
                    </h3>
                    <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">
                      {stats.unread_emails?.toLocaleString() || '0'}
                    </p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      Total Size
                    </h3>
                    <p className="text-3xl font-bold text-green-600 dark:text-green-400">
                      {stats.total_size_mb ? `${stats.total_size_mb.toFixed(1)} MB` : '0 MB'}
                    </p>
                  </div>
                </>
              )}

              {/* Quick Actions */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
                  Quick Actions
                </h3>
                <div className="space-y-3">
                  <button
                    onClick={handleStartAnalysis}
                    disabled={!isConnected || isLoading}
                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md transition duration-200"
                  >
                    {isLoading ? 'Starting Analysis...' : 'Start Analysis'}
                  </button>
                  <button
                    onClick={() => setActiveTab('analysis')}
                    className="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-md transition duration-200"
                  >
                    View Analysis
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analysis' && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Email Analysis
              </h2>
              {currentAnalysis ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                        {currentAnalysis.total_emails?.toLocaleString()}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Total Emails
                      </div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                        {currentAnalysis.total_size_mb?.toFixed(1)} MB
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Total Size
                      </div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                        {currentAnalysis.top_senders?.length || 0}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Top Senders
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    No analysis results available. Start an analysis to see insights.
                  </p>
                  <button
                    onClick={handleStartAnalysis}
                    disabled={!isConnected || isLoading}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md transition duration-200"
                  >
                    {isLoading ? 'Starting Analysis...' : 'Start Analysis'}
                  </button>
                </div>
              )}
            </div>
          )}

          {activeTab === 'charts' && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Charts & Visualizations
              </h2>
              <div className="text-center py-8">
                <p className="text-gray-600 dark:text-gray-400">
                  Charts and visualizations will be displayed here once analysis is complete.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'export' && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Export Results
              </h2>
              <div className="text-center py-8">
                <p className="text-gray-600 dark:text-gray-400">
                  Export functionality will be available here once analysis is complete.
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
} 