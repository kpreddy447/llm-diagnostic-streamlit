from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import base64
import pandas as pd

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def compare_images(img1_path, img2_path, start_date_1=None, end_date_1=None, start_date_2=None, end_date_2=None):
    img1_b64 = image_to_base64(img1_path)
    img2_b64 = image_to_base64(img2_path)

    prompt = f"""
You are an API analyst reviewing performance logs.

Each chart contains:
- API status logs over time (Success vs Failure)
- Y-axis = latencyMs
- X-axis = timestamp

### Columns in dataset:
- timestamp, sessionId, userId, apiEndpoint, operation, status, httpStatusCode, durationMs, latencyMs, error, browser, os, screenResolution

### Period 1: {start_date_1} to {end_date_1}
### Period 2: {start_date_2} to {end_date_2}

### Tasks:
1. Identify days or hours with latency spikes and status=Failure.
2. Compare errors between both time ranges.
3. Suggest patterns like browser type or endpoint causing issues.
4. Highlight consistent failure types like QuotaExceeded or 5xx.

### Output:
- Markdown table comparison
- 3–5 factual bullet points with diagnosis

Do not hallucinate. Be specific. 
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a data expert specializing in API diagnostics."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img1_b64}" }},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img2_b64}" }}
                ]
            }
        ],
        max_tokens=1200
    )

    return response.choices[0].message.content
