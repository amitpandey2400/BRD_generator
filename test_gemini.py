import google.generativeai as genai

genai.configure(api_key='AIzaSyDB5M8VauAsnbllkoWTzGZ1b4XZM3WLzw8')

print("Available Gemini models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  {m.name}")
