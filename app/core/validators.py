# app/core/validators.py
import re
from typing import List
from app.core.exceptions import InvalidSymbolError

def validate_stock_symbol(symbol: str) -> str:
    """
    Validate stock symbol format
    - Must be 1-5 uppercase letters
    - No special characters or numbers
    """
    if not symbol:
        raise InvalidSymbolError("empty")
    
    # Convert to uppercase
    symbol = symbol.upper().strip()
    
    # Check format
    if not re.match(r'^[A-Z]{1,5}$', symbol):
        raise InvalidSymbolError(symbol)
    
    return symbol

def validate_symbols_batch(symbols: List[str], max_batch_size: int = 10) -> List[str]:
    """Validate batch of stock symbols"""
    if not symbols:
        raise InvalidSymbolError("empty batch")
    
    if len(symbols) > max_batch_size:
        raise InvalidSymbolError(f"Batch size exceeds maximum of {max_batch_size}")
    
    validated = []
    for symbol in symbols:
        validated.append(validate_stock_symbol(symbol))
    
    return validated
