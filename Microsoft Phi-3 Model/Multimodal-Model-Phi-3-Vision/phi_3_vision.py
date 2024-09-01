# -*- coding: utf-8 -*-
"""Phi-3-Vision.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zDNtaz_d665-ue-cwQEncI3zsZQtWy5f

1. Libraries
2. Import Model
3. Import Processor
4. Prompt, import image
5. Inference

## ***Install Required Libraries***
"""

# !pip install numpy==1.24.4 Pillow==10.3.0 Requests==2.31.0 torch==2.3.0 torchvision==0.18.0 transformers==4.40.2

# !pip install accelerate

!mkdir my_models
!mkdir my_models/phi_3_vision

"""## ***Import Phi-3-vision model***"""

from transformers import AutoModelForCausalLM

model_id = "microsoft/Phi-3-vision-128k-instruct"

model = AutoModelForCausalLM.from_pretrained(model_id,
                                             cache_dir="/content/my_models/phi_3_vision",
                                             device_map="cuda",
                                             trust_remote_code=True,
                                             torch_dtype="auto",
                                             _attn_implementation="eager")

# model.config

"""## ***Get the Processor***"""

from transformers import AutoProcessor
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

print(processor.__doc__)

"""## ***Create Prompt***"""

messages = [
    {"role": "user", "content": "<|image_1|>\nProvide OCR for all the text in given image in markdown format."}
]

prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

prompt

"""## ***Fetch Input Image***"""

from PIL import Image
import requests

url = "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/modern-corporate-invoice-sample-design-template-abf94f862ed7e0c2f6c5dc1526029a42_screen.jpg?ts=1698354950"
image = Image.open(requests.get(url, stream=True).raw)
image

"""## ***Convert Inputs to Tokens***"""

inputs = processor(prompt, [image], return_tensors="pt").to("cuda:0")

# inputs

generation_args = {
    "max_new_tokens": 500,
    "temperature": 0.0,
    "do_sample": False,
}

"""## ***Inference***"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# generate_ids = model.generate(**inputs, eos_token_id=processor.tokenizer.eos_token_id, **generation_args)

# remove input tokens
generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

print(response)
