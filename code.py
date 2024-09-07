# Pimoroni Badger 2040 App
import gc, displayio, terminalio, board, time, digitalio, alarm, random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_debouncer import Debouncer
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle

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
    print(gc.mem_free())
    return(q, a)

def get_catfact():
    """Reads a random cat fact from the file named catfacts on main storage.
    There are no special delimiters, it's just one cat fact per line."""
    catfacts = open('catfacts', 'r').read().splitlines()
    fact = random.choice(catfacts)
    fact = "\n".join(wrap_text_to_lines(fact,30))
    print(fact)
    catfacts = []
    print(gc.mem_free())
    return(fact)

def create_button_labels(display_group):
    """Creates rounded labels above each button."""
    # Button labels
    a_rect = RoundRect(21, 111, 38, 17, 5, fill=BLACK, outline=WHITE, stroke=1)
    display_group.append(a_rect)

    button_a_text = 'Badge'
    a_group = displayio.Group(scale=1, x=26, y=119)
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
    dadjoke_q_area.text = ''
    dadjoke_a_area.text = ''
    catfact_area.text = ''
    name_area.text = ''
    title_area.text = ''

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
emoticons = bitmap_font.load_font("emoticons.bdf")
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

# Append all the groups
g.append(dadjoke_q_group)
g.append(dadjoke_a_group)
g.append(catfact_group)
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
    if now - start >= 30:
        print("Returning to badge mode and sleeping.")
        clear_ui(g)
        show_badge_mode(g)
        pin_alarm = alarm.pin.PinAlarm(pin=board.SW_UP, value=True, pull=True)
        alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
    if button_a.fell:
        print('Activating badge mode...')
        start = time.monotonic()
        clear_ui(g)
        show_badge_mode(g)
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
