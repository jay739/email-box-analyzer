# Email Box Analyzer - Web Frontend

A modern, responsive web application built with Next.js for comprehensive email analysis and visualization.

## 🚀 Features

### Core Features
- **Modern Web Interface**: Built with Next.js 14, React 18, and TypeScript
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark Mode Support**: Automatic theme switching with system preference detection
- **Real-time Updates**: Live progress tracking for email analysis
- **Interactive Visualizations**: Rich charts and graphs using Recharts
- **Email Provider Support**: Gmail, Outlook, Yahoo, and custom IMAP servers
- **OAuth2 Authentication**: Secure authentication for supported providers

### Analysis Features
- **Comprehensive Email Analysis**: Sender statistics, time patterns, sentiment analysis
- **Advanced Visualizations**: Interactive charts for email activity, sender distribution, and trends
- **Export Capabilities**: Export results in JSON, CSV, Excel, and PDF formats
- **Real-time Progress**: Live progress tracking during analysis
- **Batch Processing**: Handle large email volumes efficiently

### User Experience
- **Intuitive Dashboard**: Clean, modern interface with key metrics at a glance
- **Quick Actions**: One-click analysis for common scenarios
- **Responsive Tables**: Virtualized tables for handling large datasets
- **Search and Filter**: Advanced filtering and search capabilities
- **Keyboard Shortcuts**: Power user features for efficient navigation

## 🛠 Tech Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **React 18**: Latest React features and concurrent rendering
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions

### State Management
- **Zustand**: Lightweight state management
- **React Query**: Server state management and caching

### UI Components
- **Headless UI**: Accessible UI components
- **Heroicons**: Beautiful SVG icons
- **Recharts**: Interactive charts and visualizations
- **React Hook Form**: Form handling and validation

### Development Tools
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Jest**: Unit testing
- **Cypress**: E2E testing
- **Husky**: Git hooks

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm 9+ or yarn
- Backend API running (see main project README)

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd email_box_analyzer/web-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment Configuration**
   Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   NEXT_PUBLIC_GOOGLE_VERIFICATION=your-google-verification-code
   ```

4. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗 Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Dashboard page
│   ├── analysis/          # Analysis pages
│   ├── charts/            # Chart pages
│   ├── settings/          # Settings pages
│   └── globals.css        # Global styles
├── components/            # Reusable components
│   ├── ui/               # Base UI components
│   ├── dashboard/        # Dashboard-specific components
│   ├── charts/           # Chart components
│   ├── dialogs/          # Modal dialogs
│   └── providers/        # Context providers
├── lib/                  # Utility libraries
│   ├── api.ts           # API client
│   └── utils.ts         # Utility functions
├── store/               # Zustand stores
│   └── index.ts         # Store definitions
├── types/               # TypeScript type definitions
│   └── index.ts         # Main type definitions
├── hooks/               # Custom React hooks
└── styles/              # Additional styles
```

## 🎨 UI Components

### Base Components
- **Button**: Various button styles and variants
- **Card**: Content containers with headers and footers
- **Input**: Form input fields with validation
- **Badge**: Status indicators and labels
- **LoadingSpinner**: Loading indicators
- **Modal**: Dialog components

### Dashboard Components
- **DashboardStats**: Key metrics display
- **QuickActions**: Common action buttons
- **RecentActivity**: Activity timeline
- **EmailProviderCard**: Provider selection cards

### Chart Components
- **ActivityChart**: Email activity over time
- **SenderChart**: Top sender distribution
- **SentimentChart**: Sentiment analysis results
- **SizeChart**: Email size distribution

## 🔧 Development

### Available Scripts
```bash
# Development
npm run dev              # Start development server
npm run build            # Build for production
npm run start            # Start production server

# Code Quality
npm run lint             # Run ESLint
npm run type-check       # Run TypeScript checks
npm run format           # Format code with Prettier
npm run format:check     # Check code formatting

# Testing
npm run test             # Run unit tests
npm run test:watch       # Run tests in watch mode
npm run test:coverage    # Generate coverage report
```

### Code Style
- **ESLint**: Configured with TypeScript and React rules
- **Prettier**: Consistent code formatting
- **TypeScript**: Strict type checking enabled
- **Import Sorting**: Automatic import organization

### Testing Strategy
- **Unit Tests**: Jest with React Testing Library
- **Integration Tests**: Component integration testing
- **E2E Tests**: Cypress for critical user flows
- **Visual Regression**: Screenshot testing for UI consistency

## 🚀 Deployment

### Production Build
```bash
npm run build
npm run start
```

### Docker Deployment
```dockerfile
FROM node:18-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Build application
FROM base AS builder
WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

### Environment Variables
```env
# Required
NEXT_PUBLIC_API_URL=https://your-api-domain.com

# Optional
NEXT_PUBLIC_APP_URL=https://your-app-domain.com
NEXT_PUBLIC_GOOGLE_VERIFICATION=your-verification-code
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

## 🔒 Security

### Authentication
- **JWT Tokens**: Secure token-based authentication
- **OAuth2**: Support for provider OAuth flows
- **Session Management**: Secure session handling
- **CSRF Protection**: Built-in CSRF protection

### Data Protection
- **HTTPS Only**: Secure communication
- **Input Validation**: Client and server-side validation
- **XSS Prevention**: React's built-in XSS protection
- **Content Security Policy**: CSP headers for security

## 📊 Performance

### Optimization Features
- **Code Splitting**: Automatic route-based code splitting
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: Webpack bundle analyzer
- **Lazy Loading**: Component and route lazy loading
- **Caching**: React Query caching strategies

### Monitoring
- **Performance Metrics**: Core Web Vitals tracking
- **Error Tracking**: Error boundary and logging
- **Analytics**: User behavior tracking
- **Health Checks**: Application health monitoring

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

### Code Standards
- Follow TypeScript best practices
- Write comprehensive tests
- Use meaningful commit messages
- Update documentation as needed
- Follow the established code style

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check the main project README
- **Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas
- **Wiki**: Additional documentation and guides

### Common Issues
- **Build Errors**: Ensure Node.js version compatibility
- **API Connection**: Verify backend API is running
- **OAuth Issues**: Check provider configuration
- **Performance**: Monitor bundle size and loading times

## 🔮 Roadmap

### Upcoming Features
- **Real-time Notifications**: WebSocket-based updates
- **Advanced Filters**: Complex email filtering
- **Bulk Operations**: Batch email processing
- **API Integration**: Third-party service integration
- **Mobile App**: React Native companion app

### Performance Improvements
- **Service Workers**: Offline functionality
- **WebAssembly**: Performance-critical operations
- **Edge Computing**: CDN-based processing
- **Progressive Web App**: PWA capabilities

---

**Built with ❤️ using Next.js and modern web technologies** 