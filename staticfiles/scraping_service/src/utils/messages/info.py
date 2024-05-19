def raise_default_info(handler, info_message):
    handler.write({
        "info": info_message
    })


def raise_custom_info(handler, info_message, custom_info):
    handler.write({
        "info": info_message,
        "other": custom_info
    })
