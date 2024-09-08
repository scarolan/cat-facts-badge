# Pimoroni Badger 2040 App
import gc, displayio, terminalio, board, time, digitalio, alarm, random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_debouncer import Debouncer
from adafruit_display_shapes.roundrect import RoundRect

# Enable the trash collector
gc.enable()

# Your personal info
# Find an icon you like here: 
# https://github.com/olikraus/u8g2/wiki/fntgrpstreamline#streamline_all
# Or comment out the fonticon line to choose a random icon
username = "Sean Carolan"
jobtitle = "Sales Engineer"
#fonticon = "\u0232"

# Functions
def choose_icon():
    start_hex = 0x0030
    end_hex = 0x02BF

    # Check if fonticon is defined and not commented out
    try:
        if fonticon:  # if fonticon is defined, use it
            return fonticon
    except NameError:
        # fonticon is not defined, choose a random icon
        return chr(random.randint(start_hex, end_hex))

def get_dadjoke():
    """Returns a random Dad Joke from the file named dadjokes
    on main storage in classic Dad Joke question-answer format."""
    jokes = open('dadjokes', 'r').read().splitlines()
    joke = random.choice(jokes).split('<')
    q = joke[0]
    a = joke[1].replace('>', '').lstrip(' ')
    q = "\n".join(wrap_text_to_lines(q,30))
    a = "\n".join(wrap_text_to_lines(a,30))
    print(q)
    print(a)
    jokes = []
    return(q, a)

def get_catfact():
    """Reads a random cat fact from the file named catfacts on main storage.
    There are no special delimiters, it's just one cat fact per line."""
    catfacts = open('catfacts', 'r').read().splitlines()
    fact = random.choice(catfacts)
    fact = "\n".join(wrap_text_to_lines(fact,30))
    print(fact)
    catfacts = []
    return(fact)

def create_button_labels(display_group):
    """Creates rounded labels above each button."""
    # Button labels
    a_rect = RoundRect(2, 111, 75, 17, 5, fill=BLACK, outline=WHITE, stroke=1)
    display_group.append(a_rect)

    button_a_text = 'Emoji Party'
    a_group = displayio.Group(scale=1, x=8, y=119)
    a_area = label.Label(terminalio.FONT, text=button_a_text, color=WHITE)
    a_group.append(a_area)
    display_group.append(a_group)

    b_rect = RoundRect(119, 111, 56, 17, 5, fill=BLACK, outline=WHITE, stroke=1)
    display_group.append(b_rect)

    button_b_text = 'Dad Joke'
    b_group = displayio.Group(scale=1, x=124, y=119)
    b_area = label.Label(terminalio.FONT, text=button_b_text, color=WHITE)
    b_group.append(b_area)
    display_group.append(b_group)

    c_rect = RoundRect(226, 111, 55, 17, 5, fill=BLACK, outline=WHITE, stroke=1)
    display_group.append(c_rect)

    button_c_text = 'Cat Fact'
    c_group = displayio.Group(scale=1, x=230, y=119)
    c_area = label.Label(terminalio.FONT, text=button_c_text, color=WHITE)
    c_group.append(c_area)
    display_group.append(c_group)

def clear_ui(display_group):
    global badge_mode_active
    try:
        display_group.remove(badge_group)
        badge_mode_active = False  # Reset when the UI is cleared
    except:
        print("Badge group not attached.")
    try:
        display_group.remove(emoji_group)
        print("Emoji group removed.")
    except:
        print("Emoji group not attached.")
    try:
        display_group.remove(dadjoke_q_group)
        display_group.remove(dadjoke_a_group)
        print("Dadjoke groups removed.")
    except:
        print("Dadjoke groups not attached.")
    try:
        display_group.remove(catfact_group)
        print("Catfact group removed.")
    except:
        print("Catfact group not attached.")
    dadjoke_q_area.text = ''
    dadjoke_a_area.text = ''
    catfact_area.text = ''
    name_area.text = ''
    title_area.text = ''
    emoji_area.text = ''

    # Force garbage collection to free memory
    gc.collect()
    print(gc.mem_free())  # Print free memory for debugging

