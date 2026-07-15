# Multi Threaded Web Server
This is a simple multi thread HTTP web server written in Python.
The server uses low-level TCP sockets to accept client connections, read HTTP GET requests, and return static files from the static folder.

It supports basic HTTP responses such as 200 OK, 400 Bad request, and 404 Not found.

# Features
- Built with Python sockets
- Handles HTTP GET requests
- Serves static files from the `static` directory
- Supports files from sub-folders
- Returns `200 OK` for existing files
- Returns `404 Not Found` for missing files
- Returns `400 Bad Request` for invalid requests
- Blocks directory traversal attempts using `..`
- Does not allow directory listing
- Uses threads to handle multiple client connections
- Sends `Content-Length` and `Content-Type` headers

#Project structure
```text
Pythonwork/
    server.py
    README.md
    static/
         index.html
         pages/
            info.html
            testpage.html
         assets/
            style.css
         files/
            demo.txt


Open a terminal in the project folder and run:

python server.py

The server will run at:

http://localhost:8080


## Browser Tests

Open these URLs in a browser:

http://localhost:8080/
http://localhost:8080/index.html
http://localhost:8080/pages/info.html
http://localhost:8080/pages/tests.html
http://localhost:8080/files/demo.txt


##Curl tests

Testing a regular HTML file:

curl.exe -v http://localhost:8080/index.html

Expected result:
HTTP/1.0 200 OK

Testing the CSS file:

curl.exe -v http://localhost:8080/assets/style.css

Expected result:
HTTP/1.0 200 OK


Testing the text file:

bash
curl.exe -v http://localhost:8080/files/demo.txt

Expected result:

HTTP/1.0 200 OK
Content-Type: text/plain


Test a missing file:

curl.exe -v http://localhost:8080/whatever.html


Expected result:

HTTP/1.0 404 Not Found

Test directory access:

bash
curl.exe -v http://localhost:8080/pages/

Expected result:
HTTP/1.0 400 Bad Request


Test directory traversal blocking:

bash
curl.exe -v --path-as-is http://localhost:8080/../secret.txt

Expected result:
HTTP/1.0 400 Bad Request

