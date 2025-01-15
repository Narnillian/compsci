import random

verbs = ["Leverage", "Sync", "Target", "Gamify", "Offline", "Crowd-sourced", "24/7", "Lean-in", "30,000 foot"]
adjectives = ["A/B Tested", "Freemium", "Hyperlocal", "Siloed", "B-to-B", "Oriented", "Cloud-based", "API-based"]
participials = ["Groundbreaking", "Amazing", "Game-changing", "Gratifying", "Community-building", "Innovative"] #I guess they're not all participials because of "Innovative" -- no big deal
nouns = ["Early Adopter", "Low-hanging Fruit", "Pipeline", "Splash Page", "Productivity", "Process", "Tipping Point", "Paradigm"]

myverb = random.choice(verbs)
myadjective = random.choice(adjectives)
myparticipial = random.choice(participials)
mynoun = random.choice(nouns)

phrase = f'{myverb} {myadjective}, {myparticipial} {mynoun}'

print("-I heard you're starting a new company! What will it do?\n")
print("-" + phrase)
