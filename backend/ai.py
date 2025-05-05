import openai
import json

# OpenAI Client with Secure API Key
client = openai.OpenAI(api_key="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")  # Replace with your actual key

def nlp_to_json(user_input):
    system_prompt = """ You are an AI that converts user requests into structured JSON API calls.

Follow this format:
{
    "location": "string (required, default: '1908 San Antonio Street, Austin, TX')",
    "max_calories": "integer (optional, default: 800, assuming average meal)",
    "min_protein": "integer (optional, default: 15, assuming a moderate protein goal)",
    "radius_search": "integer (optional, default: 2000, assuming a short drive/bike range)",
    "sort_by": "string (optional, values: 'calories', 'protein', or None)"
}
### **Default Values**
- If a user wants **walking** distance → `radius_search: 1000`
- If a user wants **biking** distance → `radius_search: 2000`
- If a user wants **driving** distance → `radius_search: 10000`
- If the user does **not specify**, use `radius_search: 2000`.

### **Default Values**  
If the user does not specify a field, use:
- `max_calories: 8000` (Assumes they want a reasonable meal size)
- `min_protein: 15` (Moderate protein intake)
- `radius_search: 2000` (2 km for walking/biking)
- `sort_by`: Do **not** assume a sort unless specified.

If a user wants fewer restrictions, **increase the max_calories** or **lower min_protein**.
If they want healthier meals, **lower max_calories** or **raise min_protein**.

---

### **Examples & AI Responses**

#### **1️ User: "Find me a high-protein meal nearby."**
➡ **JSON Response**
```json
{
    "location": "1908 San Antonio Street, Austin, TX",
    "max_calories": 800,
    "min_protein": 30,
    "radius_search": 2000
}


    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        response_format={"type": "json_object"}  # ✅ Corrected value
    )

    # Convert AI response to JSON
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        response_format={"type": "json_object"}  # ✅ Fixed format
    )

    json_request = response.choices[0].message.content  # Extract JSON response
    json_request = json.loads(json_request)  # Convert to dictionary

    return json_request