import pickle
import pandas as pd
import torch
from tqdm.notebook import tqdm


def apply_random(files_path, samples, model, tokenizer, file_name, device, only_load=True):
    
    if only_load:
        rand_values_all = pickle.load(open(files_path + f"{file_name}.pkl", 'rb'))

    else:
        rand_values_all = []

        with torch.no_grad():

            for i in tqdm(range(0, len(samples['text']), 256)):
                
                batch_samples = samples['text'][i:i+256]
                
                inputs = tokenizer(batch_samples, max_length=128, padding='max_length', truncation=True, return_tensors="pt").to(device)
                
                logits = model(**inputs).logits
                predicted_labels = torch.argmax(logits, dim=1).tolist()

                for j, sample in enumerate(batch_samples):
                    tokenized_text = tokenizer.convert_ids_to_tokens(inputs['input_ids'][j].tolist())
                    
                    rand_values_sample = torch.rand(len(tokenized_text)).tolist()
                    predicted_label = predicted_labels[j]
                    
                    rand_values_sample = pd.DataFrame({"Token": tokenized_text, str(predicted_label): rand_values_sample})
                    rand_values_sample = rand_values_sample.sort_values(by=str(predicted_label), ascending=False)
                    
                    rand_values_all.append(rand_values_sample)
                
        pickle.dump(rand_values_all, open(files_path + f"{file_name}.pkl", 'wb'))
        print(f"File '{file_name}' saved.")

    print(f"'{file_name}' file shape:", len(rand_values_all))

    return rand_values_all



            

