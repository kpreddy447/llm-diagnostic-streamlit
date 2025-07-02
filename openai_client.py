from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def compare_images(img1_path, img2_path, df1, df2, status, start_date_1, end_date_1, start_date_2, end_date_2):
    img1_b64 = image_to_base64(img1_path)
    img2_b64 = image_to_base64(img2_path)

    def summarize(df):
        return df[df['status'].str.lower() == status.lower()]\
            .groupby(['operation', 'browser', 'os'])\
            .size().reset_index(name='count').to_string(index=False)

    df1_summary = summarize(df1)
    df2_summary = summarize(df2)

    prompt = f"""
You are a diagnostic AI assistant specializing in API telemetry.

You're given:
- 2 line charts representing `{status}` counts per day for two distinct time periods.
- Summarized data for each period grouped by `operation`, `browser`, and `os`.

### Period 1: {start_date_1.date()} to {end_date_1.date()}
### Period 2: {start_date_2.date()} to {end_date_2.date()}

### Data Summary (Only for status = {status}):

#### Period 1:
{df1_summary}

#### Period 2:
{df2_summary}

### Your Tasks:
1. Identify dates where `{status}` counts differ significantly (>30%) between periods.
2. Analyze and explain possible causes for the differences using operation, browser, or OS patterns.
3. Avoid any guesses. Use only visible evidence.

Format your answer as:
- A short comparison table
- 3–5 bullet points explaining observed trends
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a reliable API diagnostics assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img1_b64}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img2_b64}"}}
                ]
            }
        ],
        max_tokens=1400
    )

    return response.choices[0].message.content


# from openai import AzureOpenAI
# from dotenv import load_dotenv
# import os
# import base64
# import pandas as pd

# load_dotenv()

# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
# )

# def image_to_base64(path):
#     with open(path, "rb") as f:
#         return base64.b64encode(f.read()).decode("utf-8")

# def compare_images(img1_path, img2_path, start_date_1=None, end_date_1=None, start_date_2=None, end_date_2=None):
#     img1_b64 = image_to_base64(img1_path)
#     img2_b64 = image_to_base64(img2_path)

#     prompt = f"""
# You are an API analyst reviewing performance logs.

# Each chart contains:
# - API status logs over time (Success vs Failure)
# - Y-axis = latencyMs
# - X-axis = timestamp

# ### Columns in dataset:
# - timestamp, sessionId, userId, apiEndpoint, operation, status, httpStatusCode, durationMs, latencyMs, error, browser, os, screenResolution

# ### Period 1: {start_date_1} to {end_date_1}
# ### Period 2: {start_date_2} to {end_date_2}

# ### Tasks:
# 1. Identify days or hours with latency spikes and status=Failure.
# 2. Compare errors between both time ranges.
# 3. Suggest patterns like browser type or endpoint causing issues.
# 4. Highlight consistent failure types like QuotaExceeded or 5xx.

# ### Output:
# - Markdown table comparison
# - 3–5 factual bullet points with diagnosis

# Do not hallucinate. Be specific. 
# """

#     response = client.chat.completions.create(
#         model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
#         messages=[
#             {"role": "system", "content": "You are a data expert specializing in API diagnostics."},
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt},
#                     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img1_b64}" }},
#                     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img2_b64}" }}
#                 ]
#             }
#         ],
#         max_tokens=1200
#     )

#     return response.choices[0].message.content
