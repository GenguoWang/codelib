import urllib2
import re
import mail
#f = open("tmp.dat","w")
#f.write(a)
#f.close()
def main():
    a = urllib2.urlopen('http://www.myer.com.au/shop/mystore/edit-bose/bose--174%3B-215656570--1').read()
    #a = open("tmp.dat").read()
    p = re.compile(r"<span class='price'>\$([\d.]*)</span>")
    match = p.search(a)
    msg = ""
    success = False
    threshold = 400
    if match:
        priceStr = match.group(1)
        price = float(priceStr)
        if price < threshold:
            success = True
        msg += "Price: %f\n" % price
    else:
        msg += "No Match Found\n"
    if success:
        msg += "Low Price Found!\n"
        mail.sendMail(["wanggenguo@outlook.com"],"Watch", msg)
        print "email"
    print msg,
if __name__ == '__main__':
    main()
