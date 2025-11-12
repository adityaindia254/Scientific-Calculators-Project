def calculate_basic(expr):
    try:
        return eval(expr)
    except Exception as e:
        return f"Error: {str(e)}"
