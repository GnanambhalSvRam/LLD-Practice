'''
Main Components:
User
    - user_id: str
    - is_premium: bool
    - downloaded_songs: list[Song]

Song 
    - song_id
    + play_song 

Advertisement
    - ad_id
    + play_ad

Decorator Class: AudioSetting
Concrete Decorator Classes: BassBoost, TrebleBoost, Surround

Decorator Class: PremiumFeatures
Concrete Decorator Classes: Download
'''
from abc import ABC, abstractmethod
class User:
    
    def __init__(self, user_id, is_premium):
        self.user_id = user_id
        self.is_premium = is_premium
        self.downloaded_songs = []
        
    def downloadSong(self, song_id):
        self.downloaded_songs.append(song_id)
        
    def setPremium(self, is_premium):
        self.is_premium = is_premium
        
    def getPremium(self) -> bool:
        return self.is_premium

class Audio(ABC):
    @abstractmethod
    def play(self):
        pass
    
class Song(Audio):
    def __init__(self, song_name: str, artist: str):
        self.song_name = song_name
        self.artist = artist
        
    def play(self):
        return f'Playing {self.song_name} by {self.artist}'
        
class AudioSetting(Audio):
    
    def __init__(self, audio: Audio):
        self._audio = audio
        
    def play(self):
        return self._audio.play()
        
class BassBoost(AudioSetting):
    def play(self):
        return self._audio.play() + " | Bass Boosted"
        
class TrebleBoost(AudioSetting):
    def play(self):
        return self._audio.play() + " | Treble Boosted"
        
class Surround(AudioSetting):
    def play(self):
        return self._audio.play() + " | Surround"
        
class Advertisement(AudioSetting):
    def __init__(self, audio: Audio, ad_name: str):
        super().__init__(audio)
        self.ad_name = ad_name
        
    def play(self) -> str:
        return "Playing ad: " + self.ad_name + "... " + self._audio.play()
        
song1 = Song("Blinding Lights", "The Weeknd")
song2 = Song("Bohemian Rhapsody", "Queen")

user1 = User('ted.mosby', is_premium = True)
user2 = User('barney.stinson', is_premium = False)

if user1.getPremium():
    print(f'Spotify Premium User')
    music = Surround(BassBoost(song2))
    print(music.play())
    
if not user2.getPremium():
    print(f'Spotify Free User')
    music = Advertisement(song1, "Just Do It. Nike.")
    print(music.play())
