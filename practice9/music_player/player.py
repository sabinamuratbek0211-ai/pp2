import pygame


class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current = 0

        pygame.mixer.init()
        pygame.mixer.music.load(self.playlist[self.current])

    def play(self):
        pygame.mixer.music.play()
        print("Playing:", self.playlist[self.current])

    def stop(self):
        pygame.mixer.music.stop()
        print("Stopped")

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        print("Next:", self.playlist[self.current])

    def prev(self):
        self.current = (self.current - 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        print("Previous:", self.playlist[self.current])