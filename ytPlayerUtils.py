from youtubesearchpython import Playlist
from pytube import YouTube
import vlc
import time
import curses
import threading
import sys

class YouTubePlayer:
    def __init__(self):
        self.isPlaying = False
        self.currentAudioTime = 0

    def streamAudio(self, url):
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).order_by('abr').first()
        audio_url = audio.url
        self.currentAudioTime = 0

        # Using VLC to play the audio
        self.player = vlc.MediaPlayer(audio_url)
        self.player.play()
        time.sleep(1)  # Wait for player to start

        self.isPlaying = True

        while self.isPlaying:
            self.currentAudioTime = self.player.get_time()
            time.sleep(1)  # Aguarde um segundo antes da próxima verificação

    def handleKeys(self):
        stdscr = curses.initscr()
        curses.noecho()  # Desabilita a exibição das teclas pressionadas
        curses.nonl()
        stdscr.keypad(True)  # Habilita o processamento de teclas especiais (setas, etc.)

        stdscr.addstr(0, 0, "Pressione 'q' para sair.")

        while True:
            key = stdscr.getch()

            if key == ord('q'):  # Tecla 'q' para sair
                sys.exit()
            elif key == ord(' '):  # Tecla de espaço
                self.isPlaying = not self.isPlaying
                if self.isPlaying:
                    self.player.play()
                else:
                    self.player.pause()
                time.sleep(0.2)  # Evita múltiplos gatilhos
            elif key == curses.KEY_RIGHT:  # Seta para a direita
                self.player.set_time(self.currentAudioTime + 5000)
                self.currentAudioTime=self.currentAudioTime + 5000
                time.sleep(0.2)  # Evita múltiplos gatilhos
            elif key == curses.KEY_LEFT:  # Seta para a esquerda
                self.player.set_time(self.currentAudioTime - 5000)
                self.currentAudioTime=self.currentAudioTime + 5000
                time.sleep(0.2)  # Evita múltiplos gatilhos

        curses.endwin()

    @staticmethod
    def retrieve_all_playlist_videos(playlist_url):
        playlist = Playlist(playlist_url)
        playlist_title = playlist.info['info']['title']
        playlist_length = playlist.info['info']['videoCount']
        
        videos_info = []
        
        playlist_info = {
            'playlist_title': playlist_title,
            'playlist_length': playlist_length
        }

        videos_info.append(playlist_info)
        
        while playlist.hasMoreVideos:
            playlist.getNextVideos()
        
        for video in playlist.videos:
            video_info = {
                'title': video['title'],
                'link': video['link'],
                'duration': video['duration']
            }
            videos_info.append(video_info)
        
        return videos_info


    def startPlayer(self, url):
        stream_thread = threading.Thread(target=self.streamAudio, args=(url,))
        keys_thread = threading.Thread(target=self.handleKeys)

        stream_thread.start()
        keys_thread.start()

print(YouTubePlayer.retrieve_all_playlist_videos('https://www.youtube.com/playlist?list=PLjUfzvZPRClxqFW-VC4Cr23og-0vo5LAN'))