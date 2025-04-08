import json
import glob
import os
from datetime import datetime

def combine_test_cases():
    # Create output directory if it doesn't exist
    output_dir = 'combined_test_cases'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all test case files
    test_files = glob.glob('testfilesetmaildrafter/testcase*.json')
    
    # Create filename with datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = os.path.join(output_dir, f'combined_test_cases_{timestamp}.jsonl')
    
    # Process each test file and write to JSONL
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for test_file in test_files:
            with open(test_file, 'r', encoding='utf-8') as infile:
                test_case = json.load(infile)
                
                # Extract all prompt variables into a single string
                input_content = ""
                for var in test_case["promptVariables"]:
                    if var["key"] == "content":
                        input_content = var["value"]
                        break
                
                # Create test case entry
                test_case_entry = {
                    "Input": input_content,
                    "Output": test_case["expectedOutput"]
                }
                
                # Write as a single line to JSONL file
                json_line = json.dumps(test_case_entry, ensure_ascii=False)
                outfile.write(json_line + '\n')
    
    print(f"Test cases have been combined into {output_filename}")

if __name__ == "__main__":
    combine_test_cases() 