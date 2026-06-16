"""Adapted from subs_extract (cessen): https://github.com/cessen/subs_extract (modified)"""

import os
import subprocess
import re

archivos=[]
total_subtitulos=[]

def timecode_to_milliseconds(code):
    """ Takes a time code and converts it into an integer of milliseconds.
    """
    elements = code.replace(",", ".").split(":")
    assert(len(elements) < 4)
    
    milliseconds = 0
    if len(elements) >= 1:
        milliseconds += int(float(elements[-1]) * 1000)
    if len(elements) >= 2:
        milliseconds += int(elements[-2]) * 60000
    if len(elements) >= 3:
        milliseconds += int(elements[-3]) * 3600000
    
    return milliseconds

def milliseconds_to_timecode(milliseconds):
    """ Takes a time in milliseconds and converts it into a time code.
    """
    hours = milliseconds // 3600000
    milliseconds %= 3600000
    minutes = milliseconds // 60000
    milliseconds %= 60000
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return "{}:{:02}:{:02}.{:02}".format(hours, minutes, seconds, milliseconds // 10)

def parse_ass_file(path, padding=0):
    """ Parses an entire .ass file, extracting the dialogue.

        Returns a list of (start, length, dialogue) tuples, one for each
        subtitle found in the file.  A padding of "padding" milliseconds is
        added to the start/end times.
    """
    subtitles = []
    with open(path) as f:
        # First find out the field order of the dialogue.
        found_start = False
        fields = {}
        for line in f:
            if not found_start:
                found_start = line.strip() == "[Events]"
            elif line.strip().startswith("Format:"):
                line = line[7:].strip()
                tmp = line.split(",")
                for i in range(len(tmp)):
                    fields[tmp[i].strip().lower()] = i
                break
        if ("start" not in fields) or ("end" not in fields) or ("text" not in fields):
            raise Exception("'Start', 'End', or 'Text' field not found.")

        # Then parse the dialogue lines.
        start_times = set() # Used to prevent duplicates
        for line in f:
            if line.strip().startswith("Dialogue:"):
                elements = line[9:].strip().split(',', len(fields) - 1)
                start_element = elements[fields["start"]].strip()
                end_element = elements[fields["end"]].strip()
                text_element = elements[-1].strip()
                total_subtitulos.append(text_element)

                if (start_element not in start_times) and (text_element != ""):
                    start_times |= set(start_element)
                    start = max(timecode_to_milliseconds(start_element) - padding, 0)
                    end = timecode_to_milliseconds(end_element) + padding
                    length = end - start
                    subtitles += [(
                        milliseconds_to_timecode(start),
                        milliseconds_to_timecode(length),
                        text_element,
                    )]

    subtitles.sort()
    return subtitles, total_subtitulos

def parse_vtt_file(path, padding=0):
    """ Parses an entire WebVTT/SRT file, extracting the dialogue.

        Returns a list of (start, length, dialogue) tuples, one for each
        subtitle found in the file.  A padding of "padding" milliseconds is
        added to the start/end times.
    """
    subtitles = []
    with open(path) as f:
        start_times = set() # Used to prevent duplicates
        for line in f:
            if "-->" in line:
                # Get the timing.
                times = line.split("-->")
                start = max(timecode_to_milliseconds(times[0].strip()) - padding, 0)
                end = timecode_to_milliseconds(times[1].strip()) + padding
                length = end - start

                # Get the text.
                text = ""
                next_line = f.readline()
                while next_line.strip() != "":
                    text += next_line
                    next_line = f.readline()
                text = text.strip()
                total_subtitulos.append(text)

                # Process text to get rid of unnecessary tags.
                text = re.sub("</?ruby>", "", text)
                text = re.sub("<rp>.*?</rp>", "", text)
                text = re.sub("<rt>.*?</rt>", "", text)

                # Add to the subtitles list.
                if (start not in start_times) and (text != ""):
                    start_times |= set([start])
                    subtitles += [(
                        milliseconds_to_timecode(start),
                        milliseconds_to_timecode(length),
                        text,
                    )]
    return subtitles, total_subtitulos

def parse_subtitle_file(filepath, padding=0):
    """ Parses a subtitle file, attempting to automatically determine the
        file format for parsing.
    """
    if filepath.endswith(".ass") or filepath.endswith(".ssa"):
        return parse_ass_file(filepath, padding)
    elif filepath.endswith(".vtt") or filepath.endswith(".srt"):
        return parse_vtt_file(filepath, padding)
    else:
        raise "Unknown subtitle format.  Supported formats are SSA, ASS, VTT, and SRT."

def find_closest_sub(subs_list, timecode, max_diff_milliseconds):
    """ Finds the sub in the given list with the start time closest to timecode.

        Will only return a matching sub if the start time difference is less
        than max_diff_milliseconds.  Otherwise it will return None.
    """
    time_mil = timecode_to_milliseconds(timecode)

    # This certainly isn't the most efficient way to do this, but it's
    # dead-simple and does not appear to be a performance bottleneck at all.
    closest_so_far = -1
    closest_diff = max_diff_milliseconds
    for i in range(len(subs_list)):
        sub_start = timecode_to_milliseconds(subs_list[i][0])
        diff = abs(time_mil - sub_start)
        if diff < closest_diff:
            closest_so_far = i
            closest_diff = diff

    if closest_so_far >= 0:
        return subs_list[closest_so_far]
    else:
        return None

def audio_y_subs(subtitulos, archivo_de_video):
    indice_sub=0
    for item in subtitulos:
        base_filename = rf"media_temp/extracto_temp{indice_sub}.wav"
        print(base_filename)
        archivos.append(base_filename)
        if not os.path.isfile(base_filename):
            subprocess.Popen([
                "ffmpeg",
                "-n",
                "-vn",
                "-ss",
                item[0],
                "-i",
                archivo_de_video,
                "-aq", "8",
                "-t",
                item[1],
                "-ar",
                "44100",
                "-ac",
                "1",
                base_filename,
            ]).wait()
        indice_sub+=1
    return archivos


# Parse the subtitle files