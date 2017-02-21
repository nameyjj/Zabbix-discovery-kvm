#!/usr/bin/python
import libvirt
import json
import sys
from lxml import etree

class kvmDiscovery(object):

  def __init__(self):
    self.conn = libvirt.open("qemu:///system")
    self.DomainsID = self.conn.listDomainsID()

  def __del__(self):
    self.conn.close()

  def template(self,parent_name,sdev,tdev):
    data = {"data":[]}
    for i in self.DomainsID:
      dom = self.conn.lookupByID(i)
      dom_name = dom.name()
      xml = dom.XMLDesc(0)
      tree = etree.HTML(xml)
      parent_tab = tree.xpath(parent_name)
      for j in parent_tab:
        if j.attrib['type'] == 'file': 
            if j.attrib['device'] == 'disk':
                sdev='source/@file'
            else:
                continue
        source = j.xpath(sdev)[0]
        target = j.xpath(tdev)[0]
        info = {
		"{#SDEV}"  : source,
		"{#TDEV}"  : target,
		"{#DNAME}" : dom_name
	}
        data['data'].append(info)
    return json.dumps(data)

  def getInterface(self):
    return self.template('//devices/interface','source/@bridge','target/@dev')


  def getDisk(self):
    return self.template('//devices/disk','source/@dev','target/@dev')
   
  def getDomain(self):
    data = {"data":[]}
    for i in self.DomainsID:
      dom_name = self.conn.lookupByID(i).name()
      info = { "{#DNAME}" : dom_name }
      data['data'].append(info)
    return json.dumps(data)
    
if __name__ == '__main__':
  if len(sys.argv) != 2: sys.exit()
  if sys.argv[1] == 'domain':
    print kvmDiscovery().getDomain()
  elif sys.argv[1] == 'interface':
    print kvmDiscovery().getInterface()
  elif sys.argv[1] == 'disk':
    print kvmDiscovery().getDisk()

