import asyncio

keys = ('method', 'path', 'Range')

# create a list to store danmu needs to send to clients
danmu_list = []


class HTTPHeader:
    """
        HTTPHeader template, you can use it directly
    """

    def __init__(self):
        self.headers = {key: None for key in keys}
        self.version = '1.0 '
        self.server = 'Tai'
        self.contentLength = None
        self.contentRange = None
        self.contentType = None
        self.location = None
        self.range = None
        self.state = None

    def parse_header(self, line):
        fileds = line.split(' ')
        if fileds[0] == 'GET' or fileds[0] == 'POST' or fileds[0] == 'HEAD':
            self.headers['method'] = fileds[0]
            self.headers['path'] = fileds[1]
        fileds = line.split(':', 1)
        if fileds[0] == 'Range':
            start, end = (fileds[1].strip().strip('bytes=')).split('-')
            self.headers['Range'] = start, end

    def set_version(self, version):
        self.version = version

    def set_location(self, location):
        self.location = location

    def set_state(self, state):
        self.state = state

    def set_info(self, contentType, contentRange):
        self.contentRange = contentRange
        self.contentType = contentType

    def set_range(self):
        start, end = self.headers['Range']
        contentRange = int(self.contentRange)
        if start == '':
            end = int(end)
            start = contentRange - end
            end = contentRange - 1
        if end == '':
            end = contentRange - 1
        start = int(start)
        end = int(end)
        self.contentLength = str(end - start + 1)
        self.range = (start, end)

    def get(self, key):
        return self.headers.get(key)

    def message(self):  # Return response header
        return 'HTTP/' + self.version + self.state + '\r\n' \
               + ('Content-Length:' + self.contentLength + '\r\n' if self.contentLength else '') \
               + ('Content-Type:' + 'text/html' + '; charset=utf-8' + '\r\n' if self.contentType else '') \
               + 'Server:' + self.server + '\r\n' \
               + ('Accept-Ranges: bytes\r\n' if self.range else '') \
               + ('Content-Range: bytes ' + str(self.range[0]) + '-' + str(
            self.range[1]) + '/' + self.contentRange + '\r\n' if self.range else '') \
               + ('Location: ' + self.location + '\r\n' if self.location else '') \
               + 'Connection: close\r\n' + '\r\n'


async def dispatch(reader, writer):
    # Use reader to receive HTTP request
    # Writer to send HTTP response
    httpHeader = HTTPHeader()
    while True:
        data = await reader.readline()
        message = data.decode()
        httpHeader.parse_header(message)
        if data == b'\r\n' or data == b'':
            break
    if httpHeader.get('method') == 'GET':
        if httpHeader.get('path') == '/':
            # handle GET PAGE request
            httpHeader.set_state('200 OK')
            writer.write(httpHeader.message().encode(encoding='utf-8'))
            html_page = open("danmu.html", encoding='utf-8')
            contents = html_page.readlines()
            homepage = ''
            for e in contents:
                homepage += e
            writer.write(homepage.encode())  # Response for GET PAGE
            writer.close()
        else:
            # handle GET DANMU request
            httpHeader.set_state('200 OK')
            writer.write(httpHeader.message().encode(encoding='utf-8'))
            if httpHeader.get('path').split('/')[1] == 'NEWDANMAKUS':
                # get the time of sending GET DANMU request
                send_time = int(httpHeader.get('path').split('/')[2])
                # get the time of each danmu in danmu_list
                for each in danmu_list:
                    # if the difference of time is less than one second, then this danmu hasn't been sent to clients
                    if send_time - each[1] <= 1000:
                        # send this danmu to clients
                        writer.write((each[0] + '|').encode(encoding='utf-8'))
                    else:
                        # remove this danmu in danmu_list
                        danmu_list.remove(each)
            writer.close()
    elif httpHeader.get('method') == 'POST' and httpHeader.get('path') == '/NEWDANMAKUS':
        # handle POST DANMU request
        danmu_text = ''
        # read danmu information from POST request
        while True:
            data = await reader.readline()
            message = data.decode()
            if data == b'Jgtl)2lL1q(D@iIW2r \n':
                break
            httpHeader.parse_header(danmu_text)
            danmu_text, send_time, useless = message.split(' ')
        httpHeader.set_state('200 OK')
        writer.write(httpHeader.message().encode(encoding='utf-8'))
        writer.close()
        # add this danmu information into danmu_list
        danmu_list.append([danmu_text, int(send_time)])


if __name__ == '__main__':
    port = 8765
    loop = asyncio.get_event_loop()
    co_ro = asyncio.start_server(dispatch, '127.0.0.1', port, loop=loop)
    server = loop.run_until_complete(co_ro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
