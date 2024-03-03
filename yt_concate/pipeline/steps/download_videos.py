import os
import yt_dlp
from threading import Thread

from .step import Step


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        print('Videos to download = ', len(yt_set))
        video_list = []

        for yt in yt_set:
            if utils.video_file_exists(yt) and inputs['fast']:
                print(f'Video file exists for {yt.url}, skipping')
                continue
            else:
                video_list.append(yt)

        threads = []
        threads_num = os.cpu_count()

        divide_v_list = [video_list[i:len(video_list):threads_num] for i in range(0, threads_num)]

        for i in range(os.cpu_count()):
            threads.append(Thread(target=self.download_video, args=(divide_v_list[i], )))
            threads[i].start()

        for i in range(os.cpu_count()):
            threads[i].join()

        return data

    @staticmethod
    def download_video(v_list):
        for yt in v_list:
            url = yt.url
            ydl_opts = {
                'outtmpl': yt.video_filepath,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    print('Downloading video for', url)
                    ydl.download([url])
                except yt_dlp.DownloadError as e:
                    print(f"Error downloading video: {e}")
