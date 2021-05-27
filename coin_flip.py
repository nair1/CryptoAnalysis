import random

actual = random.randint(0, 1)

correct = 0
total = 0

for i in range (0, 10000):
    if (actual == 0):
        guess = 1
    else:
        guess = 0
        
    actual = random.randint(0, 1)
    
    total += 1
    
    if (actual == guess):
        correct += 1
        
    total_correct = round(correct * 100.0 / total * 1.0, 2)
    print(total_correct)

    print("Guess: " + str(guess) + ", Actual: " + str(actual) + " Win Rate: " + str(total_correct) + "%")