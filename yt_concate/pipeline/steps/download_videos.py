import yt_dlp

from .step import Step


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        print('Videos to download = ', len(yt_set))

        for yt in yt_set:
            url = yt.url
            if utils.video_file_exists(yt):
                print(f'Video file exists for {url}, skipping')
                continue

            ydl_opts = {
                'outtmpl': yt.video_filepath,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    print('Downloading video for', url)
                    ydl.download([url])
                except yt_dlp.DownloadError as e:
                    print(f"Error downloading video: {e}")

        return data
