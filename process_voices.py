#!/usr/bin/env python3
import os
import json
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from pydub import AudioSegment
from io import BytesIO

load_dotenv()

def load_metadata():
    """Load the composition plan metadata"""
    with open('rapbattle_metadata.json', 'r') as f:
        return json.load(f)

def split_audio():
    """Split the audio into female and male sections"""
    # Load the original audio
    audio = AudioSegment.from_mp3("rapbattle_original.mp3")
    
    # Based on the original structure: Female section first, then Male section
    # We'll split roughly in half since it's 2 main sections
    total_duration = len(audio)
    split_point = total_duration // 2
    
    female_section = audio[:split_point]
    male_section = audio[split_point:]
    
    # Export the segments
    female_section.export("female_section.mp3", format="mp3")
    male_section.export("male_section.mp3", format="mp3")
    
    print(f"Split audio into:")
    print(f"  Female section: 0 to {split_point}ms ({len(female_section)}ms)")
    print(f"  Male section: {split_point}ms to {total_duration}ms ({len(male_section)}ms)")
    
    return female_section, male_section

def apply_voice_changer(audio_file, target_voice_id, output_file):
    """Apply voice changer to an audio file"""
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    
    print(f"Applying voice changer to {audio_file} with voice ID: {target_voice_id}")
    
    # Read the audio file
    with open(audio_file, "rb") as f:
        audio_data = BytesIO(f.read())
    
    # Apply voice conversion
    converted_audio = elevenlabs.speech_to_speech.convert(
        voice_id=target_voice_id,
        audio=audio_data,
        model_id="eleven_multilingual_sts_v2",
        output_format="mp3_44100_128",
    )
    
    # Save the converted audio
    with open(output_file, "wb") as f:
        for chunk in converted_audio:
            if chunk:
                f.write(chunk)
    
    print(f"Voice-changed audio saved as: {output_file}")

def combine_segments():
    """Combine the processed segments back together"""
    female_audio = AudioSegment.from_mp3("female_section.mp3")
    male_converted_audio = AudioSegment.from_mp3("male_section_converted.mp3")
    
    # Combine them
    final_audio = female_audio + male_converted_audio
    
    # Export the final track
    final_audio.export("rapbattle_final.mp3", format="mp3")
    print("Final rap battle track saved as: rapbattle_final.mp3")
    
    return final_audio

def main():
    """Main processing pipeline"""
    print("Starting voice processing pipeline...")
    
    # Step 1: Split the audio
    female_section, male_section = split_audio()
    
    # Step 2: Apply voice changer to male section
    # Using Liam voice (young confident male voice)
    male_voice_id = "TX3LPaxmHKxFdv7VOQHJ"  # Liam - young confident male voice
    apply_voice_changer("male_section.mp3", male_voice_id, "male_section_converted.mp3")
    
    # Step 3: Combine the segments
    final_audio = combine_segments()
    
    # Step 4: Play the final result
    print("\nPlaying the final rap battle with alternating voices...")
    with open("rapbattle_final.mp3", "rb") as f:
        play(f.read())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have the original audio file and API key set up")