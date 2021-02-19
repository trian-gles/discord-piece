import json

with open('nationalities.json') as nat_file:
    nats = json.load(nat_file)

with open('all_genres.json') as gen_file:
    unfilt_gens = json.load(gen_file)

def check_nat(genre):
    for nat in nats:
        if nat.lower() in genre.lower():
            print(genre + " is a bad idea")
            return True

filt_gens = []

for gen in unfilt_gens:
    if not check_nat(gen):
        filt_gens.append(gen)


with open('filt_genres.json', 'w') as filt_file:
    json.dump(filt_gens, filt_file)
    pass
