from datetime import datetime, timedelta, timezone

from db_connection import _ActivePool

async def claimWeeklyReward(user_id: int):
    """
    Claims the weekly reward for the user.

    Args:
        user_id (int): The ID of the user claiming the reward.
    Returns:
        tuple: A tuple containing a boolean indicating success and the next use time (datetime) or an error message.
    """
    async with _ActivePool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                 UPDATE Economy 
                                 SET 
                                    Coins = Coins + 5000, 
                                    WeeklyRewardNextUse = NOW() + INTERVAL 7 DAY 
                                 WHERE UserID = %s 
                                 AND (WeeklyRewardNextUse IS NULL OR WeeklyRewardNextUse <= NOW())
                                 """, (user_id,))
                    if cursor.rowcount > 0:
                        await conn.commit()
                        new_cooldown = datetime.now(timezone.utc) + timedelta(days=7)
                        return True, new_cooldown
                    else:
                        await conn.rollback()
                        await cursor.execute("SELECT WeeklyRewardNextUse FROM Economy WHERE UserID = %s", (user_id,))
                        result = await cursor.fetchone()
                        if result:
                            next_use_time = result[0]
                            return False, next_use_time
                        else:
                            return False, None
                except Exception as e:
                    print(f"Error claiming weekly reward for user {user_id}: {e}")
                    await conn.rollback()
                    return False, e