# Track the current mode
badge_mode_active = False

def show_badge_mode(display_group):
    global badge_mode_active
    if badge_mode_active:
        print("Already in badge mode, skipping update.")
        return
    try:
        display_group.append(badge_group)
        name_area.text = username
        title_area.text = jobtitle
        display.show(display_group)
        badge_mode_active = True  # Set to True once we switch to badge mode
    except Exception as e:
        print('Oops something went wrong.')
        print(e)
    try:
        display.refresh()
    except Exception as e:
        print('Too soon, please try again.')
        print(e)

def show_dadjoke_mode(display_group):
    try:
        display_group.append(dadjoke_q_group)
        display_group.append(dadjoke_a_group)
        j = get_dadjoke()
        dadjoke_q_area.text = j[0]
        dadjoke_a_area.text = j[1]
        display.show(display_group)
    except Exception as e:
        print('Oops something went wrong.')
        print(e)
    try:
        display.refresh()
    except Exception as e:
        print('Too soon, please try again.')
        print(e)

def show_catfact_mode(display_group):
    try:
        display_group.append(catfact_group)
        c = get_catfact()
        catfact_area.text = c
        display.show(display_group)
    except Exception as e:
        print('Oops something went wrong.')
        print(e)
    try:
        display.refresh()
    except Exception as e:
        print('Too soon, please try again.')
        print(e)

def get_random_emojis():
    """Generates a string of 14 random emoji characters with a line break after the 7th character."""
    start_hex = 0x0030
    end_hex = 0x02BF
    emoji_list = [chr(random.randint(start_hex, end_hex)) for _ in range(14)]
    
    # Insert a line break after 7 emojis
    emoji_string = ''.join(emoji_list[:7]) + '\n' + ''.join(emoji_list[7:])
    
    # Force garbage collection after emoji generation
    del emoji_list  # Free up the list object
    gc.collect()
    
    return emoji_string

def show_emoji_party(display_group):
    try:
        display_group.append(emoji_group)
        # Get 8 random emoji characters
        emoji_string = get_random_emojis()
        
        # Update the emoji area with the generated string
        emoji_area.text = emoji_string
        display.show(display_group)
    except Exception as e:
        print('Oops, something went wrong.')
        print(e)
    try:
        display.refresh()
    except Exception as e:
        print('Too soon, please try again.')
        print(e)

"""These settings work well on the Pimoroni Badger 2040. This does
the basic housekeeping of initializing a palette, creating a group,
a white bitmap, and a TileGrid to store the bitmap in. This is
appended to the main group, designated by g."""
# Prepare the display settings
BLACK = 0x000000
WHITE = 0xFFFFFF
display = board.DISPLAY
display.rotation = 270

# Create a two-color palette for our bitmaps
palette = displayio.Palette(2)
palette[0] = WHITE
palette[1] = BLACK

# Create a display group and make a bitmap with the background color
g = displayio.Group()
background_bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create and append a TileGrid to the display group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)

"""Load up some fun fonts. Streamline contains tons of fun small
emoticons and other icons. Emoticons is a smaller set of smileys.
Find more bdf fonts here: https://github.com/olikraus/u8g2/
"""
streamline = bitmap_font.load_font("streamline_all.bdf")
#emoticons = bitmap_font.load_font("emoticons.bdf")
lucida_italic = bitmap_font.load_font("luIS14.bdf")
lucida_regular = bitmap_font.load_font("luRS14.bdf")
lucida_large = bitmap_font.load_font("luRS19.bdf")

"""Configure a debouncer on each button."""
pin_a = digitalio.DigitalInOut(board.SW_A)
pin_a.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.DOWN
button_a = Debouncer(pin_a)

pin_b = digitalio.DigitalInOut(board.SW_B)
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.DOWN
button_b = Debouncer(pin_b)

pin_c = digitalio.DigitalInOut(board.SW_C)
pin_c.direction = digitalio.Direction.INPUT
pin_c.pull = digitalio.Pull.DOWN
button_c = Debouncer(pin_c)

