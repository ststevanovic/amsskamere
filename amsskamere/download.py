from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to ChromeDriver
chrome_driver_path = '/usr/bin/google-chrome-stable'

# URL of the webpage containing the video
url = "https://https://kamere.amss.org.rs"

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the webpage
    driver.get(url)

    # Wait for the video to load
    time.sleep(5)

    # Locate the video element by its ID
    video_element = driver.find_element(By.ID, "batrovci2")

    # Get the blob URL from the video element
    video_url = video_element.get_attribute("src")

    # Execute JavaScript to download the video data
    video_data = driver.execute_script("""
        var video = document.getElementById(arguments[0]);
        var url = video.src;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'blob';
        xhr.send();
        return new Promise(function(resolve, reject) {
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var reader = new FileReader();
                    reader.readAsDataURL(xhr.response);
                    reader.onload = function(e) {
                        resolve(reader.result);
                    };
                } else {
                    reject(xhr.statusText);
                }
            };
            xhr.onerror = function() {
                reject(xhr.statusText);
            };
        });
    """, "batrovci2")

    # Save the video data to a file
    with open("batrovci2.mp4", "wb") as video_file:
        video_file.write(video_data.split(",")[1].decode("base64"))

    print("Video downloaded successfully and saved as batrovci2.mp4")

finally:
    # Close the WebDriver
    driver.quit()

