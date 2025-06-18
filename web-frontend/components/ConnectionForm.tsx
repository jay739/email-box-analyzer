'use client';

import { useState } from 'react';
import { useEmailStore } from '@/store/email';

export default function ConnectionForm() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [oauthUrl, setOauthUrl] = useState('');

  const { connect } = useEmailStore();

  const detectProvider = (email: string) => {
    const domain = email.split('@')[1]?.toLowerCase();
    const providerMap: { [key: string]: string } = {
      'gmail.com': 'Gmail',
      'googlemail.com': 'Gmail',
      'outlook.com': 'Outlook',
      'hotmail.com': 'Outlook',
      'live.com': 'Outlook',
      'yahoo.com': 'Yahoo',
      'ymail.com': 'Yahoo'
    };
    return providerMap[domain] || 'Unknown';
  };

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case 'Gmail':
        return '📧';
      case 'Outlook':
        return '📨';
      case 'Yahoo':
        return '📬';
      default:
        return '📮';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setOauthUrl('');

    try {
      const provider = detectProvider(email);
      
      if (provider === 'Gmail') {
        // For Gmail, start OAuth2 flow
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/oauth/gmail/auth/public`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to start OAuth2 flow');
        }

        const data = await response.json();
        
        if (data.auth_url) {
          setOauthUrl(data.auth_url);
          // Open OAuth2 URL in new window/tab
          window.open(data.auth_url, '_blank', 'width=500,height=600');
        } else if (data.user_info) {
          // Already authenticated
          setError('Already connected to Gmail!');
        }
      } else {
        // For other providers, use the new simplified API
        await connect({
          email: email,
          password: '', // Will be handled by OAuth2 or App Password flow
          use_oauth2: true
        });
      }
    } catch (err: any) {
      setError(err.message || 'Failed to connect to email account');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOAuthCallback = async (authorizationCode: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/oauth/gmail/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ authorization_code: authorizationCode }),
      });

      if (!response.ok) {
        throw new Error('Failed to complete OAuth2 authentication');
      }

      const data = await response.json();
      if (data.success) {
        setError('Successfully connected to Gmail!');
        setOauthUrl('');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to complete authentication');
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Connect Email Account
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mt-2">
          Enter your email address and we'll handle the rest
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Email Address
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="Enter your email address (e.g., user@gmail.com)"
          />
          {email && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Detected provider: {getProviderIcon(detectProvider(email))} {detectProvider(email)}
            </p>
          )}
        </div>

        {error && (
          <div className="text-red-600 dark:text-red-400 text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded-md">
            {error}
          </div>
        )}

        {oauthUrl && (
          <div className="text-blue-600 dark:text-blue-400 text-sm bg-blue-50 dark:bg-blue-900/20 p-3 rounded-md">
            <p>OAuth2 window opened! Please complete the authentication in the new window.</p>
            <p className="mt-2">
              <a 
                href={oauthUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-800 dark:text-blue-200 underline"
              >
                Click here if the window didn't open
              </a>
            </p>
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading || !email}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-md transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Connecting...
            </div>
          ) : (
            `Connect ${email ? detectProvider(email) : 'Email'} Account`
          )}
        </button>
      </form>

      <div className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-md">
        <h3 className="text-sm font-medium text-green-800 dark:text-green-200 mb-2">
          Secure Authentication
        </h3>
        <p className="text-xs text-green-700 dark:text-green-300">
          For Gmail: You'll be redirected to Google's secure login page. 
          For other providers: We'll guide you through the secure connection process.
        </p>
      </div>
    </div>
  );
} 