# This script prints today's Amazon Alexa Jeopardy questions and their correct answers

import datetime
import html
import requests

today = datetime.datetime.today()

def get_correct_answer(clue):
    question = clue['clue']
    answers = clue['answers']
    correct_index = clue['correct_answer_index']

    # html.unescape() will convert html character references to readable characters
    correct_answer = html.unescape(question) + '\n'

    # find the correct answer based on its index
    for answer in answers:
        index = answers.index(answer)
        if index == (int(correct_index) - 1):
            correct_answer += "\n"
            correct_answer += html.unescape(answer)

    correct_answer += '\n\n'
    return correct_answer


def process_jeopardy():
    # Make a request to the Jeopardy API
    try:
        today_jeopardy_clues = requests.get('https://www.jeopardy.com/api/j6-clues').json()[0]
    # Exception to run if script is ran on weekends, or other days without games posted
    except Exception:
        return 'No jeopardy game posted today'

    # Create header for output
    today_header = today.strftime("%A, %m/%d/%Y")
    output = f'Alexa Skills Jeopardy Answers for {today_header} for Amazon Echo \n\n\n'

    # This block identifies different rounds
    clue_rounds = []
    for i in range(1, 10):
        # The round's keys in the API take the form of clues_round_1, clues_round_2, etc.
        if ('clues_round_' + str(i)) in today_jeopardy_clues:
            # Append this round to the list of rounds
            clue_rounds.append(today_jeopardy_clues['clues_round_' + str(i)])
        else:
            break

    # This block appends round numbers the output
    for i, round in enumerate(clue_rounds):
        output += f'ROUND {str(i + 1)}\n\n'
        for clue in round:
            output += get_correct_answer(clue)
            output += '\n\n'

        output += '\n\n\n'

    # Write today's clues to the file
    return output

info = process_jeopardy()
print(info)
