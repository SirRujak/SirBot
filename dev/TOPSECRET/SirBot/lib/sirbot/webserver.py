import socket
import time
import webbrowser

    i = 0
    HOST = '127.0.0.1'
    PORT = 8887

    header = """HTTP/1.1 200 OK\r\nConnection: keep-alive\r\nContent-Type: text/html; encoding=utf8\r\nStatus: 200 OK\r\n\r\n""".encode()

    page = """
    <!doctype html>
    <html>
    <head>
      <title>SirBot Notifications</title>
      <style type="text/css">
        .notify {
          position: fixed;
          top: 5%;
          color: white;
          -moz-animation-duration: 7s;
          -webkit-animation-duration: 7s;
          -moz-animation-name: slidein;
          -webkit-animation-name: slidein;
          -webkit-animation-fill-mode: forwards;
          animation-fill-mode: forwards;

        }
        
        @-moz-keyframes slidein {
          from {
            font-size:100%;
            margin-left:100%;
            width:auto;
            opacity:.5;

          }

          25% {
            font-size:100%;
            margin-left:45%;
            width:auto;
            opacity:1;
          }
          
          85% {
            font-size:100%;
            margin-left:45%;
            width:auto;
            opacity:1;

          }
          
          to {
            margin-left:-50%;
            width:auto;
            opacity:0;
          }
        }
        
        @-webkit-keyframes slidein {
          from {
            font-size:150%;
            margin-left:100%;
            width:auto;
            opacity:.5;
          }

          25% {
            font-size:150%;
            margin-left:55%;
            width:auto;
            opacity:1;
          }
          
          
          85% {
            font-size:150%;
            margin-left:45%;
            width:auto;
            opacity:1;
          }
          
          to {
            margin-left:-50%;
            width:auto;
            opacity:0;
          }

          
        }

        body {
          background-color: #3496B2;
        }

        img {
          z-index: -1;
        }

      </style>
    </head>
    <body>
      <h1 class="notify">WELCOME</h1>
    </body>
    </html>
    """.encode()

    foundation = header+page

    def pagex(i,name):
        data = """ <h""" + str(i) + """ class="notify">"""+str(name).upper()+"""</h"""+str(i)+">"
##                +"""\n<audio src="r2d2notice.mp3" type="audio/mp3" autoplay></audio>"""
        data = data.encode()
        return(data)

    def start():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        webbrowser.open_new('http://127.0.0.1:8887')
        (conn,addr) = s.accept()
        temp=conn.recv(4096)
        conn.sendall(foundation)

    def newFollowerAnimation(user):
        conn.sendall(pagex(i,user))
        
