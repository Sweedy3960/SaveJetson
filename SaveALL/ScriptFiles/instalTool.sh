

sudo apt-get install curl
print("curl ok")
cd ~/Téléchargements
curl -L https://github.com/toolboc/vscode/releases/download/1.32.3/code-oss_1.32.3-arm64.deb -o code-oss_1.32.3-arm64.deb

sudo dpkg -i code.oss_1.32.3-arm64.deb
print("good work")
