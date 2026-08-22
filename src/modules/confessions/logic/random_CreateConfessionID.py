import random
import string

async def GenerateConfessionID():
    chars = string.ascii_letters + string.digits 
    confess_id = ''.join(random.choices(chars, k=3))
    return confess_id