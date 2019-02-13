
cd $(dirname $0)

./xls2html.py ./ServerlessLabs.xls 

cp -a images/* ../images/

cat Path*.html | grep -vE "<H1>|<\/?STYLE>|<\/?HTML>|<\/?BODY>|<DOCTYPE HTML>" > ADD_TO_MARKDOWN.html


README=README-2019-Jan-26_DevConf.cz_Hands-on-with-Serverless.md

cd ..

echo
if [ -f ./$README ];then
    echo "About to: append markdown to ./$README:"
    COMMAND="cat Paths/ADD_TO_MARKDOWN.html >> ./$README"
    echo "$COMMAND"
    echo "Press <return>"
    read _DUMMY
    eval "$COMMAND"
else
    echo "No such file as $README:"
    echo "Append manually ./Paths/ADD_TO_MARKDOWN.html to $README"
fi



