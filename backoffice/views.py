from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import subprocess
from django.contrib import messages
import playwright
import run_bot, scraper
import threading

BOT_THREAD = None

def trigger_bot_script(request):
    global BOT_THREAD
    
    if BOT_THREAD and BOT_THREAD.is_alive():
        messages.warning(request, "Bot is already running in the background!")
    else:
        # Start the loop in the background
        BOT_THREAD = threading.Thread(target=run_bot.start_the_loop, daemon=True)
        BOT_THREAD.start()
        messages.success(request, "Bot started! It will now loop indefinitely in the background.")

    return redirect('admin:backoffice_botlog_changelist')

@login_required
def aparatai_view(request):
    return render(request, 'pages/aparatai.html', {'segment': 'aparatai'})



def dashboard(request):
    # This is where you can calculate stats for your 5,000 items
    # For now, we just pass empty context
    context = {
        'segment': 'dashboard',
    }
    return render(request, 'pages/dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def trigger_bot_script(request):
    try:
        result = run_bot.start_the_loop()
        
        messages.success(request, f"Success: {result}")
    except Exception as e:
        messages.error(request, f"Error running script: {e}")
        
    return redirect('admin:backoffice_botlog_changelist')

def stop_bot_script(request):
    try:
        # 1. Attempt the built-in Playwright close
        run_bot.kill_browser()
    except Exception as e:
        # We ignore 'greenlet' or 'thread' errors because 
        # as you said, the browser is already closing!
        print(f"Cleanup error (ignoring): {e}")

    # 2. Add the notification
    messages.warning(request, "Bot stopped instantly")

    # 3. MUST use 'return' here to actually move the browser
    return redirect('admin:backoffice_botlog_changelist')

def run_scrape(request):
    try:
        scraper.scrape()
    except Exception as e:
        print(f"kazkas negerai: {e}")

    messages.warning(request, "Scraping completed!")

    return redirect('admin:backoffice_botlog_changelist')