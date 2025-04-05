import json
import requests  # Ensure you have the requests library installed

# Define the URL and API key
base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
api_key = "AIzaSyD_JLFtabbujqdLsmSACpdHOHyTBmHL4fQ"  # Replace with your actual API key

# Construct the full URL with the API key as a query parameter
url = f"{base_url}?key={api_key}"

headers = {
	'Content-Type': 'application/json'
}

# Define the question and context
question = "how are you?"
context = "Hello jay dev"

# Prepare the data payload
data = {
	"contents": [
		{
			"parts": [
				{
					"text": f"Question: {question}\nContext: {context}"
				}
			]
		}
	]
}

# Make the POST request with headers and data
try:
	response = requests.post(url, headers=headers, data=json.dumps(data))
	response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
except requests.exceptions.HTTPError as http_err:
	print(f"HTTP error occurred: {http_err}")
except Exception as err:
	print(f"Other error occurred: {err}")
else:
	# Check if the request was successful
	if response.status_code == 200:
		# Parse the JSON response
		result = response.json()
		# Extract the text from the response
		text = result['candidates'][0]['content']['parts'][0]['text']
		# Print the extracted text
		print(text)
	else:
		print(f"Error: {response.status_code}, Response: {response.text}")