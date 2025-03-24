from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, URLInputFile
import asyncio
from aiogram import Router
import logging
import aiohttp
import instaloader
import os
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import re







BOT_TOKEN = '6506997439:AAH9eQBPpzZKmfTnp2cFGgbNrFfJUuNA8bs'
ADMIN_ID = '5339188029'
API_URL = 'https://api.telegram.org/bot'
OPENWEATHERMAP_API_KEY = '9feaacebc8d06153712bf2d5d4f04d6e'





router = Router()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(router)

@router.message(Command(commands=["start", "help"]))
async def start_or_help_handler(message: Message):
    await message.answer("Xush kelibsiz! Bu Aiogram 3.x misoli.")

# Connect to OpenWeatherMap API
async def get_weather(city: str):
    api_key = OPENWEATHERMAP_API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    async with aiohttp.ClientSession() as session:
        params = {"q": city, "appid": api_key, "units": "metric"}
        async with session.get(base_url, params=params) as response:
            data = await response.json()
            return data

@router.message(Command(commands=["weather"]))
async def weather_handler(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos, shahar nomini kiriting.")
        return
    city = args[1]
    weather_data = await get_weather(city)
    if weather_data.get("cod") != 200:
        await message.answer("Shahar topilmadi.")
        return
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    await message.answer(f"Shahar: {city}\nHarorat: {temperature}°C\nTavsif: {weather_description}")

# Connect to OpenAI API
async def get_response(text: str):
    api_key = " "
    base_url = "https://api.openai.com/v1/engines/davinci/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"prompt": text, "max_tokens": 100}
    async with aiohttp.ClientSession() as session:
        async with session.post(base_url, json=data, headers=headers) as response:
            data = await response.json()
            return data

# async def get_response_with_playwright():
#     async with playwright.async_api.async_playwright() as p:
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#         await page.goto("https://kun.uz/")
#         await page.wait_for_timeout(5000)
#         response = await page.get_by_role("main-news__left-hero")
#         await browser.close()
#         return response

async def get_response_with_requests():
    response = requests.get("https://kun.uz/")
    soup = BeautifulSoup(response.text, "html.parser")
    news_title = soup.find("h3", class_="main-news__left-hero-title")
    news_text = soup.find("p", class_="main-news__left-hero-text")
    img = soup.find("a", class_="main-news__left-hero-img")
    image_url = img.find("img")["src"]
    os.makedirs("images", exist_ok=True)
    with open(f"images/{image_url.split('/')[-1]}", "wb") as file:
        image_response = requests.get(image_url)
        file.write(image_response.content)
    msg_text = {
        "text": news_title.text.strip() + "\n" + news_text.text.strip(),
        "image": f"images/{image_url.split('/')[-1]}",
        "image_url": image_url
    }
    return msg_text

@router.message(Command(commands=["news"]))
async def news_handler(message: Message):
    msg = await get_response_with_requests()
    news = "😯😯😯💯\n" +  msg["text"]
    img = msg["image"]
    img_url = msg["image_url"]
    # file = FSInputFile(img)
    file = URLInputFile(img_url)
    await message.answer_photo(photo=file, caption=news)

@router.message(Command(commands=["download_instagram"]))
async def download_instagram_handler(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos, Instagram video URL manzilini kiriting.")
        return
    url = args[1]
    video_path, video_url, shortcode = await download_instagram_video(url)
    file = URLInputFile(video_url)
    await message.answer_video(video=file, caption="Instagram video yuklab olindi.")
    # delete_file(video_path)

async def download_instagram_video(url: str):
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
    video_url = post.video_url
    video_path = f"videos/{post.shortcode}.mp4"
    os.makedirs("videos", exist_ok=True)
    L.download_post(post, target="videos")
    return video_path, video_url, str(post.shortcode)

@router.message(Command(commands=["download_youtube"]))
async def download_youtube_handler(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos, YouTube video URL manzilini kiriting.")
        return
    url = clean_youtube_url(args[1])
    try:
        video_path = await download_youtube_video(url)  # `video_url` keraksiz
        file = FSInputFile(video_path)  # To‘g‘ri usul
        await message.answer_video(video=file, caption="YouTube video yuklab olindi.")
    except ValueError as e:
        await message.answer(f"Xato: {e}")

def clean_youtube_url(url):
    match = re.search(r"(?:youtu\.be/|youtube\.com/watch\?v=)([\w-]+)", url)
    return f"https://www.youtube.com/watch?v={match.group(1)}"

async def download_youtube_video(url: str):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if not video:
            raise ValueError("No suitable video stream found.")
        os.makedirs("videos", exist_ok=True)
        video_path = f"videos/{yt.video_id}.mp4"
        video.download(output_path="videos", filename=f"{yt.video_id}.mp4")
        return video_path  # Faqat video fayl yo‘li qaytariladi
    except VideoUnavailable:
        raise ValueError("The video is unavailable.")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())