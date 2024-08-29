import pandas as pd
import json
from openai import OpenAI
import os
import sys

client = OpenAI()

system_prompt= """
# Identity:
You are simulating a Secure Shell (SSH) terminal of a server running Debian Jessie on an x86_64 architecture. Assume the user is 'root' and the hostname is 'userdb.verwaltung.uni-halle.de'. Your role is to maintain the persona of an SSH terminal at all times.

# Steps:
1. You will receive shell commands from the user.
2. As the conversation progresses, maintain a history of commands (from the user) and server responses (from you). Use this information to derive the state of the session.
3. Interpret what the command is trying to accomplish and analyze what a server would output if presented with this command.
4. Write and output only what an SSH terminal would output, adhering to the format specified below.

# Output Instructions:
- Output in JSON format.
- Use the key 'content' for your output, with the server's response as the value.
- Follow this format:
  ```json
  {
      \"content\": \"<server output>\"
  }
  ```
- If the output of the server would be empty, provide the json object with an empty content value.
- If the user's command or parts of the command are incorrect, non-existent, or flawed, output all error messages that the server would typically output. Do not stop after the first error message, if a server would output more than that.
- Do not provide comments, running text, or explanations, as an SSH terminal would not offer such outputs.

# Example:
**User:**
ls -l
**Assistant:**
total 8
-rw-r--r-- 1 vagrant vagrant    4 Feb  9 16:22 test2.txt
-rw-rw-r-- 1 vagrant vagrant    4 Feb  9 16:22 test.txt

**User:**
echo 'this is a test' > test3.txt
**Assistant:**

**User Input:**
ls -l
**Expected Output:**
{
    \"content\": \"total 12
-rw-r--r-- 1 vagrant vagrant    4 Feb  9 16:22 test2.txt
-rw-r--r-- 1 vagrant vagrant   15 Feb 27 16:22 test3.txt
-rw-rw-r-- 1 vagrant vagrant    4 Feb  9 16:22 test.txt\"
}

# INPUT:
INPUT:
"""

def load_dataframe_from_excel(file_path):
    return pd.read_excel(file_path)

def find_json_files_for_dataset1(df, json_folder_path):
    request_ids = df[df['dataset-name.1'] == 'halle']['request-id'].tolist()
    json_files = {}
    for file_name in os.listdir(json_folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(json_folder_path, file_name)
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    for item in data:
                        request_id = item['completion-request'][0]['request-id']
                        if request_id in request_ids:
                            for message in item['completion-request'][0]['messages']:
                                if message['role'] == 'system':
                                    message['content'] = system_prompt
                            json_files[request_id] = item
                except json.JSONDecodeError:
                    continue
    return json_files

def query_openai_and_update_df(df, json_files):
    for index, row in df.iterrows():
        if row['dataset-name.1'] == 'halle':
            request_id = row['request-id']
            if request_id in json_files:
                messages = json_files[request_id]['completion-request'][0]['messages']
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        response_format={ "type": "json_object"},
                        max_tokens=3000,
                        messages= messages
                    )
                    resp = response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"Error with request ID {request_id}: {str(e)}")
                    resp = "Error: Maximum context length exceeded. Please reduce the length of the messages."

                print(resp)
                content_items = []
                try:
                    json_resp = json.loads(resp)
                    if 'content' in json_resp:
                        content_items.append(json_resp['content'])
                except json.JSONDecodeError:
                    try:
                        for part in resp.split('\n'):
                            if part.strip():
                                json_part = json.loads(part)
                                if 'content' in json_part:
                                    content_items.append(json_part['content'])
                    except json.JSONDecodeError:
                        content_items = [resp]

                final_content = "\n".join(content_items)
                df.at[index, 'generated-response'] = final_content
    return df

def save_dataframe_to_excel(df, output_file_path):
    df.to_excel(output_file_path, index=False)

def main(excel_file_path, json_folder_path, output_excel_file_path):
    df = load_dataframe_from_excel(excel_file_path)
    json_files = find_json_files_for_dataset1(df, json_folder_path)
    updated_df = query_openai_and_update_df(df, json_files)
    save_dataframe_to_excel(updated_df, output_excel_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <path_to_excel_file> <path_to_json_folder> <output_excel_file_path>")
        sys.exit(1)

    excel_file_path, json_folder_path, output_excel_file_path = sys.argv[1], sys.argv[2], sys.argv[3]
    main(excel_file_path, json_folder_path, output_excel_file_path)

