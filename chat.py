import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize, correct, remove_accents, stem

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

    
FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]


model = NeuralNet(input_size, num_classes=len(tags)).to(device)

model.load_state_dict(model_state)
model.eval()


bot_name = "Mohammed"




def get_bot_response():
    while True:
        sentence = input("Vous: ")
        if sentence == "quit":
            break
        sentence = tokenize(sentence)
        sentence = correct(sentence)
        sentence = [remove_accents(word) for word in sentence]
        sentence = [word.lower() for word in sentence]
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        else:
            return "Je ne comprends pas ce que vous dites! Veuillez réessayer."