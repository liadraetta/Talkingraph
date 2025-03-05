from transformers import AutoModelForCausalLM, AutoTokenizer
import torch,json

model_name = "numind/NuExtract-tiny-v1.5"
device = "mps"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, trust_remote_code=True).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)


def predict_NuExtract(prompt, template,model=model, tokenizer=tokenizer, max_length=10_000, max_new_tokens=4_000):
    
    prompt = f"""<|input|>\n### Template:\n{template}\n### Text:\n{prompt}\n\n<|output|>"""
    outputs = []
    with torch.no_grad():
        
        batch_encodings = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=max_length).to(model.device)
        pred_ids = model.generate(**batch_encodings, max_new_tokens=max_new_tokens)
        outputs += tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        

    return outputs[0].split("<|output|>")[1]



text = """Trovami tutte le storie horror scritte da scrittori inglesi che parlano di famiglie disfunzionali e sono ambientate ad Abuja"""

template = {
    "QuestionPronoun": "",
    "EntityTypes": {
        "Work": [],
        "Author": [],
        "Genre":[],
        "Topic":[],
        "Location":[]
    }
}

prediction = predict_NuExtract(text,template)

print(prediction)