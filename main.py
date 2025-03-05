import pyautogui as pag
import time
import pygetwindow as gw
import easyocr
import os

#requirements
#delta force must be in windowed or borderless windowed
#run script with as admin
#have to be on main start screen

#given filepath fp of an image, find that image and click on it
def click_image(fp: str, c=0.7) -> None:
    loc = pag.locateCenterOnScreen(fp, confidence=c)
    if loc:
        pag.click(loc)
    else:
        print(f"Image '{fp}' not found on screen.")

#find the search bar and input text
def type_in_search(input: str) -> None:
    click_image('./images/search_bar.png')
    pag.write(input)

#clear search bar
def clear_search() -> None:
    click_image('./images/search_bar_wider.png', 0.5)
    pag.hotkey('ctrl', 'a')
    pag.hotkey('backspace')

#save screenshots routine
#combines typing and clearing the search bar and saving a region of the screen as a screenshot
def save_screenshot(input: str) -> None:
    clear_search()
    type_in_search(input)
    time.sleep(1)
    screenshot = pag.screenshot(region=(400, 150, 500, 200))
    screenshot.save(f'./screenshots/{input}.png')
    print(f'{input} image saved.')
    clear_search()
    time.sleep(0.1)

def main(inputs):
    for file in os.listdir('./screenshots'): #removes all files from screenshot folders
        os.remove(f'./screenshots/{file}')

    game_window = gw.getWindowsWithTitle('Delta Force') #opens delta force if not already opened
    game_window[0].activate()
    time.sleep(0.2)

    click_image('./images/auction.png') #goes to auction screen

    print('Saving images...')

    for input in inputs:
        save_screenshot(input) #saves screenshots of inputs


    print('Processing images...') #extracts the cost of each item
    reader = easyocr.Reader(['en'])
    for input in inputs:
        result = reader.readtext(f'./screenshots/{input}.png')
        for item in result:
            text = item[1]
            text = text.replace(',','')
            try:
                float(text)
                print(f'{input}: {text}')
            except ValueError:
                continue

inputs = ['Cutlass', 'Boxed Drip Coffee', 'High-precision Digital'] #change inputs here
main(inputs)




# pos = pag.locateCenterOnScreen('./images/coin_symbol.png', region=(400, 150, 800, 500))
