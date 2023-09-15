from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def chatbot_response(user_data):
    # Initialize variables to store user information
    name = ''
    age = ''
    location = ''
    dosha = ''                                                                                                                              
    
    # Initialize scores for each dosha
    kapha_score = 0
    pitta_score = 0
    vata_score = 0

    user_message = user_data.get('Q', '').strip().lower()  # Get the user's response
    question_text = user_data.get('questionText', '')
    
    def mainkapha():
        nonlocal kapha_score
        # Ask 10 yes/no questions one by one
        questions = [
            "Whether your skin remains oily throughout the year in comparison to others?",
            "Do you change your body posture frequently?",
            "Are you lazy and disinterested in activities like morning walk/jogging, swimming, or any type of outdoor games?",
            "Do you feel hungry more frequently and do you consume more food in comparison to others?",
            "Have you got a good/attractive complexion?",
            "Have you got well-built muscles?",
            "Do you think you have intense sexual desire?",
            "Do you get irritated easily?",
            "Among your family members, is your complexion considered fairer?",
            "Are sounds produced frequently in your joints on movement?"
        ]

        for i, question in enumerate(questions, 1):
            while True:
                response_key = f'Q{i}'
                if response_key in user_data:
                    answer = user_data[response_key].strip().lower()
                    if answer == "yes":
                        kapha_score += 1
                    elif answer == "no":
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                else:
                    break

    def mainPitta():
        nonlocal pitta_score
        # Ask 10 yes/no questions one by one
        questions = [
            "Are you more comfortable in winter than summer?",
            "Do you have excessive black moles, freckles, etc. on your skin?",
            "Have you experienced premature graying, wrinkling of skin & early baldness?",
            "Do you have soft, scanty, brown hair on your face, body & head?",
            "Do you involve yourself in risky & heroic activities requiring physical strength often?",
            "Do you have the ability to digest large quantities of food easily?",
            "Do you consume food more frequently than others? (5-6 times/day)",
            "Do you have soft & loose muscle bulk especially around the joints?",
            "In comparison to others, do you pass urine & stool in large quantities and do you perspire more?",
            "Do your friends complain of bad smell being emitted from your body & mouth?"
        ]

        for i, question in enumerate(questions, 1):
            while True:
                response_key = f'Q{i}'
                if response_key in user_data:
                    answer = user_data[response_key].strip().lower()
                    if answer == "yes":
                        pitta_score += 1
                    elif answer == "no":
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                else:
                    break

    def mainVatta():
        nonlocal vata_score
        # Ask 10 yes/no questions one by one
        questions = [
            "Is your long-term memory weak?",
            "Do you generally learn things quickly?",
            "Are you easily caught by diseases like flu, allergy during seasonal changes?",
            "Is your body undernourished?",
            "Are you comfortable in summer?",
            "Does your sleep last less than 6 hours per day? Or can your sleep be disturbed easily?",
            "Are your nails, teeth, hands, feet, and hairs on your body or face rough?",
            "Do you have cracks on the body, especially on the heels?",
            "Do you get frightened easily?",
            "Do you often feel stiffness in your body after exercise, traveling?"
        ]

        for i, question in enumerate(questions, 1):
            while True:
                response_key = f'Q{i}'
                if response_key in user_data:
                    answer = user_data[response_key].strip().lower()
                    if answer == "yes":
                        vata_score += 1
                    elif answer == "no":
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                else:
                    break

    def calculate_percentage(score):
        per = (score / 10) * 100
        return per

    try:
        mainkapha()
        mainPitta()
        mainVatta()
        
        # Calculate the percentage for each dosha
        kapha_percentage = calculate_percentage(kapha_score)
        pitta_percentage = calculate_percentage(pitta_score)
        vata_percentage = calculate_percentage(vata_score)
        
        # Determine the dominant dosha
        if kapha_percentage > pitta_percentage and kapha_percentage > vata_percentage:
            dosha = "Kapha"
        elif pitta_percentage > kapha_percentage and pitta_percentage > vata_percentage:
            dosha = "Pitta"
        elif vata_percentage > kapha_percentage and vata_percentage > pitta_percentage:
            dosha = "Vata"
        else:
            dosha = "Balanced"
        
        # Return the result along with dosha information
        result_message = f"ChatBot says: Hello {name}, based on your responses, you have a {dosha} dosha constitution. You can follow the given tips for a healthier lifestyle."
        
        # Include dosha scores in the response
        result_message += f"\nKapha Score: {kapha_percentage}%"
        result_message += f"\nPitta Score: {pitta_percentage}%"
        result_message += f"\nVata Score: {vata_percentage}%"
        
        return result_message
    except Exception as e:
        print("Connectivity issue or error:", str(e))

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_data = request.json
    user_message = user_data.get('Q', '').strip().lower()
    question_text = user_data.get('questionText', '')
    # Define a list of valid responses (yes/no)
    valid_responses = ['yes', 'no']

    if user_message in valid_responses:
        # Your existing code for dosha analysis goes here
        bot_message = chatbot_response(user_data)
    else:
        # Handle invalid input gracefully
        bot_message = 'Invalid input. Please respond with either "yes" or "no".'

    return jsonify({'message': bot_message})

if __name__ == '__main__':
    app.run(debug=True)
