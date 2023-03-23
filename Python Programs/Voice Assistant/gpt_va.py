import openai
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import wavio
import asyncio

# Prompt the user to enter their API key
api_key = input("Enter your OpenAI API key: ")

# Validate the API key
if not api_key:
    print("Error: No API key provided.")
    exit()
    
# Initialize the OpenAI API
openai.api_key = api_key

# Initialize the text-to-speech engine 
engine = pyttsx3.init()

# Function to transcribe audio file to text
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
    return None

# Function to generate a response
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

# Function to speak text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to record audio
async def record_audio(duration, sample_rate, filename):
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
    await asyncio.sleep(duration)
    wavio.write(filename, recording, sample_rate, sampwidth=2)

# Main function to run the program
async def main():
    while True:
        # Prompt the user to start speaking
        print("\nHello, please say your question.")
        speak_text("Hello, please say your question.")

        # Wait for user to say something
        duration = 5  # seconds
        sample_rate = sd.query_devices(kind='input')['default_samplerate']
        filename = "input.wav"
        task = asyncio.create_task(record_audio(duration, sample_rate, filename))
        await task

        # Generate the response
        text = transcribe_audio_to_text(filename)
        if text:
            print(f"You said: {text}")
            if text.lower() in ['quit', 'exit']:
                print("\nThank you for using the program. Goodbye!")
                speak_text("Thank you for using the program. Goodbye!")
                return
            
            response = generate_response(text)
            print(f"\nChat GPT-3 says: {response}")
            speak_text(response)
        else:
            print("I'm sorry, I didn't catch that. Please try again.")
            speak_text("I'm sorry, I didn't catch that. Please try again.")
            
if __name__ == "__main__":
    asyncio.run(main())
