# Installation Guide

This guide will walk you through the process of setting up a Python virtual environment and running a faucet claimer.

## Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- Python 3. (You can download it from [Python.org](https://www.python.org/downloads/))
- > [!IMPORTANT]
> THIS SCRIPT WORKS ONLY ON PYTHON VERSION 3.11

## Step 1: Clone the Repository

Clone the repository containing the Python script to your local machine:

```bash
git clone https://github.com/BlathanAevon/berachain_faucet_claimer.git
```

```bash
cd berachain_faucet_claimer
```

## Step 2: Configure Environment Variables

To run your Python script, you may need to configure environment variables with sensitive information or configuration settings. We'll start by copying an `.env_template` file and filling it with the required information.

1. Locate the `.env.example` and rename it to `.env`:

```env
# .env

CAPSOLVER_KEY = capsolver.com key

```

2. Rename `data.example` to `data`. Set all the neccesary data in `data/wallets.txt` and `data/proxies.txt`

<br>

> [!IMPORTANT]
> Proxies should be in format `http://login:pass:ip:port`

## Step 3: Run the Python Script

On Windows:
```bash
.\run.bat
```
On Linux/MacOS:
```bash
./run.sh
```
