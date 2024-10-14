
def get_header(data):
    return str(len(data)).zfill(8).encode('utf-8')
