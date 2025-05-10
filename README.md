# My submission for the Amazon Q Developer Quack The Code Challenge.


# BankNifty Algorithmic Trading System

This project implements an automated trading system for Bank Nifty options using Django as the backend framework and SmartAPI for trading operations. The system is containerized using Docker for easy deployment and management.

## Project Structure

The project consists of two main components:

1. **banknifty_algo**: Django backend application
   - Provides a web interface for configuring trading parameters
   - Manages trading bot execution through Docker containers
   - Stores trade history and configurations

2. **smartapiii**: Trading API integration module
   - Contains the SmartAPI integration for Angel Broking
   - Implements the trading logic and algorithms
   - Packaged for Docker deployment

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Django 3.2+

### Installation Steps
1. Clone the repository
2. Set up environment variables in `env.txt`
3. Build the Docker containers: `docker build -t drishangupta/drishanguptapvt:v6 .`
4. Start the Django server: `python manage.py runserver`

## Usage

1. Access the web interface at http://localhost:8000
2. Configure trading parameters (symbols, entry/exit points, etc.)
3. Start the trading bot
4. Monitor trades through the dashboard

## Features

- Automated options trading for Bank Nifty
- Real-time market data streaming
- Configurable entry/exit strategies
- Stop-loss and target management
- Trade history tracking
- Emergency kill switch

## Security

This repository has been carefully sanitized to remove all personally identifiable information (PII) and sensitive credentials:
- All API keys and credentials have been replaced with placeholders
- Environment files contain only placeholder values
- A comprehensive .gitignore file prevents accidental exposure of sensitive data

## Development

This project was developed with assistance from Amazon Q, which helped with:
- Code optimization and refactoring
- Docker configuration
- API integration
- Debugging and troubleshooting
- Best practices implementation
- Security review and implementation

For a detailed breakdown of Amazon Q's contributions, see [AmazonQ.md](AmazonQ.md).

## License

This project is proprietary and confidential.
