import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
nb_sentences = 1

# load model and token thing
finetuned_model = AutoModelForCausalLM.from_pretrained("DevidCipher/RPG-Neuro")
tokenizer = AutoTokenizer.from_pretrained("DevidCipher/RPG-Neuro")
tokenizer.pad_token = tokenizer.eos_token

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
finetuned_model.to(device)

chat_history_ids = None


def chatbot(msg):
    global chat_history_ids
    # encode the new user input, add the eos_token, and move to device
    new_user_input_ids = tokenizer.encode(
        msg + tokenizer.eos_token, return_tensors="pt"
    ).to(device)

    # append the new user input tokens to the chat history
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids

    # generate a response while limiting total length
    chat_history_ids = finetuned_model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,  # optional: for more natural responses
        top_p=0.9,
        top_k=50,
        temperature=0.7
    )

    # decode the generated tokens to a string
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )

    return response
