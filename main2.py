from matplotlib import pyplot as plt
from moviepy.editor import * 
import os
import moviepy.video.fx.all as vfx
from moviepy.video.tools.drawing import color_gradient
import numpy as np



 
duration = 0.1


def make_frame(t):
    #make the background color black 2c2f33"
    clip = ColorClip((1080,1920), color=(44,47,51))
    images_folder = os.listdir("assets/backgrounds")
    #get the amount of images in the folder
    images_amount = len(images_folder)
    if (images_amount == 0):
        print("No images in folder")
        return clip.get_frame(t)
    elif (images_amount == 1):
        square1 = ColorClip((1080,1920), color=(255,255,255)).set_position((0,0))
        final = CompositeVideoClip([clip, square1])
        
        #get the first image in the folder
        image = images_folder[0]
        #load the image and place it in the center of the square (the image is 300x300)
        image = ImageClip("assets/backgrounds/" + image).set_position((390,810))
        #overlay the image on the background
        final = CompositeVideoClip([final, image])
        return final.get_frame(t)


    elif (images_amount == 2):
        square1 = ImageClip("assets/backs/gradient.png").set_position((0,0))
        square2 = ImageClip("assets/backs/gradient.png").set_position((0,960))
        final = CompositeVideoClip([clip, square1, square2])

        #get the first image in the folder
        image = images_folder[0]
        #load the image and place it in the center top of the square (the image is 270x270)
        image = ImageClip("assets/backgrounds/" + image).set_position((405,345))
        #overlay the image on the background
        image2 = images_folder[1]
        #load the image and place it in the center bottom of the square (the image is 270x270)
        image2 = ImageClip("assets/backgrounds/" + image2).set_position((405,1305))
        #make the images rounded
        final = CompositeVideoClip([final, image, image2])

        return final.get_frame(t)    

def AudioGetter(video):
    #get the audio streams provided as mp3 from the folder assets/audio
    audio_folder = os.listdir("assets/audio")
    images_folder = os.listdir("assets/backgrounds")
    #get the amount of audio files in the folder
    audio_amount = len(audio_folder)
    if (audio_amount == 0):
        print("No audio in folder")
        return video
    elif (audio_amount == 1):
        #get the first mp3 in the folder
        audio1 = audio_folder[0]
        #load the audio
        audio1 = AudioFileClip("assets/audio/" + audio1)
        #set the audio to the video
        video = video.set_audio(audio1)
        for chunk in audio1.iter_chunks():
            # chunk is a tuple of (time, data)
            t = chunk[0]
            # create a green circle at the center of the image
            circle = (ImageClip("assets/circle.png")
                      .resize(height=100)
                      .set_position(("center", "center"))
                      .set_duration(0.2)
                      .set_start(t)
                      .fx(vfx.colorx, "#00FF00"))
            # composite the circle on top of the image
            image = CompositeVideoClip([image, circle])
        
        # make the final video by compositing the image on the background clip
        background = ColorClip((1080,1920), color=(44,47,51))
        final = CompositeVideoClip([background, image])
        return final.set_audio(audio1)
    elif (audio_amount == 2):
        audio1 = audio_folder[0]
        audio2 = audio_folder[1]

        audio1 = AudioFileClip("assets/audio/" + audio1)
        audio2 = AudioFileClip("assets/audio/" + audio2)

        video = video.set_audio(audio1)
        video = video.set_audio(audio2)

        for chunk in audio1.iter_chunks():
            # chunk is a tuple of (time, data)
            t = chunk[0]
            # create a green circle at the center of the image
            circle = (ImageClip("assets/circle.png")
                      .resize(height=100)
                      .set_position(("center", "center"))
                      .set_duration(0.2)
                      .set_start(t)
                      .fx(vfx.colorx, "#00FF00"))
            # composite the circle on top of the image
            image = CompositeVideoClip([image, circle])
        
        # make the final video by compositing the image on the background clip
        background = ColorClip((1080,1920), color=(44,47,51))
        final = CompositeVideoClip([background, image])
        return final.set_audio(audio1)

clip = VideoClip(make_frame, duration = duration)
#add the audio to the video
clip = AudioGetter(clip)

#make the background color black
clip = clip.on_color(size=(1080,1920), color=(0,0,0))
#make the text clip
#overlay the text clip on the background clip
#write the result to a file 
 
# saving Video Clip
clip.write_videofile("sine_wave.mp4", fps = 60)