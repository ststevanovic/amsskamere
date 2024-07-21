import asyncio
from pyppeteer import launch
import logging 
import os 
from PIL import Image
from datetime import datetime


out="data"
os.makedirs(out, exist_ok=True)

# Set up logging
log = ".log"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log, mode='w') 
                    ])

# Path to your Chrome executable - TODO: sys.path provide or Dockerized
CHROME_PATH = {
    'windows': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'mac': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'linux': '/usr/bin/google-chrome' 
}

async def process(button, page):

    button_onclick = await page.evaluate('(button) => button.getAttribute("onclick")', button)
    some_id = button_onclick.split("'")[1]

    # Loading...
    await button.click()
    await page.waitFor(3000)

    video_element = await page.querySelector(f'video#{some_id}')
    bounding_box = await video_element.boundingBox()
    logging.debug(f"Spider: 2 - {bounding_box}")

    # Take a full page screenshot
    timestamp = datetime.now().strftime("%H%M-%m-%Y")
    out_page = f'{out}/page_{some_id}_{timestamp}.png'
    await page.screenshot({'path': out_page , 'fullPage': True}) # This sets full page view
    logging.info(f"Screenshot taken Success: {out_page}")

    # Get the bounding box of the video element once in full page view
    video_element = await page.querySelector(f'video#{some_id}')
    bounding_box = await video_element.boundingBox()
    logging.debug(f'Bounding box (full page): {bounding_box}')

    # Calculate the page width
    page_width = await page.evaluate('document.body.scrollWidth')
    logging.debug(f'Page width: {page_width}')

    # Calculate the offset for centering the bounding box
    center_offset = page_width - bounding_box['width'] /2
    logging.debug(f'Center offset: {center_offset}')

    # Adjust the bounding box coordinates to center it horizontally
    left = center_offset
    top = bounding_box['y']
    right = center_offset + bounding_box['width']
    bottom = bounding_box['y'] + bounding_box['height']

    # Add a check for the min bounding_box size
    min_width, min_height = 253, 107  
    passed = bounding_box['width'] > min_width and bounding_box['height'] > min_height
    if not passed:
        logging.debug(f"Bounding box too small for {some_id}: {bounding_box}")
        return False
    
    # Crop the page screenshot to the video bounding box
    out_screenshot = os.path.join(out, f'b_{some_id}_{timestamp}.png')
    with Image.open(out_page) as img:
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img_path = out_screenshot
        cropped_img.save(cropped_img_path)
        logging.debug(f"Cropped video screenshot saved as {cropped_img_path}")

    return passed

async def take_screenshots(url):
    browser = await launch(
        executablePath=CHROME_PATH['mac'],  # TODO: dep.
        headless=True, 
        args=[
            '--autoplay-policy=no-user-gesture-required',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-default-apps',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-hang-monitor',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--disable-sync',
            '--disable-translate',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain',
            '--disable-gpu' 
        ])
    page = await browser.newPage()
    
    await page.goto(url)
    logging.debug(f'Navigating to URL:{url}')

   
    # Get all buttons on the page
    buttons = await page.querySelectorAll('button')

    torepeat = []
    for button in buttons:
        passed = await process(button, page)
        if not passed:
            torepeat.append(button)

    while torepeat:
        for button in torepeat[:]:
            passed = await process(button, page)
            if passed:
                torepeat.remove(button)
       
        
    await browser.close()



url = 'https://kamere.amss.org.rs/'

asyncio.run(take_screenshots(url))
