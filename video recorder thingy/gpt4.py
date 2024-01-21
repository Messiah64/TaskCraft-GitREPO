import openai

from datetime import datetime


# Set your OpenAI API key
openai.api_key = "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"

def generate_schedule_planner_response(transcripted_text):

    # Get the current date and time
    current_datetime = datetime.now()
    # Format the date and time as strings
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M:%S")


    # Define the conversation messages
    messages = [
        {"role": "system", "content":  "ct output"},
        {"role": "user", "content": f"Current time is: {formatted_time}, Current date is: {formatted_date}" + transcripted_text},
    ]

    # Call OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=2048,
        messages=messages,
    )

    # Extract and return the content of the generated response
    generated_response = response["choices"][0]["message"]["content"]
    return generated_response

# Example usage:
transcripted_text = "I need to finish my math homework by 8 pm today. I have 10 calculus questions to do. I have to sweep the floor and do the dishes soon, and need my parents' signature on a consent form for tomorrow's school trip"

response = generate_schedule_planner_response(transcripted_text)
print(response)
