'''
def grounding(answer, chunks):

    print("Grounding Check")

    for chunk in chunks:

        if chunk["text"] in answer:

            print("O :", chunk["source"])

        else:

            print("X :", chunk["source"])
'''

def grounding(answer, chunks):

    result = []

    print("Grounding Check")

    for chunk in chunks:

        if chunk["text"] in answer:
            print("O :", chunk["source"])
            result.append((chunk["source"], "O"))

        else:
            print("X :", chunk["source"])
            result.append((chunk["source"], "X"))

    return result