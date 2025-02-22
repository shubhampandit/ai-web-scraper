import json
import asyncio
from typing import List, Optional, Dict, Any
import google.generativeai as genai
from groq import Groq
from config import (
    GEMINI_API_KEY,
    GROQ_API_KEY,
    GROQ_MODEL,
    GEMINI_MODEL
)
import llm_prompts

# Initialize clients
genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

async def fetch_urls_using_llm(first_page_url: str, num_pages: int) -> List[str]:
    try:
        completion = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model=GROQ_MODEL,
            messages=[{
                "role": "user", 
                "content": llm_prompts.get_urls_prompt(first_page_url, num_pages)
            }],
            temperature=0.6,
            max_completion_tokens=7100,
            top_p=0.95,
            stream=False,
            stop=None,
        )
        
        urls = [first_page_url] + completion.choices[0].message.content.strip().split(',')
        return urls[:num_pages]
    except Exception as e:
        print(f"Error fetching URLs from LLM: {e}")
        return [first_page_url]

async def get_next_url(current_url: str) -> Optional[str]:
    try:
        completion = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model=GROQ_MODEL,
            messages=[{
                "role": "user", 
                "content": llm_prompts.get_next_url_prompt(current_url)
            }],
            temperature=0.6,
            max_completion_tokens=7100,
            top_p=0.95,
            stream=False,
            stop=None,
        )
        
        next_url = completion.choices[0].message.content.strip()
        return next_url if next_url and next_url.lower() != "null" else None
    except Exception as e:
        print(f"Pagination error: {str(e)}")
        return None

async def process_content_with_gemini(content: str, data_points: List[str]) -> Dict[str, Any]:
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config=generation_config,
    )

    try:
        response = await asyncio.to_thread(
            model.start_chat().send_message,
            llm_prompts.get_crawler_prompt(content, data_points)
        )
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"data": []}