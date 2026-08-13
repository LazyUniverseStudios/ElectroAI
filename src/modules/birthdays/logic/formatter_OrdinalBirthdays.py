def format_ordinal_date(date_str : str) -> str:
    """
    Format a date string into an ordinal date format.

    Args:
        date_str (str): The date string in 'YYYY-MM-DD' format.

    Returns:
        str: The formatted ordinal date string.
    """
    from datetime import datetime
    # Wrap in str() so it works whether date_str is a string or a date object
    if isinstance(date_str, str):
        # Parse the input date string
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        date_obj = date_str

    # Get the day of the month
    day = date_obj.day

    # Determine the ordinal suffix
    if day in [1, 21, 31]:
        suffix = 'st'
    elif day in [2, 22]:
        suffix = 'nd'
    elif day in [3, 23]:
        suffix = 'rd'
    else:
        suffix = 'th'

    # Format the ordinal date
    ordinal_date = f"{day}{suffix} {date_obj.strftime('%B')}"
    
    return ordinal_date