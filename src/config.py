# Command Prefix for the Bot's text commands
COMMAND_PREFIX = "."

# Database Connection Pool Settings
POOL_MIN_SIZE = 2  # Minimum number of connections in the pool
POOL_MAX_SIZE = 20  # Maximum number of connections in the pool

# Embed Colors
embedColor = {
    "DEFAULT": 0x3B2DFF, # Default color for embeds
    "ERROR": 0xCB2821, # Embed color for error messages
    "SUCCESS": 0x21CB28, # Embed color for success messages
    "MISC": 0x000001, # Miscellaneous embed color
    "BIRTHDAY": 0xFFD700, # Embed color for birthday messages
    "CONFESSION" : 0x9D4EDD, # Embed Color for confession submissions
    "BOOST": 0xF47FFF # Embed Color for Boost Messages
}

# Bot Identity IDs
botIdentityIDs = {
    "BOT": 1378449256049803384, # Bot ID for the Discord bot
    "BOT_ADMIN": 757868967384711249  # Bot Admin ID for the Discord bot
}

# Server Identity IDs
serverIdentityIDs = {
    "GUILD": 1216146656878133429, # Guild ID for
    "GUILD_OWNER": 757868967384711249  # Guild Owner ID for the Discord server
}

# Channel IDs
channelIDs = {
    "JOINS_CHANNEL": 1459155124089000072, # Joins Channel ID
    "LEAVES_CHANNEL": 1459155124089000072, # Leaves Channel ID
    "GENERAL_CHAT_CHANNEL": 1480599558642728990, # General Chat Channel ID
    "INTRODUCTION_CHANNEL": 1537111461636218910, # Introduction Channel ID
    "BIRTHDAY_CHANNEL": 1523831931710738544, # Birthday Channel ID
    "QOTD_CHANNEL": 1523838557624471625, # Question of the Day Channel ID
    "BOOSTS_CHANNEL": 1427728272560623626, # Boosts Channel ID
    "CONFESSIONS_CHANNEL": 1540322421071151176, # Confessions Channel ID
}

# Role IDs
roleIDs = {
    "BASE_MEMBER_ROLE": 1412101472438452306, # ".gg/electrocafe" | Base Member Role ID, All Humans have this role by default.
    "MEMBER_PING_SEPERATOR": 1412101886001020929, # Member Ping Seperator Role ID
    "MEMBER_PROFILE_SEPERATOR": 1412101535227183176, # Member Profile Seperator Role ID
    "BASE_BOT_ROLE": 1412101520786329711, # Base Bot Role ID
    "LEVEL_ROLES": {
        "LEVEL_5": 1538515520137986108, # Level 5
        "LEVEL_10": 1412101177809829958, # Level 10
        "LEVEL_20": 1412101132825657344, # Level 20
        "LEVEL_30": 1412101119676518603, # Level 30
        "LEVEL_40": 1412101106426970233, # Level 40
        "LEVEL_50": 1412101089721057411, # Level 50
        "LEVEL_60": 1412101074302537879, # Level 60
        "LEVEL_70": 1412101053838786801, # Level 70
        "LEVEL_80": 1412101030442958858, # Level 80
        "LEVEL_90": 1412101011954208888, # Level 90
        "LEVEL_100": 1412100991884460076, # Level 100
        "LEVEL_110": 1412100964835528784, # Level 110
        "LEVEL_120": 1412100943654158409, # Level 120
        "LEVEL_130": 1412100917670449283, # Level 130
        "LEVEL_140": 1412100893066788956, # Level 140
        "LEVEL_150": 1412100878151979159, # Level 150
    },
    "STAFF_ROLES": {
        "LEAD_MANAGEMENT": 1412099637032255518,
        "MANAGER": 1412099673975554132,
        "PARTNERSHIP_MANAGER": 1412099702073327798,
        "EVENT_MANAGER": 1412099739037466755,
        "TICKET_MANAGER": 1412099771388395741,
        "HEAD_ADMIN": 1412099820453232721,
        "ADMIN": 1412099853374193714,
        "HEAD_MODERATOR": 1412099909779456083,
        "MODERATOR": 1412099881526493214,
        "TRIAL_MODERATOR": 1412099948446617652,
        "STAFF_BASE": 1412099992818286835, # "Staff Team"
        "EVENT_STAFF_BASE": 1412100011575214153 # "Event Team"
    },
    "BIRTHDAY_ROLE": 1538506580486656022, # Birthday Role ID
    "BIRTHDAY_PING_ROLE": 1412101967144026142, # Birthday Ping Role ID
    "BUMP_PING_ROLE": 1412101940292222986, # Bump Ping Role ID
    "GIVEAWAY_PING_ROLE": 1412102063445512282, # Giveaway Ping Role ID
    "QOTD_PING_ROLE": 1412102087663157360, # Question of the Day Ping Role ID
    "CHAT_REVIVE_PING_ROLE": 1412102007283646628, # Chat Ping Role ID
}
