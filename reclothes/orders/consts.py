# Regex patterns
UUID4_REGEX = r'[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z'  # Without '-'

# Error messages
ORDER_NOT_FOUND_MSG = 'Order not found.'
CART_NOT_FOUND_MSG = 'Cart not found.'
NAME_NOT_FOUND_MSG = 'Card holder name not found.'
EXPIRY_DATE_NOT_FOUND_MSG = 'Date not found.'
INVALID_DATE_MSG = 'Invalid date.'
NUMBER_NOT_FOUND_MSG = 'Card number not found.'
INVALID_CARD_NUMBER_MSG = 'Card number must have exactly 16 digits.'
CODE_NOT_FOUND_MSG = 'Code not found.'
INVALID_CODE_MSG = 'Code must have exactly 3 digits.'
NOT_ORDER_OWNER_MSG = 'Not your order.'

# Card
CARD_NUMBER_SIZE = 16
CODE_SIZE = 3
