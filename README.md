# Email Test Case Processor

This repository contains scripts for processing email test cases.

## Scripts

### 1. combine_test_cases.py

This script combines individual test case JSON files into a single JSONL file.

**Usage:**
```
python combine_test_cases.py
```

The script will:
- Create a directory called `combined_test_cases` if it doesn't exist
- Combine all test case files from the `testfilesetmaildrafter` directory
- Create a new JSONL file with a timestamp in the name

### 2. sanitize_test_cases.py

This script sanitizes the Output values in a combined test cases file using the OpenAI API.

**Usage:**
```
python sanitize_test_cases.py
```

The script will:
- Prompt you to enter the path to a combined test cases file
- Process each test case and sanitize the Output values using the OpenAI API
- Create a new file with "sanitized" in the name containing the updated content

## Setup

1. Install the required dependencies:
```
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```
export OPENAI_API_KEY=your_api_key_here
```

Or on Windows:
```
set OPENAI_API_KEY=your_api_key_here
```