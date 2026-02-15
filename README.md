# Mosaic Ceramics QQ Bot

A QQ channel bot that serves the Mosaic Ceramics decision analysis data. Built with the official [qq-botpy](https://github.com/tencent-connect/botpy) SDK.

## Features

- `/help` — Show available commands
- `/summary` — Full decision analysis summary (probabilities, EMV, optimal decision, recommendations)
- `/emv` — Expected Monetary Value analysis
- `/payoff` — Payoff matrix
- `/recommend` — Key recommendations

## Setup

### Prerequisites

- Python 3.8+
- A registered QQ Bot with AppID and AppSecret from the [QQ Bot Developer Portal](https://bot.q.qq.com/)

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Copy the example config and fill in your bot credentials:

```bash
cp config.yaml.example config.yaml
```

Edit `config.yaml`:

```yaml
bot:
  appid: "YOUR_APP_ID"
  secret: "YOUR_APP_SECRET"
```

> ⚠️ Never commit `config.yaml` — it contains your bot secret.

### Running the Bot

```bash
python -m qq_bot.bot
```

The bot will connect to QQ and start listening for @mentions in channels.

## Testing

```bash
pip install pytest
python -m pytest tests/ -v
```

## Project Structure

```
├── config.yaml.example     # Configuration template
├── requirements.txt        # Python dependencies
├── Mosaic_Ceramics_Decision_Analysis.csv  # Analysis data
├── qq_bot/
│   ├── __init__.py
│   ├── bot.py              # Main bot entry point
│   ├── config.py           # Configuration loading
│   ├── data_loader.py      # CSV parsing and formatting
│   └── handlers.py         # Command handlers
└── tests/
    ├── test_config.py
    ├── test_data_loader.py
    └── test_handlers.py
```
