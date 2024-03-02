import os
import time
import yt_dlp
from threading import Thread

from .step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        caption_list = []
        for yt in data:
            if utils.caption_file_exists(yt):
                print(f'Caption file exists for {yt.url}, skipping')
                continue
            else:
                caption_list.append(yt)

        threads = []

        for i in range(os.cpu_count()):
            threads.append(Thread(target=self.download_caption, args=(caption_list, i)))
            threads[i].start()

        for i in range(os.cpu_count()):
            threads[i].join()

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    @staticmethod
    def download_caption(caption_list, thread_id):
        for yt in caption_list[thread_id::os.cpu_count()]:
            url = yt.url
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'outtmpl': yt.caption_filepath,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    print('Downloading caption for', yt.id)
                    ydl.download([url])
                except yt_dlp.DownloadError as e:
                    print(f"Error downloading subtitles: {e}")
