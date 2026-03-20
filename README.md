# NGINX Log Analyzer

A simple command line tool for parsing, filtering and analyzing NGINX access logs.
Supports combined and common log format with filtering and basic statistics.

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

## Installation

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

## Usage
Set your input directory and output file:
```bash
nla --set-input-path "/Users/User/Desktop/Logs/input/" --set-output-path "/Users/User/Desktop/Logs/output.json"
```

## Example
```bash
nla --format c --method POST GET --show
nla --format clf --ip 192.168.1.10 --show
nla --format c --method GET --path /admin /api --show
```
