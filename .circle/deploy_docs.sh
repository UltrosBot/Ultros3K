sftp -b .circle/upload_docs leaf@ultros.io
ssh -t leaf@ultros.io "cd /home/leaf/ ; /usr/bin/bash -c ./unpack_docs.sh"
