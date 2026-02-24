def validate_password_strength(password:str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    has_upper = False
    has_numbers = False
    for c in password:
        if c.isupper(): has_upper = True
        if c.isdigit(): has_numbers = True
        if has_numbers and has_upper:
            break
    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    if not has_numbers:
        return False, "Password must contain at least one number"    
    return True, ""