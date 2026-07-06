import random
import string
from InternalLogic.DatabaseLogic.DBConnection import DB_GetConnection

async def GenerateCaseID():
    conn = await DB_GetConnection()
    chars = string.ascii_letters + string.digits 
    cursor = await conn.cursor()

    while True:
        case_id = ''.join(random.choices(chars, k=6))
        
        await cursor.execute("SELECT 1 FROM moderation WHERE CaseID = %s", (case_id,))
        exists = await cursor.fetchone()
        if not exists:
            await cursor.close()
            conn.close()
            return case_id
