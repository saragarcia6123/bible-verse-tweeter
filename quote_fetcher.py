import json
import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

headers = {"api-key": os.getenv("BIBLE_API_KEY")}

BASE_URL = "https://api.scripture.api.bible/v1"

VERSES_ENDPOINT = "/bibles/{bibleId}/chapters/{chapterId}/verses"
VERSE_ENDPOINT = "/bibles/{bibleId}/verses/{verseId}"

BIBLE_ID = "de4e12af7f28f599-02"  # KJV

with open('data/chapter_ids.json', 'r') as f:
    all_chapters = json.load(f)

def get_verses(chapter_id):
    url = f"{BASE_URL}{VERSES_ENDPOINT.format(bibleId=BIBLE_ID, chapterId=chapter_id)}"
    verses_data = requests.get(url, headers=headers).json()["data"]
    
    return [verse['id'] for verse in verses_data]

def get_verse(verse_id):
    url = f"{BASE_URL}{VERSE_ENDPOINT.format(bibleId=BIBLE_ID, verseId=verse_id)}"
    
    params = {
        "content-type": "text",
        "include-notes": "false",
        "include-titles": "true",
        "include-chapter-numbers": "false",
        "include-verse-numbers": "false",
        "include-verse-spans": "false",
        "use-org-id": "false"
    }
    
    return requests.get(url, headers=headers, params=params).json()["data"]

def get_random_verse():
    chapter_id = all_chapters[random.randint(0, len(all_chapters)-1)]
    verses = get_verses(chapter_id)
    verse_num = random.randint(0, len(verses))
    verse_content = ""
    reference = ""
    i = 0
    
    while verse_content == '' or verse_content.endswith(','):
        try:
            verse_id = chapter_id + "." + str(verse_num)
            verse_data = get_verse(verse_id)
            verse_text = verse_data['content'].strip().replace(":", ".")
            
            if reference == "":
                reference = verse_data['reference']
            verse_content += verse_text
            
        except json.JSONDecodeError:
            pass
        
        verse_num += 1
        i+= 1
        if verse_num > len(verses)-1 or i > 3:
            break
    
    return f'"{verse_content}" - {reference}'
