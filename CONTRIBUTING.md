# Contributing to Strategic Risk Monitor

Thank you for your interest in contributing to the Strategic Risk Monitor! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git
- Basic understanding of Flask and financial markets

### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment
4. Install dependencies
5. Set up environment variables
6. Run the application

```bash
git clone https://github.com/yourusername/strategic-risk-monitor.git
cd strategic-risk-monitor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py
```

## 🤝 How to Contribute

### Types of Contributions
- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Submit pull requests
- **Documentation**: Improve guides and documentation
- **Testing**: Add test coverage

### Reporting Bugs
1. Check existing issues first
2. Use the bug report template
3. Include steps to reproduce
4. Provide system information
5. Add screenshots if applicable

### Suggesting Features
1. Check existing feature requests
2. Use the feature request template
3. Explain the use case
4. Describe the proposed solution
5. Consider implementation complexity

### Code Contributions

#### Before You Start
1. Check open issues and discussions
2. Create an issue if one doesn't exist
3. Wait for maintainer feedback
4. Fork the repository

#### Development Workflow
1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Update documentation
5. Commit with clear messages
6. Push to your fork
7. Create a pull request

#### Branch Naming
- Feature: `feature/description`
- Bug fix: `bugfix/description`
- Documentation: `docs/description`
- Refactor: `refactor/description`

#### Commit Messages
Use clear, descriptive commit messages:
```
feat: add ML model performance tracking
fix: resolve dashboard chart rendering issue
docs: update API documentation
refactor: simplify risk calculation logic
```

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Project Structure
```
strategic-risk-monitor/
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── models.py             # Database models
├── routes.py             # Main API routes
├── simple_routes.py      # Simplified routes
├── monitoring.py         # Background monitoring
├── services/             # Business logic services
│   ├── data_collector.py
│   ├── risk_calculator.py
│   ├── alert_system.py
│   └── ml_integration.py
├── templates/            # HTML templates
├── static/              # CSS, JS, images
└── tests/               # Test files
```

### Adding New Features

#### Data Sources
1. Create a new method in `DataCollector`
2. Add error handling and fallbacks
3. Update risk calculation if needed
4. Add tests for the new data source

#### ML Models
1. Add model training in `ml_trainer.py`
2. Update prediction logic in `ml_integration.py`
3. Add model evaluation metrics
4. Document model parameters

#### Alert Channels
1. Create new alerter in `services/`
2. Follow existing pattern (email, discord, telegram)
3. Add configuration options
4. Test alert delivery

#### API Endpoints
1. Add route to appropriate file
2. Include proper error handling
3. Add input validation
4. Document endpoint behavior

### Testing
- Write unit tests for new functionality
- Test error conditions and edge cases
- Ensure existing tests still pass
- Add integration tests for complex features

### Documentation
- Update README.md for significant changes
- Add docstrings to new functions
- Update API documentation
- Include usage examples

## 🔧 Development Environment

### Required APIs for Testing
- GEMINI_API_KEY (free tier available)
- REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET (free)
- NEWSAPI_KEY (free tier: 1000 requests/day)
- FRED_API_KEY (free, unlimited)

### Optional APIs
- Email configuration for alert testing
- Discord webhook for notification testing
- Telegram bot for message testing

### Development Tools
- Flask development server
- SQLite for local database
- pytest for testing
- Black for code formatting
- Flake8 for linting

## 📝 Pull Request Process

### Before Submitting
1. Test your changes thoroughly
2. Update documentation
3. Add tests if needed
4. Ensure code follows style guidelines
5. Commit with clear messages

### PR Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Linked to relevant issue

### Review Process
1. Automated tests run
2. Code review by maintainers
3. Feedback and iterations
4. Final approval
5. Merge to main branch

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority-high`: Critical issues
- `priority-low`: Nice to have

## 📞 Getting Help

### Communication Channels
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Code Comments: Technical implementation questions

### Questions and Support
- Check existing issues and discussions first
- Be specific about your problem
- Include relevant code snippets
- Provide context about your use case

## 🎯 Contribution Areas

### High Priority
- Bug fixes for existing functionality
- Performance optimizations
- Test coverage improvements
- Documentation updates

### Medium Priority
- New data source integrations
- Additional ML models
- UI/UX improvements
- Mobile responsiveness

### Low Priority
- Advanced analytics features
- Integration with more services
- Experimental features
- Alternative visualizations

## 🏆 Recognition

Contributors will be:
- Listed in the README.md
- Acknowledged in release notes
- Invited to join the maintainer team (for significant contributions)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Strategic Risk Monitor! Your efforts help create better financial risk monitoring tools for everyone.