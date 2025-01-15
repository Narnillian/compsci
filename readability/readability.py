import math
import syllapy

algorithms = ["flesch-kincaid", "dale-chall", "smog"]

def compute_dc_difficult_words(text):
    count = 0
    # this isn't perfect but it's close enough. i think false negatives > false positives
    from dale_chall import words as easy_words
    for word in text.split():
        word = word.lower().strip()
        if word[-1] in '.,;!?:)]':
            word = word[:-1]
        if word[0] in '.,;!?:([':
            word = word[1:]
        if len(word) > 3:
            if word[-1] == 's':   word = word[:-1]
            elif len(word) > 4:
                if word[-2:] == 'ed':  word = word[:-2]
                if word[-3:] == 'taking': word = word[:-3]
        # I don't know why the list is type ([""], [""], ... but it is, so we have to work with it)
        if [word] not in easy_words:
            count += 1
    return count

def compute_syllables(word):
    count = 0

    if word[-1] in '.,;!?:)]':
        word = word[:-1]
    if word[0] in '.,;!?:([':
        word = word[1:]
 
    if len(word) < 4: return 1
    
    if word[-1] in 'eE':
        word = word[:-1]

    if word[-1] in 'yY':
        count = count + 1

    prev_was_vowel = False
    for char in word:
        if char in 'aeiouAEIOU':
            if not prev_was_vowel:
                count += 1
            prev_was_vowel = True
        else: prev_was_vowel = False
    return count

def compute_score(words, sentences, syllables, metric,
                  dc_difficult_words=0,
                  smog_difficult_words=0):
    score = 0
    match metric:
        case "flesch-kincaid":
            score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
            if score >= 90: return "5th Grader"
            if score >= 80: return "6th Grader"
            if score >= 70: return "7th Grader"
            if score >= 60: return "8-9th Grader"
            if score >= 50: return "10-12th Grader"
            if score >= 30: return "College Student"
            return "College Graduate"
        case "dale-chall":
            score = 0.1579 * ((dc_difficult_words / words) * 100) + 0.0496 * (words / sentences)
            if (dc_difficult_words / words) * 100 > 5:
                score += 3.6365
            if score <= 4.9: return "4th Grader"
            if score <= 5.9: return "5-6th Grader"
            if score <= 6.9: return "7-8th Grader"
            if score <= 7.9: return "9-10th Grader"
            if score <= 8.9: return "11-12th Grader"
            if score <= 9.9: return "College Student"
            return "College Graduate"
        case "smog":
            score = 1.043 * math.sqrt(smog_difficult_words) * (30 / sentences) + 3.1291
            if score <= 4: return "Elementary School student"
            if score <= 8: return "Middle School student"
            if score <= 12: return "High School Student"
            if score <= 16: return "College Student"
            return "College Graduate"
        case "*":
            score = []
            for metric_listed in algorithms:
                if metric_listed == "dale-chall":
                    score.append(compute_score(words, sentences, syllables, metric_listed, dc_difficult_words))
                elif metric_listed == "smog":
                    score.append(compute_score(words, sentences, syllables, metric_listed, smog_difficult_words=smog_difficult_words))
                else:
                    score.append(compute_score(words, sentences, syllables, metric_listed))
            return score
        case _:
            print("ERR: INVALID METRIC")
            exit(-1)


def compute_readability(text, metric, use_syllapy=False, output=False):	
    total_sentences = 0
    total_words = 0
    dc_difficult_words = 0
    smog_difficult_words = 0
    total_syllables = 0
    total_syllables_syllapy = 0

    for char in [".","!","?"]:
        total_sentences += text.count(char)
    
    words = text.split()
    total_words = len(words)

    for word in words:
        syllables = compute_syllables(word)
        total_syllables += syllables
        if syllables >= 3:
            smog_difficult_words += 1
        total_syllables_syllapy += syllapy.count(word)
    del words # in order to save resources, delete the big variable once unneeded

    if output:
        print("Words:            " + str(total_words))
        print("Sentences:        " + str(total_sentences))
    
    if metric in ["dale-chall", "*"]:
        dc_difficult_words = compute_dc_difficult_words(text)
        if output: print("Difficult words:  " + str(dc_difficult_words))

    if output:
        print("Syllables:        " + str(total_syllables))
        print("Syllables according to SyllaPy: " + str(total_syllables_syllapy), end=" ")
        difference = 1 - (total_syllables / total_syllables_syllapy)
        print("(" + str(round(difference * 100, 2)) + "% difference)")
        print()

    result = ""
    if use_syllapy:
        total_syllables = total_syllables_syllapy
   # if metric is invalid, the program will end inside this function
    result = compute_score(total_words, total_sentences, total_syllables, metric,
                           dc_difficult_words, smog_difficult_words)
    return result

def print_result(result, metric=""):
    if type(result) == list:
        for i in range(len(result)):
            algo = ""
            match algorithms[i]:
                case "flesch-kincaid":
                    algo = "Flesch-Kincaid"
                case "dale-chall":
                    algo = "Dale-Chall"
                case "smog":
                    algo = "McLaughlin's SMOG"
                case _:
                    algo = "your metric"
            print("According to " + algo + ", the text can be read by a " + result[i])
    else:
        algo = ""
        match metric:
            case "flesch-kincaid":
                algo = "Flesch-Kincaid"
            case "dale-chall":
                algo = "Dale-Chall"
            case "smog":
                algo = "McLaughlin's SMOG"
            case _:
                algo = "your metric"
        print("According to " + algo + ", the text can be read by a " + result)

if __name__ == "__main__":
    import ch1text
    import IEEssay
    print("Welcome to the Readability Calculator!")
    # if input is not empty and it is not "y" or "Y", then use_syllapy = False
    use_syllapy = input("Would you like to use SyllaPy or our heuristic (default) in the final computations? (s/h) ")
    use_syllapy = True if len(use_syllapy) and use_syllapy[0].lower() == "s" else False
    metric = "*"
    
    print()
    
    print("The Head First Learn To Code excerpt:")
    result = compute_readability(ch1text.quote, metric, use_syllapy, True)
    print_result(result, metric)
    
    print("\n")
    
    print("My Israel Education Essay:")
    result = compute_readability(IEEssay.text, metric, use_syllapy, True)
    print_result(result, metric)
    