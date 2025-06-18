'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/auth';
import { useEmailStore } from '@/store/email';
import { useAnalysisStore } from '@/store/analysis';
import ConnectionForm from '@/components/ConnectionForm';
import Dashboard from '@/components/Dashboard';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Page() {
  const { user, isAuthenticated, checkAuth } = useAuthStore();
  const { isConnected } = useEmailStore();
  const { currentAnalysis } = useAnalysisStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeApp = async () => {
      try {
        await checkAuth();
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeApp();
  }, [checkAuth]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  // Show login form if not authenticated
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex flex-col items-center justify-center py-12 px-4">
        <header className="w-full max-w-3xl mb-10 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-2">
            Email Box Analyzer
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Connect your email, analyze your inbox, and visualize your email activity with powerful insights.
          </p>
        </header>
        
        <ConnectionForm />
      </div>
    );
  }

  // Show dashboard if authenticated
  return <Dashboard />;
} 