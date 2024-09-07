# CircuitPython examples for the Badger RP2040

# Shapes
# https://docs.circuitpython.org/projects/display-shapes/en/latest/examples.html
roundrect = RoundRect(0, 0, 296, 128, 6, fill=WHITE, outline=BLACK, stroke=2)
g.append(roundrect)

#circle = Circle(150, 102, 22, fill=WHITE, outline=BLACK)
g.append(circle)

#rect = Rect(0, 0, 296, 128, fill=WHITE, outline=BLACK)
g.append(rect)

#triangle = Triangle(46, 84, 22, 124, 71, 124, fill=0x00FF00, outline=0xFF00FF)
g.append(triangle)

# Fun with emoji
emoji_group = displayio.Group(scale=2, x=5, y=60)
emoji_text = "\u02b0\u0270\u0232\u0033\u0034"
emoji_area = label.Label(streamline, text=emoji_text, color=BLACK)
emoji_group.append(emoji_area)
g.append(emoji_group)

# Emoticons
faces_group = displayio.Group(scale=1, x=5, y=80)
faces_text = "\u0020\u0021\u0022\u0023"
faces_area = label.Label(emoticons, text=faces_text, color=BLACK)
faces_group.append(faces_area)
g.append(faces_group)
