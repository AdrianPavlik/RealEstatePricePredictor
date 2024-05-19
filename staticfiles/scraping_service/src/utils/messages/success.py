def raise_default_success(handler, success_message):
    handler.write({
        "success": success_message
    })


def raise_custom_success(handler, success_message, custom_success):
    handler.write({
        "success": success_message,
        "other": custom_success
    })
