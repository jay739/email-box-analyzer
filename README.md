# Email Box Analyzer 📧📊

<p align="center">
  <img src="docs/logo.svg" alt="email-box-analyzer logo" width="128" />
</p>

A modern, intelligent email analysis platform that provides deep insights into your email patterns, communication habits, and inbox organization. Built with FastAPI backend and Next.js frontend, featuring seamless OAuth2 authentication and comprehensive email analytics.

## 🎯 Project Scope

Email Box Analyzer is designed to help users understand their email communication patterns through advanced analytics, sentiment analysis, and interactive visualizations. The platform supports multiple email providers with a focus on security and user privacy.

### Key Objectives
- **Simplify Email Analysis**: One-click email input that automatically detects provider and handles authentication
- **Comprehensive Insights**: Deep analysis of email patterns, sender relationships, and communication trends
- **Privacy-First**: Secure OAuth2 authentication with no permanent storage of email content
- **Modern UX**: Intuitive web interface with real-time progress tracking and interactive visualizations

## 🚀 Features

### 🔐 Smart Authentication
- **Provider Detection**: Automatically detects email provider from domain
- **OAuth2 Integration**: Seamless Gmail authentication via Google OAuth2
- **App Password Support**: Secure authentication for other providers (Outlook, Yahoo, etc.)
- **Single Email Input**: Users only need to enter their email address

### 📊 Advanced Analytics
- **Sender Analysis**: Top senders, frequency patterns, and relationship insights
- **Time Patterns**: Email activity by hour, day, week, and month
- **Sentiment Analysis**: Emotional tone analysis of email content
- **Thread Analysis**: Conversation flow and response patterns
- **Attachment Statistics**: File type analysis and storage insights

### 📈 Interactive Visualizations
- **Real-time Charts**: Dynamic charts using Recharts library
- **Multiple Chart Types**: Bar charts, line graphs, pie charts, and heatmaps
- **Responsive Design**: Mobile-optimized visualizations
- **Export Capabilities**: PNG, SVG, and PDF export options

### 🛠 Technical Features
- **RESTful API**: FastAPI-based backend with automatic OpenAPI documentation
- **Async Processing**: Background task processing for large email datasets
- **Real-time Updates**: WebSocket-based progress tracking
- **CORS Support**: Cross-origin resource sharing for web frontend
- **Comprehensive Logging**: Structured logging with error tracking

## 🏗 Architecture

### Backend (FastAPI)
```
src/
├── api/                    # API layer
│   ├── routes/            # API route handlers
│   │   ├── auth.py        # JWT authentication routes
│   │   ├── oauth.py       # OAuth2 authentication routes
│   │   ├── providers.py   # Email provider detection
│   │   ├── email.py       # Email connection and operations
│   │   ├── analysis.py    # Email analysis engine
│   │   ├── charts.py      # Chart generation
│   │   └── export.py      # Data export functionality
│   └── models.py          # Pydantic data models
├── core/                  # Core business logic
│   ├── config_manager.py  # Provider configuration
│   ├── email_manager.py   # Email operations
│   └── gmail_oauth_manager.py # Gmail OAuth2 handling
├── analyzers/             # Analysis modules
│   └── email_analyzer.py  # Email analysis engine
├── visualizers/           # Visualization modules
│   └── chart_manager.py   # Chart generation
├── utils/                 # Utility modules
│   ├── logger.py          # Logging configuration
│   └── exceptions.py      # Custom exceptions
└── main.py               # FastAPI application entry point
```

### Frontend (Next.js)
```
web-frontend/
├── app/                   # Next.js App Router pages
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ConnectionForm.tsx # Email connection form
│   ├── Dashboard.tsx      # Main dashboard
│   ├── LoadingSpinner.tsx # Loading indicators
│   └── LoginForm.tsx      # Authentication form
├── store/                 # State management
│   ├── analysis.ts        # Analysis state
│   ├── auth.ts           # Authentication state
│   └── email.ts          # Email state
├── types/                 # TypeScript definitions
└── package.json          # Dependencies and scripts
```

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management
- **Google OAuth2**: Secure Gmail authentication
- **IMAP/SMTP**: Email protocol support for multiple providers
- **JWT**: Authentication and authorization

