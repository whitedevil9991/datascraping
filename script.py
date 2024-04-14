import requests
from bs4 import BeautifulSoup
import pandas as pd
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)
#openai.api_key = 'ap_key' 

urls = [
    'https://www.ci.richmond.ca.us/1404/Major-Projects',
    'https://www.bakersfieldcity.us/518/Projects-Programs',
    'https://www.cityofwasco.org/311/Current-Projects',
    'https://www.eurekaca.gov/744/Upcoming-Projects',
    'https://www.cityofarcata.org/413/Current-City-Construction-Projects'
]

extracted_data = []

for url in urls:
    query = f"Construction and infrastructure projects in California site:{url}"
    
    # response = openai.completions.create(
    #     engine="davinci", 
    #     prompt=query,
    #     max_tokens=50, 
    #     n=1,  # Specify the number of completions to generate
    #     stop=None,  # Specify stop sequences to control response length
    #     temperature=0.7  # Adjust the sampling temperature (higher for more randomness)
    # )

    response = client.chat.completions.create(
    model="IIlama2", 
    prompt=query,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

    search_query = response.choices[0].text.strip()
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    projects = soup.find_all('div', class_='project')
    for project in projects:

        title = project.find('h2').text.strip()
        link = project.find('a')['href']
        extracted_data.append({'Title': title, 'Link': link})

# Create DataFrame from extracted data
df = pd.DataFrame(extracted_data)

# Save data
df.to_csv('construction_projects.csv', index=False)

# Display Data
print(df)
