import requests
import time

def parse_request_and_execute(prompt, url, headers, options_dict, max_retries=5, delay=5):
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "options": options_dict
            }
        ]
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)
            response.raise_for_status()  # Check for HTTP errors
            return response  # return the server response
        except Exception as e:
            print(f"Request attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("Max retries reached. Returning empty result.")
                return {}
            time.sleep(delay)  # wait before retrying