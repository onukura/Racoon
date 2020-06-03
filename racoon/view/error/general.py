# -*- coding: utf-8 -*-
from flask import render_template


# Custom Error Handlers for general error codes
def err_404(e):
    return (
        render_template(
            "error/error_base.html",
            error_code=404,
            header_name="Page not found",
            error_message="",
        ),
        404,
    )


def err_500(e):
    return (
        render_template(
            "error/error_base.html",
            error_code=500,
            header_name="Internal server error",
            error_message="",
        ),
        500,
    )
