# Contributing to Email Box Analyzer 🤝

Thank you for your interest in contributing to Email Box Analyzer! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **🐛 Bug Reports**: Report issues you encounter
- **💡 Feature Requests**: Suggest new features or improvements
- **📝 Documentation**: Improve or add documentation
- **🔧 Code Contributions**: Submit pull requests with code changes
- **🧪 Testing**: Help test the application and report issues
- **🌐 Translations**: Help translate the application to other languages

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- Git
- Basic knowledge of FastAPI and React/Next.js

### Development Setup

1. **Fork the Repository**
   ```bash
   git clone https://github.com/jay739/email-box-analyzer.git
   cd email-box-analyzer
   ```

2. **Set Up Backend**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up OAuth2 credentials (for Gmail testing)
   mkdir -p ~/.email_analyzer/oauth
   # Add your credentials.json file here
   ```

3. **Set Up Frontend**
   ```bash
   cd web-frontend
   npm install
   ```

4. **Start Development Servers**
   ```bash
   # Backend (in one terminal)
   make run
   
   # Frontend (in another terminal)
   cd web-frontend
   npm run dev
   ```

## 📝 Development Guidelines

### Code Style

#### Python (Backend)
- Follow **PEP 8** style guidelines
- Use **Black** for code formatting
- Use **isort** for import sorting
- Maximum line length: 88 characters (Black default)
- Use type hints for all function parameters and return values

```bash
# Format code
make format

# Check code quality
make lint
```

#### TypeScript/JavaScript (Frontend)
- Use **Prettier** for code formatting
- Follow **ESLint** rules
- Use **TypeScript** for type safety
- Follow React best practices

```bash
cd web-frontend
npm run format
npm run lint
```

### Git Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clear, descriptive commit messages
   - Use conventional commit format: `type(scope): description`
   - Examples:
     - `feat(auth): add OAuth2 support for Outlook`
     - `fix(api): resolve CORS issue with frontend`
     - `docs(readme): update installation instructions`

3. **Test Your Changes**
   ```bash
   # Backend tests
   make test
   
   # Frontend tests
   cd web-frontend
   npm test
   ```

4. **Submit a Pull Request**
   - Create a detailed description of your changes
   - Include any relevant issue numbers
   - Add screenshots for UI changes
   - Ensure all tests pass

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(oauth): add Gmail OAuth2 authentication
fix(api): resolve email connection timeout issue
docs(readme): update installation instructions
style(frontend): format components with Prettier
```

## 🧪 Testing

### Backend Testing
```bash
# Run all tests
make test

# Run specific test file
pytest tests/unit/test_email_analyzer.py

# Run with coverage
pytest --cov=src tests/
```

### Frontend Testing
```bash
cd web-frontend

# Run unit tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests (if configured)
npm run test:e2e
```

### Manual Testing
- Test OAuth2 flows with Gmail
- Test email analysis with different providers
- Test chart generation and export functionality
- Test responsive design on different screen sizes

## 📚 Documentation

### Code Documentation
- Use docstrings for all Python functions and classes
- Use JSDoc for TypeScript/JavaScript functions
- Keep documentation up to date with code changes

### API Documentation
- Update OpenAPI schemas when adding new endpoints
- Add examples for new API endpoints
- Test API documentation at `/docs` endpoint

### User Documentation
- Update README.md for new features
- Add screenshots for UI changes
- Update setup instructions if needed

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Operating system and version
   - Python version
   - Node.js version
   - Browser (for frontend issues)

2. **Steps to Reproduce**
   - Clear, step-by-step instructions
   - Sample data if applicable

3. **Expected vs Actual Behavior**
   - What you expected to happen
   - What actually happened

4. **Additional Information**
   - Error messages and stack traces
   - Screenshots if applicable
   - Console logs

## 💡 Feature Requests

When suggesting features:

1. **Describe the Problem**
   - What problem does this feature solve?
   - Who would benefit from this feature?

2. **Propose a Solution**
   - How should this feature work?
   - Any specific requirements or constraints?

3. **Consider Implementation**
   - Is this feasible with current architecture?
   - Any potential challenges?

## 🔒 Security

### Security Guidelines
- Never commit sensitive information (API keys, passwords, etc.)
- Use environment variables for configuration
- Follow OAuth2 security best practices
- Validate all user inputs
- Use HTTPS in production

### Reporting Security Issues
- **DO NOT** create public issues for security vulnerabilities
- Email security issues to: security@emailboxanalyzer.com
- Include detailed information about the vulnerability
- Allow time for response before public disclosure

## 🏷️ Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `invalid`: Something that isn't a valid issue
- `question`: Further information is requested
- `wontfix`: This will not be worked on

## 🎉 Recognition

Contributors will be recognized in:

- **README.md**: Contributors section
- **Release Notes**: For significant contributions
- **GitHub**: Contributor statistics and profile

## 📞 Getting Help

If you need help with contributing:

1. **Check Documentation**: Read the README and API docs
2. **Search Issues**: Look for similar issues or discussions
3. **Create Discussion**: Use GitHub Discussions for questions
4. **Join Community**: Connect with other contributors

## 📋 Checklist for Pull Requests

Before submitting a pull request, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] No sensitive information is included
- [ ] Changes are tested manually
- [ ] PR description is clear and detailed

## 🚀 Release Process

### For Maintainers

1. **Prepare Release**
   - Update version numbers
   - Update CHANGELOG.md
   - Create release branch

2. **Test Release**
   - Run full test suite
   - Test on different environments
   - Verify documentation

3. **Deploy**
   - Create GitHub release
   - Deploy to production
   - Announce release

---

Thank you for contributing to Email Box Analyzer! 🎉

Your contributions help make email analysis more accessible and powerful for everyone. 