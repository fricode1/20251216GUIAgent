from DrissionPage import Chromium
tab = Chromium().latest_tab
tab.get('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_iframe')
print(tab.html)