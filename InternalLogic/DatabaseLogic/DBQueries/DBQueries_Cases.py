from InternalLogic.DatabaseLogic.DBConnection import DB_GetConnection

async def CreateCase(CaseID: str, CaseType: str, ModeratorID: int, TargetID: int, reason: str):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("INSERT INTO moderation (CaseID, CaseType, ModeratorID, TargetID, Reason) VALUES (%s, %s, %s, %s, %s)", (CaseID, CaseType, ModeratorID, TargetID, reason))
    await conn.commit()
    await cursor.close()
    conn.close()

async def FetchCase(CaseID: str):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM moderation WHERE CaseID = %s", (CaseID,))
    result = await cursor.fetchone()
    await cursor.close()
    conn.close()
    return result

async def FetchCasesByTarget(target: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM moderation WHERE TargetID = %s", (target,))
    result = await cursor.fetchall()
    await cursor.close()
    conn.close()
    return result

async def FetchCasesByModerator(moderator: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM moderation WHERE ModeratorID = %s", (moderator,))
    result = await cursor.fetchall()
    await cursor.close()
    conn.close()
    return result

async def FetchCasesByType(case_type: str):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM moderation WHERE CaseType = %s", (case_type,))
    result = await cursor.fetchall()
    await cursor.close()
    conn.close()
    return result

async def FetchCases_All():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM moderation")
    result = await cursor.fetchall()
    await cursor.close()
    conn.close()
    return result