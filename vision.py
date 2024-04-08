import requests
import re
import base64

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # Read the file
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')



def fill_context_with_vision(path):
    encoded_image = convert_image_to_base64(image_path=path)
    fill_context_with_vision_prompt = """
You are tasked with analyzing a screenshot of a web page, focusing on the elements encased within bounding boxes. Your primary objective is to identify and extract the atomic functionality associated with these elements. Should there be any uncertainty regarding their functionality, your role shifts to detailing the visual features of these elements.
Guidelines:
Bounding Box Recognition: Accurately identify the UI elements highlighted with red bounding boxes, focusing exclusively on these elements.
Index Identification: Note the index number displayed inside each bounding box. This index will serve as the key for the corresponding element in the output JSON.
Functionality Description: Provide a description of each element's functionality or intended user interaction. If an element's function is unclear, describe its appearance.
Output Formatting: Your output should be a well-structured JSON object. Each key is an index number from the image, and its value is the associated element's functional description or visual description if the functionality is unknown.
"""
    GPT4V_KEY = "d333f752996f4219ba6bc8f56a964980"
    headers = {
        "Content-Type": "application/json",
        "api-key": GPT4V_KEY,
    }


    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"{fill_context_with_vision_prompt}"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                            "detail": "high"
                        }
                    }
                ]
            },
        ],
        "max_tokens": 800,
        "temperature": 0.0,
        "top_p": 0.95
    }

    GPT4V_ENDPOINT = "https://auteur-westus.openai.azure.com/openai/deployments/gpt4-vision/chat/completions?api-version=2024-02-15-preview"
    try:
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    response = response.json()['choices'][0]['message']['content']
    pattern = r'\{[\s\S]*?\}'
    match = re.search(pattern, response)

    return match[0]