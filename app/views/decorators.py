def remove_xss_protection(response):
    response.headers['X-XSS-Protection'] = 0
    return response