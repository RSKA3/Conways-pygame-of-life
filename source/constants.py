# Game logic
INITIAL_GRID_DIMENSION = 100  # n*n grid
MIN_GRID_DIMENSION = 10
MAX_GRID_DIMENSION = 300
CHANGE_DIMENSIONS_BY = 10 # how much to zoom in or out every click

# Tick Speed
TICK_SPEED = 60
INITIAL_TICKS_PER_UPDATE = 12
MIN_TICKS_PER_UPDATE = 3  # twenty updates a second
MAX_TICKS_PER_UPDATE = 60 # one update every second
buttonsCanBePressedEveryTicks = 10

# Dict which values can be changed by child classes safely
TICK = 'tick'
TICKS_PER_UPDATE = 'ticks_per_update'
PAUSED = 'paused'

INIT_SETTINGS = {
    TICK: 0,
    TICKS_PER_UPDATE: INITIAL_TICKS_PER_UPDATE,
    PAUSED: True
}

# Visuals
INIT_SIZE_OF_WINDOW = 0.8 # times the screen height

# Sizes
GRID_MULTIPLE = { "left" : 0.05, "top" : 0.05, "width": 0.8, "height": 0.8 }

# ASSETS
FILE_PATH = "assets"

# Icon filepaths
FORWARD_ICON  = "forward.png"
PAUSE_ICON    = "pause.png"
PLAY_ICON     = "play.png"
ZOOM_IN_ICON  = "zoom-in.png"
ZOOM_OUT_ICON = "zoom-out.png"
LOGO_ICON     = "logo.png"

# Font filepath
FONT_NAME = "Minecraft.ttf"

# COLORS
MAP_BACKGROUND_COLOR    = "0x071E22"
BUTTON_COLOR        = "0x1D7874"
MAIN_BOX_COLOR          = "0x679289"
CELL_COLOR             = "0xF4C095"

stopDrawingGridLines = 80 # if either of the gridDimensions surpasses this then we dont draw gridlines