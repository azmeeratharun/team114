from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("ibm-granite/granite-3.3-2b-instruct")
model = AutoModelForCausalLM.from_pretrained("ibm-granite/granite-3.3-2b-instruct")
qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_answer(relevant_chunks, question):
    context = "\n".join(relevant_chunks)
    prompt = (
        f"Use the following context to answer the question.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    
    # Use max_new_tokens to avoid max_length warning
    output = qa_pipeline(prompt, max_new_tokens=512, do_sample=False)
    return output[0]["generated_text"]