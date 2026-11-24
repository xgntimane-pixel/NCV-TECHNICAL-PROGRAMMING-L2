def is_valid_time(time_str):
    """Check if time_str is a valid mm:ss (minutes >= 0, seconds 0-59)."""
    if ':' not in time_str:
        return False
    parts = time_str.split(':')
    if len(parts) != 2:
        return False
    mm, ss = parts
    if not (mm.isdigit() and ss.isdigit()):
        return False
    minutes = int(mm)
    seconds = int(ss)
    if minutes < 0 or seconds < 0 or seconds > 59:
        return False
    return True

def time_to_seconds(time_str):
    """Convert valid mm:ss to total seconds."""
    mm, ss = time_str.split(':')
    return int(mm) * 60 + int(ss)

qualifiers = 0
winner_name = None
winner_seconds = None
first_valid = True

print("Enter athlete name and time (mm:ss). Type 'x' to finish.")

while True:
    line = input().strip()
    if line.lower() == 'x':
        break
    if not line:
        continue

    parts = line.split()
    if len(parts) < 2:
        continue

    name = parts[0]
    time_str = parts[1]

    if not is_valid_time(time_str):
       continue

    total_seconds = time_to_seconds(time_str)

    
    if total_seconds <= 1500:
        qualifiers += 1

    
    if first_valid or total_seconds < winner_seconds:
        winner_name = name
        winner_seconds = total_seconds
        first_valid = False
    
if winner_name is None:
    print("Nobody entered.")
    print("Qualified: 0")
else:
    win_mm = winner_seconds // 60
    win_ss = winner_seconds % 60
    print(f"Winner: {winner_name} ({win_mm:02d}:{win_ss:02d})")
    print(f"Qualified: {qualifiers}")