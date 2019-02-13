
cd $(dirname $0)

./xls2html.py ./ServerlessLabs.xls 

cp -a images/* ../images/

cat Path*.html | grep -vE "<H1>|<\/?STYLE>|<\/?HTML>|<\/?BODY>|<DOCTYPE HTML>" > ADD_TO_MARKDOWN.html


