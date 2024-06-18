# Installation Guide

This guide will walk you through the process of setting up a Python virtual environment and running a Python script.

## Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- Python 3.x (You can download it from [Python.org](https://www.python.org/downloads/))

## Step 1: Clone the Repository

Clone the repository containing the Python script to your local machine:

```bash
git clone https://github.com/BlathanAevon/berachain_faucet_claimer.git
```

```bash
cd berachain_faucet_claimer
```

## Step 2: Create a Virtual Environment

It's a good practice to create a virtual environment to isolate your project dependencies. To create a virtual environment, run the following command:

```bash
python3 -m venv venv
```

## Step 3: Activate the Virtual Environment

Activate the virtual environment you created in the previous step. The activation process depends on your operating system:

- On macOS and Linux, use the following command:

  ```bash
  source venv/bin/activate
  ```

- On Windows, use the following command:

  ```
  .\venv\Scripts\activate
  ```

## Step 4: Install Dependencies

To ensure your Python script has access to the required packages and libraries, you need to install the project dependencies. You can do this using `pip`, Python's package manager.

Navigate to your project directory (where the script and the virtual environment are located) in your command prompt or terminal. Then, run the following command:

```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

To run your Python script, you may need to configure environment variables with sensitive information or configuration settings. We'll start by copying an `.env_template` file and filling it with the required information.

1. Locate the `.env.example` and rename it to `.env`:

```env
# .env

CAPSOLVER_KEY = capsolver.com key

```

2. Rename `data.example` to `data`. Set all the neccesary data in `data/wallets.txt` and `data/proxies.txt`
<br>

> [!IMPORTANT]
> proxies should be in format `http://login:password:ip:port`

## Step 6: Run the Python Script

Now that you have set up your virtual environment and installed the necessary dependencies, you can run your Python script.

Navigate to your project directory (where the script is located) in your command prompt or terminal. Then, use the following command to execute your Python script:

```bash
python main.py
```