# Reserved for wakeup
#pin_up = digitalio.DigitalInOut(board.SW_UP)
#pin_up.direction = digitalio.Direction.INPUT
#pin_up.pull = digitalio.Pull.DOWN
#button_up = Debouncer(pin_up)

pin_down = digitalio.DigitalInOut(board.SW_DOWN)
pin_down.direction = digitalio.Direction.INPUT
pin_down.pull = digitalio.Pull.DOWN
button_down = Debouncer(pin_down)

# Creates the button labels
create_button_labels(g)

# Badge UI
grafana = displayio.OnDiskBitmap("/grafana.bmp")
grafana_clear = displayio.Bitmap(100, 75, 2)
glabs = displayio.OnDiskBitmap("/glabs.bmp")
glabs_clear = displayio.Bitmap(200, 53, 2)
grafana_grid = displayio.TileGrid(grafana, pixel_shader=grafana.pixel_shader, x=0, y=0)
glabs_grid = displayio.TileGrid(glabs, pixel_shader=glabs.pixel_shader, x=85, y=0)
name_group = displayio.Group(scale=1, x=80, y=58)
name_area = label.Label(lucida_large, text=username, color=BLACK)
name_group.append(name_area)
title_group = displayio.Group(scale=1, x=87, y=81)
title_area = label.Label(lucida_italic, text=jobtitle, color=BLACK)
title_group.append(title_area)
icon_group = displayio.Group(scale=2, x=254, y=100)
icon_area = label.Label(streamline, text=choose_icon(), color=BLACK)
icon_group.append(icon_area)
badge_group = displayio.Group()
badge_group.append(glabs_grid)
badge_group.append(grafana_grid)
badge_group.append(name_group)
badge_group.append(title_group)
badge_group.append(icon_group)

# Catfact UI
catfact_group = displayio.Group(scale=1, x=0, y=8)
catfact_area = label.Label(lucida_regular, text=" "*200, color=BLACK, padding_top=0, padding_bottom=0, line_spacing=0.75)
catfact_group.append(catfact_area)

# Dadjoke UI
dadjoke_q_group = displayio.Group(scale=1, x=0, y=8)
dadjoke_a_group = displayio.Group(scale=1, x=0, y=72)
dadjoke_q_area = label.Label(lucida_regular, text=" "*93, color=BLACK, padding_top=0, padding_bottom=0, line_spacing=0.75)
dadjoke_a_area = label.Label(lucida_italic, text=" "*93, color=BLACK, padding_top=0, padding_bottom=0, line_spacing=0.75)
dadjoke_q_group.append(dadjoke_q_area)
dadjoke_a_group.append(dadjoke_a_area)

# Emoji Party UI
emoji_group = displayio.Group(scale=2, x=0, y=50)
emoji_area = label.Label(streamline, text=" "*14, color=BLACK, line_spacing=1.5)
emoji_group.append(emoji_area)

# Only append the badge group
# We are tight on memory so these groups must be appended
# and removed on every refresh.
g.append(badge_group)

# Initial display - starts with badge since other labels are empty
display.show(g)
time.sleep(2)
display.refresh()

print("Setup complete, entering loop.")

start = time.monotonic()
while True:
    button_a.update()
    button_b.update()
    button_c.update()
    #This is reserved for wake from sleep
    #button_up.update()
    button_down.update()
    now = time.monotonic()
    if now - start >= 120:
        print("Returning to badge mode and sleeping.")
        clear_ui(g)
        show_badge_mode(g)
        pin_alarm = alarm.pin.PinAlarm(pin=board.SW_UP, value=True, pull=True)
        alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
    if button_a.fell:
        print('Activating emoji party...')
        start = time.monotonic()
        clear_ui(g)
        show_emoji_party(g)
    if button_b.fell:
        print('Activating dadjoke mode...')
        start = time.monotonic()
        clear_ui(g)
        show_dadjoke_mode(g)
    if button_c.fell:
        print('Activating catfact mode')
        start = time.monotonic()
        clear_ui(g)
        show_catfact_mode(g)
    if button_down.fell:
        print('Returning to badge mode')
        start = time.monotonic()
        clear_ui(g)
        show_badge_mode(g)
