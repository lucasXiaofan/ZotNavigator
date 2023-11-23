import json

# Open the JSON file
dir = r"C:\Users\LangZheZR\Documents\GitHub\UniGPT\new_mvp\fake_database\events_data.json"



## user tag
user_tag = ['computer science','first year','interested in machine learning research']

## priority queue and similarity search: 
import openai
import numpy as np
openai.api_key = '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'
def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def similarity_search(string1, string2):
    """Compute the similarity between two strings using OpenAI embeddings."""
    
    # Set your OpenAI API key
    openai.api_key = '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'

    # Get embeddings for the strings
    response = openai.Embedding.create(
        input=[string1, string2],
        engine="text-embedding-ada-002"  # Choose an appropriate engine
    )
    
    # Extract embeddings
    embedding1 = response['data'][0]['embedding']
    embedding2 = response['data'][1]['embedding']

    # Compute cosine similarity
    similarity = cosine_similarity(embedding1, embedding2)

    return similarity

def are_words_similar(word1, word2):
    prompt = f"Are the words '{word1}' and '{word2}' representing the highly relevant concept? Answer with True or False."
    
    response = openai.Completion.create(
      engine="text-davinci-003",  # Specify the GPT-3.5 engine
      prompt=prompt,
      max_tokens=5  # A small number, as we expect a short response
    )

    # Process the response
    answer = response.choices[0].text.strip()
    return answer

# print(similarity_search(','.join(user_tag),'machine learning, natural language processing, student center'))
# print(similarity_search('machine learning','mechanical engineering')) -> .81
print(are_words_similar('Machine learning','physics'))
# with open('./fake_database/events_data.json') as file:
#     # Load the JSON data
#     data = json.load(file)

# priority_queue = {}
# for event in data: 
#     tag = ",".join(event["event_tags"])
#     score = similarity_search(tag,','.join(user_tag))
#     if event["event_name"] not in priority_queue:
#         priority_queue[event["event_name"]] = {'match_score':score,
#                                                'url':event["event_link"],
#                                                'date': event["event_date"],
#                                                'location':event['event_location']}
#     # print(f'tag for {event["event_name"]}: {tag}')
# sorted_priority_queue = sorted(priority_queue.items(), key=lambda x: x[1]['match_score'], reverse=True)
# for k,v in sorted_priority_queue:
#     print(f"{k} and {v['match_score']}")