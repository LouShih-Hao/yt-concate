import os
import time
import yt_dlp

from webvtt import WebVTT

from .step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for yt in data:
            url = yt.url
            if utils.caption_file_exists(yt):
                print(f'Caption file exists for {url}, skipping')
                continue

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

            vtt_file_path = yt.caption_filepath + '.en.vtt'
            srt_file_path = yt.caption_filepath

            # 轉換 VTT 到 SRT
            if os.path.exists(vtt_file_path):
                vtt = WebVTT().read(vtt_file_path)
                with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                    for caption in vtt:
                        srt_file.write(f"{caption.start} --> {caption.end}\n{caption.text}\n")
                os.remove(vtt_file_path)  # 刪除原始的 VTT 檔案
            else:
                print(f"VTT file not found at {vtt_file_path}")
        end = time.time()
        print('took', end - start, 'seconds')

        return data
