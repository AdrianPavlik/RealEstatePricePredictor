def raise_default_error(handler, error_message):
    handler.write({
        "error": error_message
    })


def raise_custom_error(handler, error_message, custom_errors):
    handler.write({
        "error": error_message,
        "other": custom_errors
    })
