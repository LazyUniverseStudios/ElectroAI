import datetime
from InternalLogic.DatabaseLogic.DBConnection import DB_GetConnection

async def ClaimDailyReward(user_id: int):
    """
    Attempts to claim the daily 1000 coin reward for a user if their cooldown has expired.

    Args:
        user_id (int): The unique ID of the user.

    Returns:
        tuple: 
            (True, next_cooldown_time) if successful.
            (False, existing_cooldown_time) if still on cooldown.
            (None, None) if a database error occurs.
    """
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE Economy 
                             SET 
                                Coins = Coins + 1000, 
                                DailyRewardNextUse = NOW() + INTERVAL 1 DAY 
                             WHERE UserID = %s 
                             AND (DailyRewardNextUse IS NULL OR DailyRewardNextUse <= NOW())
                             """, (user_id,))
        if cursor.rowcount > 0:
            await conn.commit()
            new_cooldown = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
            return True, new_cooldown
        else: 
            await cursor.execute("""
                                 SELECT DailyRewardNextUse 
                                 FROM Economy 
                                 WHERE UserID = %s
                                 """, (user_id,)) 
            result = await cursor.fetchone()
            next_use_time = result[0] if result else None
            return False, next_use_time
    except Exception as e:
        print(f"Error claiming daily reward for user {user_id}: {e}")
        return None, None
    finally:
        await cursor.close()
        conn.close()

async def ClaimMonthlyReward(user_id: int):
    """
    Attempts to claim the monthly 5000 coin reward for a user if their cooldown has expired.
    Args:
        user_id (int): The unique ID of the user.
    Returns:
        tuple: 
            (True, next_cooldown_time) if successful.
            (False, existing_cooldown_time) if still on cooldown.
            (None, None) if a database error occurs.
    """
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE Economy 
                             SET 
                                Coins = Coins + 5000, 
                                MonthlyRewardNextUse = NOW() + INTERVAL 30 DAY 
                             WHERE UserID = %s 
                             AND (MonthlyRewardNextUse IS NULL OR MonthlyRewardNextUse <= NOW())
                             """, (user_id))
        if cursor.rowcount > 0:
            await conn.commit()
            new_cooldown = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
            return True, new_cooldown
        else:
            await cursor.execute("""
                                 SELECT MonthlyRewardNextUse 
                                 FROM Economy 
                                 WHERE UserID = %s
                                 """, (user_id,))
            result = await cursor.fetchone()
            next_use_time = result[0] if result else None
            return False, next_use_time
    except Exception as e:
        print(f"Error claiming monthly reward for user {user_id}: {e}")
        return None, None
    finally:
        await cursor.close()
        conn.close()

async def ClaimWeeklyReward(user_id: int):
    """
    Attempts to claim the weekly 2000 coin reward for a user if their cooldown has expired.
    
    Args:
        user_id (int): The unique ID of the user.
    
    Returns:
        tuple: 
            (True, next_cooldown_time) if successful.
            (False, existing_cooldown_time) if still on cooldown.
            (None, None) if a database error occurs.
    """
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE Economy 
                             SET 
                                Coins = Coins + %s, 
                                WeeklyRewardNextUse = NOW() + INTERVAL 7 DAY
                             WHERE UserID = %s 
                             AND (WeeklyRewardNextUse IS NULL OR WeeklyRewardNextUse <= NOW())
                             """, (2000, user_id))
        if cursor.rowcount > 0:
            await conn.commit()
            new_cooldown = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            return True, new_cooldown
        else:
            await cursor.execute("""
                                 SELECT WeeklyRewardNextUse 
                                 FROM Economy 
                                 WHERE UserID = %s
                                 """, (user_id,))
            result = await cursor.fetchone()
            next_use_time = result[0] if result else None
            return False, next_use_time
    except Exception as e:
        print(f"Error claiming weekly reward for user {user_id}: {e}")
        return None, None
    finally:
        await cursor.close()
        conn.close()

async def FetchUserEconomyData(user_id: int):
    """
    Fetches the economy data for a specific user.
    
    Args:
        user_id (int): The unique ID of the user.
    
    Returns:
        dict: A dictionary containing the user's economy data, or None if not found.
    """
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             SELECT Coins, DailyRewardNextUse, WeeklyRewardNextUse, MonthlyRewardNextUse 
                             FROM economy 
                             WHERE UserID = %s
                             """, (user_id,))
        result = await cursor.fetchone()
        if result:
            return {
                "Coins": result[0],
                "DailyRewardNextUse": result[1],
                "WeeklyRewardNextUse": result[2],
                "MonthlyRewardNextUse": result[3]
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching user economy data for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def FetchUserBalance(user_id: int):
    """
    Fetches the current coin balance for a specific user.
    
    Args:
        user_id (int): The unique ID of the user.
    
    Returns:
        int: The user's current coin balance, or None if not found.
    """
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             SELECT Coins 
                             FROM economy 
                             WHERE UserID = %s
                             """, (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user balance for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def FetchUserDailyRewardCooldown(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             SELECT DailyRewardNextUse 
                             FROM economy 
                             WHERE UserID = %s
                             """, (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user daily reward cooldown for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()
        
async def FetchUserWeeklyRewardCooldown(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             SELECT WeeklyRewardNextUse 
                             FROM economy 
                             WHERE UserID = %s
                             """, (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user weekly reward cooldown for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def FetchUserMonthlyRewardCooldown(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             SELECT MonthlyRewardNextUse 
                             FROM economy 
                             WHERE UserID = %s
                             """, (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user monthly reward cooldown for user {user_id}: {e}")
        return None
    finally:
        await cursor.close()
        conn.close()

async def UpdateUserBalance_Add(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE economy 
                             SET Coins = Coins + %s 
                             WHERE UserID = %s
                             """, (amount, user_id))
        await conn.commit()
    except Exception as e:
        print(f"Error updating user balance for user {user_id}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()

async def UpdateUserBalance_Subtract(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE economy 
                             SET Coins = Coins - %s 
                             WHERE UserID = %s 
                             AND Coins >= %s
                             """, (amount, user_id, amount))
        await conn.commit()
        result = cursor.rowcount
    except Exception as e:
        print(f"Error updating user balance for user {user_id}: {e}")
        await conn.rollback()
        result = 0
    finally:
        await cursor.close()
        conn.close()
    return result

async def UpdateUserBalance_Set(user_id: int, amount: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE economy 
                             SET 
                                Coins = %s 
                             WHERE UserID = %s
                             """, (amount, user_id))
        await conn.commit()
    except Exception as e:
        print(f"Error updating user balance for user {user_id}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()

async def UpdateUserEconomy_Reset(user_id: int):
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE Economy 
                             SET 
                                Coins = 0, 
                                DailyRewardNextUse = NULL, 
                                WeeklyRewardNextUse = NULL, 
                                MonthlyRewardNextUse = NULL
                             WHERE UserID = %s
                             """, (user_id,))
        await conn.commit()
    except Exception as e:
        print(f"Error resetting user economy for user {user_id}: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()

async def UpdateServerEconomy_Reset():
    conn = await DB_GetConnection()
    cursor = await conn.cursor()
    try:
        await cursor.execute("""
                             UPDATE Economy 
                             SET 
                                Coins = 0,
                                DailyRewardNextUse = NULL,
                                WeeklyRewardNextUse = NULL,
                                MonthlyRewardNextUse = NULL
                             """)
        await conn.commit()
    except Exception as e:
        print(f"Error resetting server economy: {e}")
        await conn.rollback()
    finally:
        await cursor.close()
        conn.close()