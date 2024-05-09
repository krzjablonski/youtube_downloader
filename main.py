from pytube import YouTube
import os
import ffmpy


def download_video(save_path: str, audio_only: bool) -> None:
    link = input("Youtube Link: ")
    yt = YouTube(link)

    yd = yt.streams.get_highest_resolution() if audio_only is False else yt.streams.get_audio_only()

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    saved_path = yd.download(save_path)

    if audio_only:
        new_file_name = saved_path.replace('.mp4', '.mp3')
        ff = ffmpy.FFmpeg(inputs={saved_path: None}, outputs={new_file_name: None})
        ff.run()
        os.remove(saved_path)


def ask_for_next_video() -> bool:
    answer = input("Download next video? [y/n]: ")
    if answer not in ['y', 'n']:
        return ask_for_next_video()
    return answer == 'y'


def select_path() -> str:
    default_path = os.path.expanduser("~/Youtube Download")
    path = input("Provide path to save the files, default is: " + default_path + ': ')
    return path or default_path


def download_only_audio() -> bool:
    answer = input("Download only audio? [y/n]: ")
    if answer not in ['y', 'n']:
        return ask_for_next_video()
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