### Frontend
- **Next.js 14**: React framework with App Router
- **React 18**: Latest React features and concurrent rendering
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **Recharts**: Interactive charts and visualizations

### Development & Deployment
- **Docker**: Containerization for consistent environments
- **Jenkins**: CI/CD pipeline automation
- **Black & isort**: Python code formatting
- **ESLint & Prettier**: Frontend code quality
- **Make**: Build automation

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Git

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jay739/email-box-analyzer.git
   cd email-box-analyzer
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up Gmail OAuth2 (see GMAIL_OAUTH2_SETUP.md)
   mkdir -p ~/.email_analyzer/oauth
   # Download credentials.json from Google Cloud Console
   # Place it in ~/.email_analyzer/oauth/credentials.json
   
   # Start the backend
   make run
   ```

3. **Frontend Setup**
   ```bash
   # Navigate to frontend directory
   cd web-frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

4. **Access the Application**
   - Web Interface: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - API ReDoc: http://localhost:8000/redoc

### Gmail OAuth2 Setup

For Gmail integration, you need to set up OAuth2 credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth2 credentials (Desktop application type)
5. Download credentials.json and place it in `~/.email_analyzer/oauth/`
6. See [GMAIL_OAUTH2_SETUP.md](GMAIL_OAUTH2_SETUP.md) for detailed instructions

## 🚀 Usage

### Simple Email Analysis

1. **Enter Your Email**: Simply type your email address in the connection form
2. **Automatic Provider Detection**: The app detects your email provider (Gmail, Outlook, etc.)
3. **Secure Authentication**: 
   - Gmail users: Redirected to Google OAuth2 login
   - Other providers: Use App Password authentication
4. **Analysis**: Choose folders and analysis options
5. **View Results**: Interactive dashboard with charts and insights

### API Usage

```bash
# Start OAuth2 flow for Gmail
POST /api/oauth/gmail/auth/public

# Connect to email account
POST /api/email/connect
{
  "email": "user@example.com"
}

# Start analysis
POST /api/analysis/start
{
  "folder": "INBOX",
  "limit": 1000,
  "include_sentiment": true
}

# Get analysis results
GET /api/analysis/{analysis_id}/results
```

## 🔧 Development

### Backend Development
```bash
# Run the API server
make run

# Format code
make format

# Run tests
make test

# Check code quality
make lint
```

