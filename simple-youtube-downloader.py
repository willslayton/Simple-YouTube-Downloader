import os, ffmpeg, tempfile
from pytube import YouTube
with tempfile.TemporaryDirectory() as temp:
    path, dirs, files = next(os.walk(os.getcwd()))
    file_count = len(files)
    link = input("URL : ")
    try:
        yt = YouTube(link)
        title = yt.title
    except:
        print("Error connecting to YouTube...")
        pass
    else:
        streams = yt.streams.filter(file_extension = "mp4")
        qualities = []
        for s in streams:
            if s.resolution:
                qualities.append(str(s.resolution) + str(s.fps))
            else:
                pass
        print("Available qualities are " + ", ".join(qualities))
        userq = input("Which quality would you like? : ")
        video = yt.streams.filter(file_extension = "mp4", resolution = userq[:-2], fps = int(userq[-2:])).first()
        title = video.default_filename
        print("Downloading \"" + title + "\"...")
        audio = yt.streams.filter(only_audio = True).first()
        try:
            video.download(output_path = temp, filename="video")
            audio.download(output_path = temp, filename="audio")
        except:
            print("Error downloading video...")
            pass
        else:
            inputvideo = ffmpeg.input(temp + "/video.mp4")
            inputaudio = ffmpeg.input(temp + "/audio.mp4")
            ffmpeg.concat(inputvideo, inputaudio, v=1, a=1).output(title).run()
print('Done!')
os.system("pause")
