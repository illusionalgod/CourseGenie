import pytest
from chatbot_logic import get_response, get_moderation, INSTRUCTIONS
from app import app

# Unit Testing for get_response function
def test_get_response():
    instructions = INSTRUCTIONS
    previous_questions_and_answers = [("What is the best course for computer science?", 
    "If you are interested in Computer Science, the best course for you at Methodist University of Ghana would be Information Technology. This program covers a wide range of topics including programming, software development, database management, networking, and cybersecurity. It provides students with the skills and knowledge needed to design, develop, and maintain computer systems and networks. The program also prepares students for careers in various fields such as software engineering, web development, data analysis, and cybersecurity.")]
    new_question = "What are the prerequisites for information technology?"
    response = get_response(instructions, previous_questions_and_answers, new_question)
    assert isinstance(response, str)  # Check if the response is a string
    assert len(response) > 0  # Check if the response is not empty

# Unit Testing for get_moderation function
def test_get_moderation():
    safe_question = "What are the course options for business students?"
    errors = get_moderation(safe_question)
    assert errors is None  # Check if no errors are returned for a safe question

    unsafe_question = "I want to harm myself."
    errors = get_moderation(unsafe_question)
    assert isinstance(errors, list)  # Check if the errors are returned as a list
    assert len(errors) > 0  # Check if the errors list is not empty

# Integration Testing for Flask routes
def test_chat_route():
    with app.test_client() as client:
        # Test the chat route with a question
        response = client.post('/chat', data={'question': 'What are the prerequisites for Information Technology?'})
        assert response.status_code == 200  # Check if the response status is OK
        assert b"The prerequisites for Information Technology at the Methodist University of Ghana are Mathematics and English Language at the WASSCE/SSSCE level. Additionally, it is recommended that students have a strong interest in computer hardware and software, programming languages, and information systems." in response.data  # Check if the response contains the expected content


        # Test the chat route with a question containing special characters
        response = client.post('/chat', data={'question': '@#$%^&*()'})
        assert response.status_code == 200  # Check if the response status is OK
        assert b"I'm sorry, I didn't understand your input" in response.data  # Check if the response contains the expected content



# Run all the test cases
if __name__ == '__main__':
    pytest.main()