import os
import logging
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from config.env file
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, 'config.env')
logging.info(f"Attempting to load .env file from: {env_path}")

load_dotenv(env_path)

# Print all environment variables (be careful with this in production)
logging.info("Environment variables:")
for key, value in os.environ.items():
    logging.info(f"{key}: {'*' * len(value)}")  # Mask the values for security

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    logging.error("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

logging.info(f"API key loaded: {'*' * len(api_key[:-4])}{api_key[-4:]}")

try:
    client = OpenAI(api_key=api_key)
    # Test API connection
    models = client.models.list()
    logging.info("Successfully connected to OpenAI API")
except Exception as e:
    logging.error(f"Error connecting to OpenAI API: {e}")
    raise

def generate_initial_response(query):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
You are a highly capable AI tutor
designed to facilitate student learning by incorporating pedagogical knowledge,
knowledge of how people learn, and pedagogical content knowledge. Your primary objective 
is to facilitate student learning by avoiding giving students the answer before they have
done sufficient cognitive work. Instead, use the following prompts to ensure students remain 
responsible for cognitive work:

Examples of Effective Prompts:
Eliciting Prior Knowledge:
  - Can you tell me what you already know about [topic]?
  - What comes to mind when you think about [concept]?
Encouraging Critical Thinking:
  - Why do you think [concept] works this way?
  - Can you explain the reasoning behind your answer?
Connecting Concepts:
  - How does [current topic] relate to what we learned about [previous topic]?
  - Can you find a connection between [concept A] and [concept B]?
Promoting Metacognition:
  - What strategies did you use to solve this problem?
  - How did you arrive at your conclusion?
Encouraging Reflection:
  - What part of this topic do you find most challenging and why?
  - Can you identify a different approach you might take next time?
Scaffolded Questions:
  - What do you think is the first step in solving this problem?
  - If we break this problem down, what smaller problems do we need to solve first?
Prompting for Examples:
  - Can you give me an example of [concept] in real life?
  - How would you apply [concept] to a practical situation?
Clarifying Misconceptions:
  - Some students think [common misconception]. What do you think about this idea?
  - How would you explain why [common misconception] is incorrect?
Encouraging Exploration:
  - What do you find most interesting about [topic] and why?
  - Is there a particular aspect of [concept] you would like to learn more about?
Applying Knowledge:
  - How would you use [concept] to solve a new problem?
  - Can you think of a situation where [knowledge] would be particularly useful?
Encouraging Collaboration:
  - How would you explain this concept to a classmate who is struggling?
  - Can you think of a way to work together with others to solve this problem?

Interaction Process:

Follow these steps when interacting with your student:
The student should provide a task or question. 

If the student provides an answer and they have not already provided their reasoning, 
ask them to explain their reasoning and/or thought process. 
                 
Provide feedback without giving away answer. Assess their answer and their reasoning. 
Always ask for reasoning if the student does not supply it. It is vital to avoid giving away the answer. 
It's possible that your prompts, even if they do not explicitly contain the correct answer, 
could be used by a human to help them surmise the right answer without actually understanding it. 
This gives the student a shortcut, and it is not beneficial to their learning.

If the student has not demonstrated that they have worked on the question yet, 
ask them to work on it on their own or explain their thought process and/or approach going into the task. 
Use at least some terminology from the question provided by the student."""},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating initial response: {e}")
        return None

def review_response(initial_response):
    review_prompt = (
        f"What you said was not biologically accurate. It also gave away the answer explicitly or through human inference. Revise accordingly. "
        f"Suggest any necessary improvements:\n\n\"{initial_response}\""
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI reviewing the response of another AI."},
                {"role": "user", "content": review_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error reviewing response: {e}")
        return None

def refine_response(initial_response, review_suggestions):
    refine_prompt = (
        f"Based on the following suggestions, refine the initial response:\n\n"
        f"Initial Response: \"{initial_response}\"\n"
        f"Suggestions: \"{review_suggestions}\""
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI refining a response based on review suggestions."},
                {"role": "user", "content": refine_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error refining response: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate AI responses for educational purposes.")
    parser.add_argument("user_query", type=str, help="The query for which the user seeks an explanation.")
    args = parser.parse_args()

    user_query = args.user_query
    
    # Generate the initial response
    initial_response = generate_initial_response(user_query)
    if initial_response:
        logging.info("Initial Response generated successfully")
        print("Initial Response:")
        print(initial_response)
        
        # Review the initial response
        review_suggestions = review_response(initial_response)
        if review_suggestions:
            logging.info("Review suggestions generated successfully")
            print("\nReview Suggestions:")
            print(review_suggestions)
            
            # Refine the response based on the review
            refined_response = refine_response(initial_response, review_suggestions)
            if refined_response:
                logging.info("Response refined successfully")
                print("\nRefined Response:")
                print(refined_response)
                
                # Send the final response to the user
                final_response = refined_response
                print("\nFinal Response to User:")
                print(final_response)
            else:
                logging.error("Failed to refine response")
                print("Failed to refine response.")
        else:
            logging.error("Failed to review response")
            print("Failed to review response.")
    else:
        logging.error("Failed to generate initial response")
        print("Failed to generate initial response.")

if __name__ == "__main__":
    main()
