# Hedera Account Transaction Sync

This Python script provides a reliable way to sync and store transactions for a specified Hedera account. It uses the Hedera Mirror Node API to fetch transactions and stores them locally in a JSON file.

## Features

- Continuous syncing of transactions for a specified Hedera account
- Resilient to network issues and rate limiting with built-in retry mechanism
- Handles large transaction volumes, fetching all new transactions even if more than 100 occur between syncs
- Stores transactions locally in a JSON file for easy access and backup
- Logs sync activities with timestamps

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone this repository:
2. replace '0.0.626047' with the target account id
