import subprocess

def format_time(t):
    hrs = int(t//3600)
    mins = int((t%3600)//60)
    secs = int(t%60)
    ms = int((t - int(t))*1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"


def split_words(segment):
    words = segment['text'].strip().split()
    start = segment['start']
    end = segment['end']

    duration = end - start
    word_time = duration / max(len(words),1)

    timed_words = []

    for i,word in enumerate(words):
        w_start = start + i * word_time
        w_end = w_start + word_time
        timed_words.append((word,w_start,w_end))

    return timed_words


def make_shorts_captions(input_video, segments, output_video):

    srt_file = "temp_subs.srt"
    index = 1

    with open(srt_file,"w",encoding="utf8") as f:

        for seg in segments:
            words = split_words(seg)

            for word,start,end in words:
                f.write(f"{index}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{word}\n\n")
                index+=1

    subprocess.run([
        "ffmpeg","-y","-i",input_video,
        "-vf",f"subtitles={srt_file}:force_style='Fontsize=28,PrimaryColour=&Hffffff&,OutlineColour=&H000000&,BorderStyle=3,Outline=3,Shadow=1,Alignment=2'",
        "-c:a","copy",
        output_video
    ])
