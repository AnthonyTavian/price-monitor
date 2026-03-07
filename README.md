# Price Monitor

A REST API for monitoring Amazon Brazil product prices using web scraping, automated scheduling, and Telegram notifications.

## Features

- **Product monitoring** — Register Amazon product URLs and set a target price
- **Automated scraping** — Playwright-based scraper that bypasses Amazon's bot protection
- **Price history** — Full price history stored per product
- **Scheduled checks** — Automatic price verification at configurable intervals
- **Telegram notifications** — Instant alerts when a product reaches its target price
- **JWT authentication** — Secure user authentication with access tokens
- **Automated tests** — 24 tests covering auth and product endpoints
- **CI/CD** — GitHub Actions pipeline running tests on every push

## Tech Stack

- **Python 3.11**
- **FastAPI** — REST API framework
- **PostgreSQL** — Primary database
- **SQLAlchemy** — ORM
- **Playwright** — Web scraping
- **APScheduler** — Background task scheduling
- **Docker & Docker Compose** — Containerization
- **Pytest** — Testing
- **GitHub Actions** — CI/CD

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AnthonyTavian/price-monitor.git
cd price-monitor
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Fill in the environment variables:
```env
DATABASE_URL=postgresql://user:password@db:5432/price_monitor
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=price_monitor
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL_HOURS=6
```

4. Start the application:
```bash
docker-compose up --build
```

5. Access the API docs at `http://localhost:8000/docs`

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/me` | Get current user info |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Add a product to monitor |
| GET | `/products` | List all monitored products |
| GET | `/products/{id}` | Get a specific product |
| PUT | `/products/{id}` | Update product target price |
| DELETE | `/products/{id}` | Remove a product |

### Price History
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/{id}/price-history` | Get full price history for a product |

## How It Works

1. User registers and logs in to receive a JWT token
2. User adds an Amazon product URL with a target price
3. The API immediately scrapes the current price and product name using Playwright
4. APScheduler runs price checks at the configured interval
5. When a product's price drops to or below the target, a Telegram notification is sent
6. All price checks are stored in the price history table

## Running Tests

```bash
docker exec -it price-monitor-api-1 pytest tests/ -v
```

## Project Structure

```
price-monitor/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── routers/         # API route handlers
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   │   ├── scraping_service.py
│   │   ├── scheduler_service.py
│   │   ├── notification_service.py
│   │   ├── product_service.py
│   │   ├── price_history_service.py
│   │   └── user_service.py
│   ├── utils/           # Security and dependencies
│   ├── config.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── test_auth.py
│   └── test_products.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## License

MIT