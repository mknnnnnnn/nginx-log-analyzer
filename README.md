# NGINX Log Analyzer

A simple command line tool for parsing, filtering and analyzing NGINX access logs.
Supports combined and common log format with filtering and basic statistics. 

The repository includes example log files that can be used for testing.

## Features

### Parsing
- Combined format
- Common Log Format

### Filtering
- IP address
- User
- HTTP method
- Path substring
- Protocol
- Status / status range
- Bytes / bytes range
- Referrer
- User-Agent
- Time range

### Statistics
- Top IPs
- Top requested paths
- Bytes summary

## Setup - Docker Compose

Clone the repository:
```bash
git clone https://github.com/mknnnnnnn/nginx-log-analyzer.git
cd nginx-log-analyzer
```

Run Docker Compose:
```bash
docker compose run --rm nla --help
```

The local `logs` directory is mounted as `/logs` inside the container.
The local `results` directory is mounted as `/results` inside the container.

### Usage
```bash
docker compose run --rm nla -i /logs -o /results/results.json --format c --ip 127.0.0.1 --show
docker compose run --rm nla -i /logs -o /results/results.json --format c --method POST GET --show
docker compose run --rm nla -i /logs -o /results/results.json --format clf --ip 192.168.1.10 --show
docker compose run --rm nla -i /logs -o /results/results.json --format c --method GET --path /admin /api --show
```

Place NGINX access log files in the `logs` directory. Output files will be saved in the `results` directory.

## Setup - Local

Clone the repository and install the package:

```bash
git clone https://github.com/mknnnnnnn/nginx-log-analyzer.git
cd nginx-log-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip3 install .
```

After the installation the CLI command will be available:
```bash
nla --help
```

### Usage
```bash
nla -i /path/to/logs -o /path/to/results.json --format c --ip 127.0.0.1 --show
nla -i /path/to/logs -o /path/to/results.json --format c --method POST GET --show
nla -i /path/to/logs -o /path/to/results.json --format clf --ip 192.168.1.10 --show
nla -i /path/to/logs -o /path/to/results.json --format c --method GET --path /admin /api --show
```

Place NGINX access log files in the `logs` directory. Output files will be saved in the `results` directory.