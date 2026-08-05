'''
from chunks import chunks
def retrieve(query):
    print(f"검색 Query : {query}")

    return chunks
'''

from chunks import chunks

def retrieve(query):

    result = []

    for chunk in chunks:

        if "Kubernetes" in query and "Kubernetes" in chunk["text"]:
            result.append(chunk)

        elif "Docker" in query and "Docker" in chunk["text"]:
            result.append(chunk)

    return result