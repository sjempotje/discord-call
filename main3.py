import moviepy.editor as mp
import numpy as np
from moviepy import *

def create_circle_clip(video_clip):
    # Extract the audio from the video clip
    audio_clip = video_clip.audio
    
    # Get the volume of the audio clip
    max_volume = audio_clip.max_volume()
    
    # Set the threshold volume to 20% of the maximum volume
    threshold_volume = max_volume * 0.2
    
    # Create a green circle clip
    green_circle = mp.ColorClip(video_clip.size, color=(0, 255, 0)).set_opacity(0.5)
    
    # Create a video clip with the green circle clip
    video_with_green_circle = video_clip.set_audio(None).set_opacity(0.5).set_duration(audio_clip.duration)
    
    # Use memory mapping to create a large array for storing the audio frames
    audio_frames = np.memmap('audio_frames.npy', dtype='float32', mode='w+', shape=(int(audio_clip.fps * audio_clip.duration), ))
    
    # Iterate through each frame of the audio clip and store it in the audio_frames array
    for i, (t, volume) in enumerate(audio_clip.iter_frames()):
        audio_frames[i] = volume
    
    # Iterate through each frame of the video clip and add the green circle when the volume is above the threshold
    for i, frame in enumerate(video_clip.iter_frames()):
        if audio_frames[i] >= threshold_volume:
            video_with_green_circle = video_with_green_circle.blit(green_circle, (0, 0))
        else:
            video_with_green_circle = video_with_green_circle.blit(frame, (0, 0))
    
    # Delete the memmap object to free up memory
    del audio_frames
    
    # Set the audio of the video clip back to the original audio clip
    video_with_green_circle = video_with_green_circle.set_audio(audio_clip)
    
    return video_with_green_circle


# Load the video clip
video_clip = mp.VideoFileClip("sine_wave.mp4")

# Create the video clip with the green circle
video_with_green_circle = create_circle_clip(video_clip)

# Save the video clip
video_with_green_circle.write_videofile("video_with_green_circle.mp4", fps=video_clip.fps)

