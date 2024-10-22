import groq


def classify_llama(transcript="i feel so bad"):
    client = groq.Client(api_key='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')

    text_to_analyze =transcript

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Analyze the following text and classify its emotion to : sad ,happy , angry , surprised , afraid ,nuetral,optimism , or a compination . return first the expression then the explaianation : '{text_to_analyze}'"

            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    res=""
    for chunk in completion:
        res+=(chunk.choices[0].delta.content or "")
    return res

def main(transcript):
    res = classify_llama(transcript)
    new_res = ''
    for i in range(len(res)):
        new_res += res[i]
        if res[i] == '.':
            new_res += '\n'  # Adds a newline character after each period
    return new_res
