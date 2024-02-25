import os
import yt_dlp
from webvtt import WebVTT
from .step import Step

import time


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for url in data:
            print('Downloading caption for', url)
            if utils.caption_file_exists(utils.get_caption_filepath(url)):
                print('Caption file exists')
                continue
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'outtmpl': utils.get_caption_filepath(url),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                except yt_dlp.DownloadError as e:
                    print(f"Error downloading subtitles: {e}")

            vtt_file_path = utils.get_caption_filepath(url) + '.en.vtt'
            srt_file_path = utils.get_caption_filepath(url)

            # 轉換 VTT 到 SRT
            if os.path.exists(vtt_file_path):
                vtt = WebVTT().read(vtt_file_path)
                with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                    for caption in vtt:
                        srt_file.write(f"{caption.start} --> {caption.end}\n{caption.text}\n\n")
                os.remove(vtt_file_path)  # 刪除原始的 VTT 檔案
            else:
                print(f"VTT file not found at {vtt_file_path}")
        end = time.time()
        print('took', end - start, 'seconds')
