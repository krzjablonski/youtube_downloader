from pytube import YouTube
from pytube.innertube import _default_clients as client
import os
import ffmpy
from tqdm import tqdm

client["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
client["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
client["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
client["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
client["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
client["ANDROID_MUSIC"] = client["ANDROID_CREATOR"]


def download_video(save_path: str, audio_only: bool) -> None:
    link = input("Youtube Link: ")
    yt = YouTube(link)
    yd = yt.streams.get_audio_only() if audio_only else yt.streams.get_highest_resolution()
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # Create a progress bar
    progress_bar = tqdm(total=yd.filesize, unit='iB', unit_scale=True, desc=yt.title)

    def progress_callback(stream, chunk, bytes_remaining):
        current = yd.filesize - bytes_remaining
        progress_bar.update(current - progress_bar.n)

    yt.register_on_progress_callback(progress_callback)

    try:
        saved_path = yd.download(save_path)
    except OSError as e:
        print(f"Error saving file: {e}")
        return
    finally:
        progress_bar.close()

    if audio_only:
        new_file_name = saved_path.replace('.mp4', '.mp3')
        ff = ffmpy.FFmpeg(inputs={saved_path: None}, outputs={new_file_name: None})
        ff.run()
        os.remove(saved_path)


def ask_for_next_video() -> bool:
    answer = input("Download next video? [y/n]: [default n] \n")
    answer = 'n' if answer == '' else answer
    if answer not in ['y', 'n']:
        return ask_for_next_video()
    return answer.lower() == 'y'


def select_path() -> str:
    default_path = os.path.expanduser("~/Youtube Download")
    path = input("Provide path to save the files, default is: " + default_path + ' : \n')
    return path or default_path


def download_only_audio() -> bool:
    answer = input("Download only audio? [y/n]: [default n] \n")
    answer = 'n' if answer == '' else answer
    if answer not in ['y', 'n']:
        return download_only_audio()
    return answer == 'y'


def main() -> None:
    next_video = True
    selected_path = select_path()
    audio_only = download_only_audio()

    while next_video:
        download_video(selected_path, audio_only)
        next_video = ask_for_next_video()


if __name__ == '__main__':
    main()
