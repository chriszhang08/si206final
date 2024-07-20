# %%
import sqlite3
import requests
import json
import bs4
import matplotlib.pyplot as plt
import numpy as np
import re

# establish sqlite connection
conn = sqlite3.connect('pokemon.db')
c = conn.cursor()

# %% initialize the database
# create the table for the pokedex of all pokemon
c.execute("CREATE TABLE IF NOT EXISTS pokedex (id INTEGER PRIMARY KEY, name TEXT, url TEXT)")
conn.commit()
# create table for advanced pokemon information for specific pokemon
c.execute("CREATE TABLE IF NOT EXISTS starters (id INTEGER PRIMARY KEY, name TEXT, flavor_text_es TEXT)")
conn.commit()
# create table for the words in the scraped html
c.execute("CREATE TABLE IF NOT EXISTS bagofwords (word TEXT PRIMARY KEY, count INTEGER)")
conn.commit()

# %%
# fetch the pokedex from the pokeapi, limit the results to 25
pokemon = requests.get('https://pokeapi.co/api/v2/pokedex/1')
# jsonify the response
pokemon = pokemon.json()["pokemon_entries"]

# divide pokemon into groups of 25
pokemon_groups = [pokemon[i:i + 25] for i in range(0, len(pokemon), 25)]

#%% insert the pokemon into the database one group at a time
for group in pokemon_groups:
    for i in group:
        c.execute("INSERT INTO pokedex (id, name, url) VALUES (?, ?, ?)",
                  (i['entry_number'], i['pokemon_species']['name'], i['pokemon_species']['url']))
    conn.commit()


# %%
# look at database
c.execute('SELECT * FROM pokedex LIMIT 10')
rows = c.fetchall()
for row in rows:
    print(row)

# %% query the pokedex for starter information
ids_to_fetch = [1, 2, 3, 4, 5, 6, 7, 8, 9]
c.execute('SELECT * FROM pokedex WHERE id IN ({})'.format(', '.join('?' * len(ids_to_fetch))), ids_to_fetch)
rows = c.fetchall()

# for each pokemon, use the api link to fetch the flavor text in spanish
for row in rows:
    pokeinfo = requests.get(row[2])
    pokeinfo = pokeinfo.json()
    flavortexts_all = pokeinfo['flavor_text_entries']
    flavortexts_es = [i for i in flavortexts_all if i['language']['name'] == 'es']
    flavortext_es = flavortexts_es[0]['flavor_text']
    c.execute("INSERT INTO starters (id, name, flavor_text_es) VALUES (?, ?, ?)",
              (row[0], row[1], flavortext_es))
conn.commit()

# %% query new database
c.execute('SELECT * FROM starters')
rows = c.fetchall()
for row in rows:
    print(row)

# %% scrape the html
url = 'https://www.bbc.com/mundo/articles/c0w4q32wzvpo'
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

# turn the text into a bag of words and push to database
words = soup.get_text().split()
for word in words:
    c.execute("INSERT OR IGNORE INTO bagofwords (word, count) VALUES (?, 0)", (word,))
    c.execute("UPDATE bagofwords SET count = count + 1 WHERE word = ?", (word,))

conn.commit()


#%%
# join pokedex and starters tables on id
c.execute('SELECT * FROM pokedex JOIN starters ON pokedex.id = starters.id')
rows = c.fetchall()
# calculate how many times each vowel appears in the flavor text
vowels = ['a', 'e', 'i', 'o', 'u']
vowel_counts = {}
for row in rows:
    for vowel in vowels:
        vowel_counts[vowel] = vowel_counts.get(vowel, 0) + row[5].count(vowel)

# plot the vowel counts
fig, ax = plt.subplots()
ax.bar(vowel_counts.keys(), vowel_counts.values())
ax.set_ylabel('Count')
ax.set_xlabel('Vowel')
ax.set_title('Vowel Counts in Pokemon Flavor Text')
plt.show()

#%%
# do the same but for every letter
letter_counts = {}
for row in rows:
    for letter in row[5]:
        letter_counts[letter] = letter_counts.get(letter, 0) + 1

# plot the letter counts
fig, ax = plt.subplots()
ax.bar(letter_counts.keys(), letter_counts.values())
ax.set_ylabel('Count')
ax.set_xlabel('Letter')
ax.set_title('Letter Counts in Pokemon Flavor Text')
plt.show()


#%%
# count how many times each vowel appears in the scraped html
c.execute('SELECT * FROM bagofwords')
rows = c.fetchall()
vowel_counts = {}
for row in rows:
    for vowel in vowels:
        vowel_counts[vowel] = vowel_counts.get(vowel, 0) + row[0].count(vowel)

# plot the vowel counts, make the graph red and as a percentage
fig, ax = plt.subplots()
ax.bar(vowel_counts.keys(), vowel_counts.values(), color='red')
ax.set_ylabel('Count')
ax.set_xlabel('Vowel')
ax.set_title('Vowel Counts in Scraped HTML')
plt.show()

#%%
# count how many times each letter appears in the scraped html
letter_counts = {}
for row in rows:
    for letter in row[0]:
        letter_counts[letter] = letter_counts.get(letter, 0) + 1

# plot the letter counts, make the graph red and as a percentage
fig, ax = plt.subplots()
ax.bar(letter_counts.keys(), letter_counts.values(), color='red')
ax.set_ylabel('Count')
ax.set_xlabel('Letter')
ax.set_title('Letter Counts in Scraped HTML')
plt.show()