### Frontend Development
```bash
cd web-frontend

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📊 Supported Email Providers

| Provider | Authentication | Status |
|----------|----------------|---------|
| Gmail | OAuth2 | ✅ Fully Supported |
| Outlook/Hotmail | App Password | ✅ Supported |
| Yahoo Mail | App Password | ✅ Supported |
| iCloud | App Password | 🔄 In Progress |
| ProtonMail | App Password | 🔄 In Progress |
| Custom IMAP | Username/Password | ✅ Supported |

## 🔒 Security & Privacy

### Data Protection
- **No Email Storage**: Email content is processed in memory only
- **Secure Authentication**: OAuth2 for Gmail, App Passwords for others
- **HTTPS Enforcement**: All communications encrypted
- **Input Validation**: Comprehensive input sanitization

### Privacy Features
- **Local Processing**: Email analysis happens on your server
- **Configurable Retention**: Control how long analysis data is kept
- **GDPR Compliant**: Built with privacy regulations in mind
- **No Third-party Tracking**: No external analytics or tracking

## 🚀 Future Enhancements

### 🔮 Upcoming Features

#### Authentication & Security
- [ ] **Multi-factor Authentication**: Support for 2FA across all providers
- [ ] **OAuth2 for All Providers**: Extend OAuth2 to Outlook, Yahoo, and others
- [ ] **Enterprise SSO**: SAML/OIDC integration for corporate environments
- [ ] **Role-based Access Control**: User roles and permissions system

#### Analysis & Insights
- [ ] **AI-powered Insights**: Machine learning for email categorization
- [ ] **Spam Detection**: Advanced spam pattern analysis
- [ ] **Email Clustering**: Group similar emails automatically
- [ ] **Predictive Analytics**: Email volume and response time predictions
- [ ] **Language Detection**: Multi-language email analysis
- [ ] **Entity Recognition**: Extract names, companies, and locations

#### User Experience
- [ ] **Real-time Notifications**: WebSocket-based live updates
- [ ] **Email Templates**: Pre-built analysis templates
- [ ] **Custom Dashboards**: User-defined dashboard layouts
- [ ] **Scheduled Analysis**: Automated periodic email analysis
- [ ] **Email Alerts**: Custom alert rules and notifications

#### Advanced Features
- [ ] **Bulk Operations**: Batch email processing and analysis
- [ ] **API Integration**: Third-party service connections (CRM, calendar)
- [ ] **Mobile App**: React Native companion application
- [ ] **Offline Mode**: Local analysis without internet connection
- [ ] **Collaborative Analysis**: Share insights with team members

#### Performance & Scalability
- [ ] **Database Integration**: PostgreSQL for persistent storage
- [ ] **Redis Caching**: Performance optimization with caching
- [ ] **Horizontal Scaling**: Load balancing and clustering
- [ ] **CDN Integration**: Global content delivery
- [ ] **Background Jobs**: Celery/RQ for async processing

#### Export & Integration
- [ ] **Advanced Export Formats**: PowerPoint, Word, and custom formats
- [ ] **API Webhooks**: Real-time data integration
- [ ] **Slack Integration**: Share insights directly to Slack
- [ ] **Email Reports**: Automated email reports and summaries
- [ ] **Calendar Integration**: Email analysis tied to calendar events

### 🎯 Technical Improvements

#### Backend Enhancements
- [ ] **GraphQL API**: Alternative to REST for complex queries
- [ ] **Microservices Architecture**: Service decomposition
- [ ] **Event-driven Architecture**: Message queues and event streaming
- [ ] **Container Orchestration**: Kubernetes deployment
- [ ] **Service Mesh**: Istio for service-to-service communication

#### Frontend Enhancements
- [ ] **Progressive Web App**: Offline capabilities and app-like experience
- [ ] **Server-side Rendering**: Improved SEO and performance
- [ ] **Component Library**: Reusable UI component system
- [ ] **Accessibility**: WCAG 2.1 compliance
- [ ] **Internationalization**: Multi-language support

#### DevOps & Monitoring
- [ ] **Infrastructure as Code**: Terraform/CloudFormation
- [ ] **Observability**: Distributed tracing and monitoring
- [ ] **Chaos Engineering**: Resilience testing
- [ ] **Blue-Green Deployment**: Zero-downtime deployments
- [ ] **Cost Optimization**: Resource usage monitoring and optimization

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `make test`
5. Format your code: `make format`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write comprehensive tests
- Update documentation
- Follow conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check the API docs at `/docs`
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Ask questions and share ideas in GitHub Discussions

### Common Issues
- **OAuth2 Errors**: Check Google Cloud Console configuration
- **Connection Issues**: Verify email provider settings and app passwords
- **Analysis Failures**: Check email account permissions and API limits

## 🙏 Acknowledgments

- **FastAPI** team for the excellent web framework
- **Next.js** team for the React framework
- **Google** for Gmail API and OAuth2
- **Open Source Community** for the amazing tools and libraries

---

**Built with ❤️ using FastAPI and Next.js**

*Email Box Analyzer - Transform your inbox into insights* 