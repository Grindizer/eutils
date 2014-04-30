import lxml.etree

class Base(object):

    def __init__(self, xml=None, root=None):
        self._xml = xml
        self._xmlroot = root if root else lxml.etree.XML(xml)

    def __str__(self):
        return unicode(self).encode('utf-8')

    @classmethod
    def _validate_xml(xml):
        """validate the xml during initialization. Subclasses override this
        to apply any __init__-time validation of the incoming XML"""
        pass
