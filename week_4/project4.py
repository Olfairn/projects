#%%
import sqlite3

conn = sqlite3.connect('songs.db')

#%%

class Song:
    def __init__(self,artist,lyrics):
        self.artist = artist
        self.lyrics = lyrics
    
    def __repr__(self):
        return "Song('{}','{}')".format(self.artist, self.lyrics)
#%%

c = conn.cursor()

c.execute("""CREATE TABLE songs (
    artist text, 
    lyrics text
    )""")

#%%

c.execute("INSERT INTO employees VALUES ('Corey', 'Tom', 70000)")

#c.execute("INSERT INTO employees VALUES (:artist, :lyrics, :pay)", {'artist':emp1.artist,'lyrics':emp1.lyrics,'pay':emp1.pay})

#conn.close()
#%%
#c.execute("SELECT * FROM songs")

c.execute("SELECT * FROM songs WHERE artist=:artist", {'artist':'The doors'})
c.fetchmany(5)

#%%
song_1 = Song('The doors','You know that it would be untrue')

#%%
insert_song(song_1)
c.fetchmany(5)
#%%
c.fetchmany(100)

#%%
def insert_song(song):
    with conn:
        c.execute("INSERT INTO songs VALUES (:artist, :lyrics)", {'artist':song.artist,'lyrics':song.lyrics})

#%%
def get_song_by_name(song_name):
    c.execute("SELECT * FROM songs WHERE lyrics=:lyrics", {'lyrics':'song_name'})
    return c.fetchall()

#%%
def update_pay(emp,pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
        WHERE artist = :artist AND lyrics  = :lyrics""",
        {'artist':emp.artist, 'lyrics': emp.lyrics, 'pay': pay})
#%%

conn.commit()
#%%
conn.close()
# %%
