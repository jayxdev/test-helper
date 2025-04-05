import google.generativeai as genai
from src.settings import api_key

def setup():
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model
def generate(model,text):
    response = model.generate_content(text)
    return response.text    

if __name__ == "__main__":
    model=setup()
    response = generate(model,"extract mcq and return only answer to the mcq question")
    print(response)
