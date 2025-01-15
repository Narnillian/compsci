print('What type of animal are you calculating for? (d)og, (c)at, or (p)arakeet?')
while True:
    animal_type = input()
    if (animal_type not in ['d','dog','c','cat','p','parakeet']):
        print("Unfortunately, that animal isn't supported!")
    else: break
pet_name = input("What is their name? ")
pet_age = int(input("What is their age? "))

if (animal_type == 'd' or animal_type == 'dog'):
    if (pet_age < 1):       converted_age = 0
    elif (pet_age == 1):    converted_age = 15
    elif (pet_age == 2):    converted_age = 21
    else:                   converted_age = (pet_age-2) * 5 + 21
elif (animal_type == 'c' or animal_type == 'cat'):
    if (pet_age < 1):       converted_age = 0
    elif (pet_age == 1):    converted_age = 15
    elif (pet_age == 1):    converted_age = 24
    else:                   converted_age = (pet_age-2) * 4 + 24
elif (animal_type == 'p' or animal_type == 'parakeet'):
    converted_age = pet_age * 10
else:
    print("Somehow, you've input an animal that isn't available!")
    exit()

print(f'{pet_name} is about {converted_age} years old, relative to human aging!')
