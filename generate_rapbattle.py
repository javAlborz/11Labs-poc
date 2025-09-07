#!/usr/bin/env python3
import os
import json
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()

def read_rap_battle():
    """Read and format the rap battle content"""
    with open('rapbattle.txt', 'r') as f:
        content = f.read()
    return content

def generate_rap_battle():
    """Generate the rap battle track with detailed response"""
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    
    # Read the rap battle content
    rap_content = read_rap_battle()
    
    # Create a prompt that incorporates the rap battle content
    prompt = f"""Create a hip-hop rap battle track with a strong female rapper performing all vocals. The track should be aggressive, rhythmic, and energetic with a strong beat. Here's the battle content to perform:

{rap_content}

Structure this as a rap battle with:
- Strong female rapper delivering all verses with attitude
- Aggressive, confident female vocal delivery
- Strong hip-hop beat and rhythm
- Clear, powerful female vocal performance
- Tempo around 90-110 BPM suitable for rap battles
- Female voice throughout the entire track"""

    print("Generating rap battle track...")
    
    # Generate with detailed response to get composition plan and timing
    track_details = elevenlabs.music.compose_detailed(
        prompt=prompt,
        music_length_ms=60000,  # 60 seconds - adjust as needed
    )
    
    # Save the audio
    audio_filename = "rapbattle_original.mp3"
    with open(audio_filename, "wb") as f:
        f.write(track_details.audio)
    
    # Save the composition plan and metadata
    metadata_filename = "rapbattle_metadata.json"
    with open(metadata_filename, "w") as f:
        json.dump(track_details.json, f, indent=2)
    
    print(f"Track generated and saved as: {audio_filename}")
    print(f"Metadata saved as: {metadata_filename}")
    print(f"Original filename from API: {track_details.filename}")
    
    # Display composition plan sections for timing reference
    if 'composition_plan' in track_details.json:
        plan = track_details.json['composition_plan']
        print("\nComposition Plan Sections:")
        cumulative_time = 0
        for i, section in enumerate(plan.get('sections', [])):
            duration = section.get('durationMs', 0)
            start_time = cumulative_time
            end_time = cumulative_time + duration
            print(f"  Section {i+1}: {section.get('sectionName', 'Unknown')} - {start_time}ms to {end_time}ms ({duration}ms)")
            cumulative_time += duration
    
    # Play the track
    print("\nPlaying the generated track...")
    play(track_details.audio)
    
    return track_details

if __name__ == "__main__":
    try:
        track_details = generate_rap_battle()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set ELEVENLABS_API_KEY in your .env file")