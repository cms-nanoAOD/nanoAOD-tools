#!/usr/bin/env python

import json
import os
import pycurl
from cStringIO import StringIO
from pprint import pprint
from CRABClient.UserUtilities import getUsernameFromCRIC

class Crab3ToolsException(Exception):
    pass

class UserCacheHelper:
    def __init__(self, proxy=None, user=None):
        if proxy is None:
            #proxy = os.getenv('X509_USER_PROXY')
            proxy = '/tmp/x509up_u103214'
        if not proxy or not os.path.isfile(proxy):
            raise Crab3ToolsException('X509_USER_PROXY is %r, get grid proxy first' % proxy)
        self.proxy = proxy

        if user is None:
            user = getUsernameFromCRIC()
        if not user:
            raise Crab3ToolsException('could not get username from CRIC, returned %r' % user)
        self.user = user

    def _curl(self, url):
        buf = StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, str(url))
        c.setopt(pycurl.WRITEFUNCTION, buf.write)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.SSLKEY, self.proxy)
        c.setopt(pycurl.SSLCERT, self.proxy)
        c.perform()
        j = buf.getvalue().replace('\n','')
        try:
            return json.loads(j)['result']
        except ValueError:
            raise Crab3ToolsException('json decoding problem: %r' % j)

    def _only(self, l):
        if len(l) != 1:
            raise Crab3ToolsException('return value was supposed to have one element, but: %r' % l)
        return l[0]

    def listusers(self):
        return self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=listusers')

    def userinfo(self):
        return self._only(self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=userinfo&username=' + self.user))

    def quota(self):
        return self._only(self.userinfo()['used_space'])

    def filelist(self):
        return self.userinfo()['file_list']

    def fileinfo(self, hashkey):
        return self._only(self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=fileinfo&hashkey=' + hashkey))

    def fileinfos(self):
        return [self.fileinfo(x) for x in self.filelist() if '.log' not in x] # why doesn't it work for e.g. '150630_200330:tucker_crab_repubmerge_tau0300um_M0400_TaskWorker.log' (even after quoting the :)?

    def fileremove(self, hashkey):
        x = self._only(self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=fileremove&hashkey=' + hashkey))
        if x:
            raise Crab3ToolsException('fileremove failed: %r' % x)

if __name__ == '__main__':
    h = UserCacheHelper()
    for x in h.filelist():
        if '.log' in x:
            continue
        print 'remove', x
        h.fileremove(x)
