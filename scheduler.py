
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from telegram.ext import Application

def setup_schedulers(app: Application):
    scheduler = AsyncIOScheduler()
    scheduler.start()
