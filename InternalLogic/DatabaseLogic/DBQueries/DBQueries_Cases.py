from InternalLogic.DatabaseLogic.DBConnection import DB_GetConnection

async def CreateCase(CaseID: str, CaseType: str, ModeratorID: int, TargetID: int, reason: str):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("INSERT INTO moderation (CaseID, CaseType, ModeratorID, TargetID, Reason) VALUES (%s, %s, %s, %s, %s)", (CaseID, CaseType, ModeratorID, TargetID, reason))
        await conn.commit()
    except Exception as e:
        print(f"Error creating case {CaseID}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()

async def FetchCase(CaseID: str):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT * FROM moderation WHERE CaseID = %s", (CaseID,))
        result = await cursor.fetchone()
    except Exception as e:
        print(f"Error fetching case {CaseID}: {e}")
        result = None
    finally:
        await cursor.close()
        conn.close()
    return result

async def FetchCasesByTarget(target: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT * FROM moderation WHERE TargetID = %s", (target,))
        result = await cursor.fetchall()
    except Exception as e:
        print(f"Error fetching cases for target {target}: {e}")
        result = None
    finally:
        await cursor.close()
        conn.close()
    return result

async def FetchCasesByModerator(moderator: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT * FROM moderation WHERE ModeratorID = %s", (moderator,))
        result = await cursor.fetchall()
    except Exception as e:
        print(f"Error fetching cases for moderator {moderator}: {e}")
        result = None
    finally:
        await cursor.close()
        conn.close()
    return result

async def FetchCasesByType(case_type: str):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT * FROM moderation WHERE CaseType = %s", (case_type,))
        result = await cursor.fetchall()
    except Exception as e:
        print(f"Error fetching cases for type {case_type}: {e}")
        result = None
    finally:
        await cursor.close()
        conn.close()
    return result

async def FetchCases_All():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("SELECT * FROM moderation")
        result = await cursor.fetchall()
    except Exception as e:
        print(f"Error fetching all cases: {e}")
        result = None
    finally:
        await cursor.close()
        conn.close()
    return result