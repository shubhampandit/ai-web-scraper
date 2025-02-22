def get_crawler_prompt(markdown_content, data_points):
    """Generate a structured prompt for LLM-based data extraction."""
    data_points_str = ", ".join(data_points)
    return f"""You are an expert in text parsing and structured data extraction. Given a Markdown document, extract the required data points and return them as a structured JSON array.

### **Instructions:**  
1. The input will be a **Markdown document** containing multiple entities/products/elements.  
2. You need to extract **all the data points** explicitly mentioned by the user.  
3. Each entity should be represented as an **individual JSON object** in an **array**.  
4. If an entity is missing a requested data point, set its value to **"null"**.  
5. Ensure that all requested data points are present in every JSON object.  
6. Maintain the **exact case** and formatting for values but remove unnecessary whitespace.  
7. The output should be **valid JSON**, properly formatted and indented.  

### **Example Input:**  
#### Markdown Document:  
```
For an example markdown with products containing name, price and category as datapoints, the returned output should strictly follow the format below: 

### **Expected Output:**  
```
"data": [
  {{
    "Name": "Alpha",
    "Price": "$100",
    "Category": "Electronics"
  }},
  {{
    "Name": "Beta",
    "Price": "null",
    "Category": "Home Appliance"
  }},
  {{
    "Name": "Gamma",
    "Price": "$200",
    "Category": "null"
  }}
]
```

### **Additional Notes:**  
- The LLM should infer **structured elements** based on Markdown formatting (headers, lists, bold text, etc.).  
- If a data point exists in different formats (e.g., “Cost” instead of “Price”), **normalize** the field based on the user's request.  
- Preserve the **order of entities** as they appear in the document.  
- Ensure that the JSON output is **syntactically correct and properly escaped**. 
- If you couldn't parse or return anything, please return the following JSON object:
```
{{
  "data": []
}}
``` 

#### **Now, parse the following Markdown document and return the structured JSON output:**  
**Markdown Input:**  
```
{markdown_content}
```
**Requested Data Points:**  
```
{data_points_str}
```
"""

def get_next_url_prompt(current_url: str):
    return f"""Analyze this URL and predict the next page URL focusing on numerical patterns. Return ONLY the URL or 'null':
Current URL: {current_url}
Next URL:"""

def get_urls_prompt(first_page_url, num_pages):
    return f"""
        You are given the URL of the first page in a sequence. Your task is to identify the numeric or structural pattern in the URL and generate the next {num_pages - 1} URLs accordingly.

- If the pattern follows a numeric sequence, increment the number appropriately.
- If the pattern follows a slug-based sequence (e.g., alphabetical or other structured variations), adjust accordingly to generate the next URLs.
- Maintain the same base structure of the URL while only modifying the relevant part that changes sequentially.

Example:
- Input: https://example.com/page1
- Expected Output: https://example.com/page2,https://example.com/page3,https://example.com/page4, ...

Output format:
- Return a plain comma-separated list of URLs.
- Do **not** include any additional text, explanation, or formatting—only the URLs in order.

Input:
First Page URL: {first_page_url}
        """