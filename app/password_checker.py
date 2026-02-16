def validate_password_strength(password:str) -> tuple[bool, str]:
      # Check length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check for uppercase
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for digit
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, ""