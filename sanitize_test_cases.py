import json
import os
import openai
from datetime import datetime
import glob

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

def get_most_recent_file():
    """
    Get the most recently created file in the combined_test_cases directory.
    """
    files = glob.glob('combined_test_cases/*.jsonl')
    if not files:
        return None
    return max(files, key=os.path.getctime)

def sanitize_email_content(content):
    """
    Sanitize email content using OpenAI API to extract only the clean email content.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an email content extractor. Extract only the clean email content from the given text, removing signatures, disclaimers, and any other non-essential parts. Return only the clean email content."},
                {"role": "user", "content": content}
            ],
            max_tokens=1000,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error sanitizing content: {e}")
        return content  # Return original content if sanitization fails

def sanitize_test_cases(file_path):
    """
    Process a combined test cases file, sanitize all Output values, and create a new file.
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return
    
    print(f"Processing file: {file_path}")
    
    # Read the input file
    test_cases = []
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            if line.strip():  # Skip empty lines
                test_cases.append(json.loads(line))
    
    # Sanitize each Output value
    for i, test_case in enumerate(test_cases):
        print(f"Sanitizing test case {i+1}/{len(test_cases)}...")
        test_case["Output"] = sanitize_email_content(test_case["Output"])
    
    # Create output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.basename(file_path)
    name_parts = os.path.splitext(base_name)
    output_filename = f"{name_parts[0]}_sanitized_{timestamp}{name_parts[1]}"
    output_path = os.path.join('combined_test_cases', output_filename)
    
    # Write the sanitized test cases to a new file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for test_case in test_cases:
            json_line = json.dumps(test_case, ensure_ascii=False)
            outfile.write(json_line + '\n')
    
    print(f"Sanitized test cases have been saved to {output_path}")

if __name__ == "__main__":
    # Get the most recent file
    file_path = get_most_recent_file()
    if file_path:
        sanitize_test_cases(file_path)
    else:
        print("No .jsonl files found in the combined_test_cases directory.") 