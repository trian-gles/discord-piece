import json
import detectlanguage

detectlanguage.configuration.api_key = "KEY"

with open('nationalities.json') as nat_file:
    nats = json.load(nat_file)

with open('all_genres.json') as gen_file:
    unfilt_gens = json.load(gen_file)

def check_nat(genre):
    for nat in nats:
        if nat.lower() in genre.lower():
            print(genre + " is ethnic and a bad idea")
            return True

def check_spanish(genre):
    try:
        language = detectlanguage.detect(genre)[0]['language']
    except IndexError:
        return False
    if  language == 'es':
        print(genre + " is spanish not a good idea")
        return True

filt_gens = []

for gen in unfilt_gens:
    if check_spanish(gen) or check_nat(gen):
        continue
    filt_gens.append(gen)


with open('filt_genres.json', 'w') as filt_file:
    json.dump(filt_gens, filt_file)
