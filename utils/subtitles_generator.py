import datetime

def format_timestamp(seconds):
    return str(datetime.timedelta(seconds=seconds)).replace('.', ',')

# def generate_srt(chunks, output_path):
#     with open(output_path, "w", encoding="utf-8") as f:
#         for idx, (start, text) in enumerate(chunks, 1):
#             start_time = format_timestamp(start)
#             end_time = format_timestamp(start + 4)  # default 4s per caption
#             f.write(f"{idx}\n{start_time} --> {end_time}\n{text}\n\n")

# def generate_vtt(chunks, output_path):
#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write("WEBVTT\n\n")
#         for (start, text) in chunks:
#             start_time = format_timestamp(start)
#             end_time = format_timestamp(start + 4)
#             f.write(f"{start_time} --> {end_time}\n{text}\n\n")
def generate_srt(text):
    lines = text.strip().split('. ')
    srt = ""
    for i, line in enumerate(lines):
        srt += f"{i+1}\n00:00:{i:02d},000 --> 00:00:{i+2:02d},000\n{line.strip()}\n\n"
    return srt

def generate_vtt(text):
    lines = text.strip().split('. ')
    vtt = "WEBVTT\n\n"
    for i, line in enumerate(lines):
        vtt += f"00:00:{i:02d}.000 --> 00:00:{i+2:02d}.000\n{line.strip()}\n\n"
    return vtt
