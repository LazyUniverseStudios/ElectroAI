import random

GeneralQuestions = {
    "aaa" : "Which everyday sound would make the worst alarm clock noise and why?",
    "aab" : "Your laugh gets swapped with an animal sound, but you get to choose which animal sound it is. What do you choose and why?",
    "aac" : "If you were famous what would your stage name be and why?",
    "aad" : "What fictional character do you have beef with? Why do you have it?",
    "aae" : "If you could eat only one food for the rest of your life what would it be and why?",
    "aaf" : "What is something you would sell an organ for? And which organ would it be?",
    "aag" : "Is water wet?"
}

PressTheButton = {
    "baa" : "Would you press the button if it had a 5% chance of giving you 1 trillion dollars & 95% chance of turning you into a femboy? Why?"
}

ReflectionQuestions = {
    "caa" : "What would your younger self be most surprised about where you are today?"
}

WouldYouRather = {
    "daa" : "Would you rather date a Hello Kitty Girl or a Goth Femboy and why?",
    "dab" : "Would you rather fight 100 chicken-sized zombies or 10 zombie-sized chickens and why?"
}

deck_map = {
    "General Questions": GeneralQuestions,
    "Press the Button": PressTheButton,
    "Reflection Questions": ReflectionQuestions,
    "Would You Rather?": WouldYouRather
}

def get_random_question():
    deck = random.choice(list(deck_map.keys()))
    questions = deck_map[deck]
    question_key = random.choice(list(questions.keys()))
    question = questions[question_key]
    return deck, question, question_key
