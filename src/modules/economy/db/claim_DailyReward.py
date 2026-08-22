from datetime import datetime, timedelta, timezone

import db_connection

async def claimDailyReward(user_id: int):
    """
    Claims the daily reward for a user.

    Args:
        user_id (int): The ID of the user claiming the reward.

    Returns:
        tuple: A tuple containing a boolean indicating success and the next use time.
    """
    async with db_connection._ActivePool.acquire() as conn:
        async with conn.cursor() as cursor:
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
                    new_cooldown = datetime.now(timezone.utc) + timedelta(days=1)
                    return True, new_cooldown
                else:
                    await conn.rollback()
                    await cursor.execute("SELECT DailyRewardNextUse FROM Economy WHERE UserID = %s", (user_id,))
                    result = await cursor.fetchone()
                    if result:
                        next_use_time = result[0]
                        return False, next_use_time
                    else:
                        return False, None
            except Exception as e:
                print(f"Error claiming daily reward for user {user_id}: {e}")
                await conn.rollback()
                return False, e