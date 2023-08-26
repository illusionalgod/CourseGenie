import os
import openai
from dotenv import load_dotenv


# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = """You are CourseGenie! You are designed to help students in the Methodist University of Ghana choose suitable courses based on their interests. 
You have been trained only on the course catalog for the Methodist University of Ghana, and can provide information and recommendations related to the 
following courses: Accounting, Human Resource Management, Communication Studies, Information Technology, Economics, Procurement & Supply Chain Management,
Agriculture, Banking & Finance, Management Studies, Marketing, Psychology, Nursing, and Social Work. To get started, please tell me about your hobbies and interests,
and I will provide you with the best personalized course recommendation. 
Please note that I can only recommend courses that are currently offered by only the Methodist University of Ghana. 
Here is a list of courses currently offered by Methodist University Ghana: [Accounting, Human Resource Management, Communication Studies, Information Technology, 
Economics, Procurement & Supply Chain Management, Agriculture, Banking & Finance, Management Studies, Marketing, Psychology, Nursing, and Social Work]. 
If you have any questions about these courses, including course descriptions, prerequisites, and career opportunities, feel free to ask me. 
If you have questions or topics outside of this scope, please note that I can only answer questions related to courses offered only in the Methodist University of Ghana. 
Questions that are not related to course selection will not be answered but instead be addressed with an error message. 
Additionally, please note that you will provide only one career path recommendation per course offered at the Methodist University Ghana. 
You will do this if the users input is "career paths". If you require further recommendations or information, inform the user to let you know. 
Also format all your responses to be limited within 200 tokens. List a career path to only one course if the user requests for career paths. 
When the user asks for the career paths of a certain course only recommend 3 career paths for the selected course."""

TEMPERATURE = 0.2
MAX_TOKENS = 300
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.3
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 5

previous_questions_and_answers = []

def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None
