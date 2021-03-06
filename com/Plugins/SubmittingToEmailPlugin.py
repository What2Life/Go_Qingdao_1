#! /usr/bin/python
# -*- coding:utf-8 -*-

from pandas import Series
from com.Plugins.AbstractPlugin import AbstractPlugin
from com.Common.HttpRequest import *

class SubmittingToEmailPlugin(AbstractPlugin):
    def __init__(self):
        AbstractPlugin.__init__(self, "submitting_to_email")

    def do_extract(self, simple_data):
        features = []
        count = 0
        for values in simple_data.values:
            count = count + 1
            print "[submitting_to_email][%s]" %count
            soup = self.get_soup(values[0])
            if soup is None:
                features.append(0)
                continue

            try:
                if "mail(" in soup.prettify() and "?>" in soup.prettify():
                    features.append(1)
                    print "[submitting_to_email][Phishing] %s" %values[1]
                    continue

                is_phishing_website = False
                for tag_form in soup.findAll("form"):
                    if not tag_form.has_attr("action"):
                        continue
                    if "mailto:" in tag_form["action"].lower():
                        is_phishing_website = True
                        break
            except RuntimeError:
                print "RuntimeError!!"

            if is_phishing_website:
                features.append(1)
                print "[submitting_to_email][Phishing] %s" %values[1]
            else:
                features.append(0)

        return Series(features)
