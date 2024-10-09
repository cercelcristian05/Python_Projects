import asyncio
import edge_tts

VOICES = ['en-US-JennyNeural']
TEXT = """Hello"""
VOICE = VOICES[0]
OUTPUT_FILE = "test.mp3"

async def amain():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

loop = asyncio.get_event_loop_policy().get_event_loop()
try:
    loop.run_until_complete(amain())
finally:
    loop.close()