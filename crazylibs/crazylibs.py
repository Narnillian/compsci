from random import choice as randchoice

text = ""
adjectives = []
nouns = []
verbs = []
verb_ings = []
proper_nouns = []
adjectives_all = []
nouns_all = []
verbs_all = []
verb_ings_all = []
proper_nouns_all = []

#`with` automatically closes the file afterwards. check with `story.closed`
with open("story.txt") as story:
    text = story.read()

for token_list in ["neriya","malia","josh","tomomi","rami"]:
    print(token_list.capitalize()+":")
    with open(token_list+".txt") as words:
        for line in words:
            parts = line.split(maxsplit=1)
            parts[1] = parts[1].strip()
            match parts[0].lower():
                case "adjective":
                    adjectives.append(parts[1])
                case "noun":
                    nouns.append(parts[1])
                case "verb":
                    verbs.append(parts[1])
                case "verb_ing":
                    verb_ings.append(parts[1])
                case "proper_noun":
                    proper_nouns.append(parts[1])
                case _:
                    print("ERR: BAD TOKEN IN LIST")
                    print(line)
                    exit(9)
    story = text.split()
    for index,item in enumerate(story):
        #print(item)
        if "{" in item:
            beginning = item[:item.find("{")]
            middle = ""
            end = item[item.find("}")+1:]
            #print(item[item.find("{")+1:item.find("}")-1])
            match item[item.find("{")+1:item.find("}")].lower():
                case "adjective":
                    middle = randchoice(adjectives)
                case "noun":
                    middle = randchoice(nouns)
                case "verb":
                    middle = randchoice(verbs)
                case "verb_ing":
                    middle = randchoice(verb_ings)
                case "proper_noun":
                    middle = randchoice(proper_nouns)
                case _:
                    print("ERR: BAD TOKEN IN STORY")
                    exit(9)
            #for i in item[::-1]: #i don't need this anymore but it's cool so i'll keep it
            story[index] = beginning+middle+end
    story = ' '.join(story) #list --> string
    print(story+"\n")
    try:
        output = open("OUTPUT/crazy_libs.txt","x")
    except:
        output = open("OUTPUT/crazy_libs.txt", "a")
    finally:
        output.write(token_list.capitalize()+":\n")
        output.write(story+"\n\n")
    output.close()
    for i in adjectives: adjectives_all.append(i)
    adjectives = []
    for i in nouns: nouns_all.append(i)
    nouns = []
    for i in verbs: verbs_all.append(i)
    verbs = []
    for i in verb_ings: verb_ings_all.append(i)
    verb_ings = []
    for i in proper_nouns: proper_nouns_all.append(i)
    proper_nouns = []

print("All:")
story = text.split()
for index,item in enumerate(story):
    #print(item)
    if "{" in item:
        beginning = item[:item.find("{")]
        middle = ""
        end = item[item.find("}")+1:]
        #print(item[item.find("{")+1:item.find("}")-1])
        match item[item.find("{")+1:item.find("}")].lower():
            case "adjective":
                middle = randchoice(adjectives_all)
            case "noun":
                middle = randchoice(nouns_all)
            case "verb":
                middle = randchoice(verbs_all)
            case "verb_ing":
                middle = randchoice(verb_ings_all)
            case "proper_noun":
                middle = randchoice(proper_nouns_all)
            case _:
                print("ERR: BAD TOKEN IN STORY")
                exit(9)
        #for i in item[::-1]: #i don't need this anymore but it's cool so i'll keep it
        story[index] = beginning+middle+end
story = ' '.join(story)
print(story)
try:
    output = open("OUTPUT/crazy_libs.txt","x")
except:
    output = open("OUTPUT/crazy_libs.txt", "a")
finally:
    output.write("All:\n")
    output.write(story+"\n")
    output.write("-----\n\n")
