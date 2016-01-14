#!/usr/bin/python

import libvirt
import sys
import time

class getKVMInfo(object):
  def __init__(self,dom_name):
    self.conn = libvirt.open("qemu:///system")
    self.dom = self.conn.lookupByName(dom_name)

  def __del__(self):
    self.conn.close()

  def cpuTime(self,type):
    start = self.dom.getCPUStats(1,0)[0][type]
    stime = time.time()
    time.sleep(0.1)
    end = self.dom.getCPUStats(1,0)[0][type]
    etime = time.time()
    cpuutil = (end - start + 0.0) / 10000000 / (etime - stime)
    return cpuutil

  def vcpuInfo(self):
    return self.dom.maxVcpus()

  def inTraffic(self,interface):
    data = self.dom.interfaceStats(interface)
    return data[0]

  def outTraffic(self,interface):
    data = self.dom.interfaceStats(interface)
    return data[4]

  def inPackets(self,interface):
    data = self.dom.interfaceStats(interface)
    return data[1]

  def outPackets(self,interface):
    data = self.dom.interfaceStats(interface)
    return data[5]

  def rd_req(self,disk):
    data = self.dom.blockStats(disk)
    return data[0]

  def rd_bytes(self,disk):
    data = self.dom.blockStats(disk)
    return data[1]

  def wr_req(self,disk):
    data = self.dom.blockStats(disk)
    return data[2]

  def wr_bytes(self,disk):
    data = self.dom.blockStats(disk)
    return data[3]

  def rss_Memory(self):
    data = self.dom.memoryStats()
    return data[rss]

if __name__ == '__main__':
  if sys.argv[1] == 'interface':
    if sys.argv[2] == 'inTraffic': print getKVMInfo(sys.argv[3]).inTraffic(sys.argv[4])
    if sys.argv[2] == 'outTraffic': print getKVMInfo(sys.argv[3]).outTraffic(sys.argv[4])
    if sys.argv[2] == 'inPackets': print getKVMInfo(sys.argv[3]).inPackets(sys.argv[4])
    if sys.argv[2] == 'outPackets': print getKVMInfo(sys.argv[3]).outPackets(sys.argv[4])
  elif sys.argv[1] == 'disk':
    if sys.argv[2] == 'rd_req' : print getKVMInfo(sys.argv[3]).rd_req(sys.argv[4])
    if sys.argv[2] == 'rd_bytes' : print getKVMInfo(sys.argv[3]).rd_bytes(sys.argv[4])
    if sys.argv[2] == 'wr_req' : print getKVMInfo(sys.argv[3]).wr_req(sys.argv[4])
    if sys.argv[2] == 'wr_bytes' : print getKVMInfo(sys.argv[3]).wr_bytes(sys.argv[4])
  elif sys.argv[1] == 'memory':
    print getKVMInfo(sys.argv[3]).rss_Memory()
  elif sys.argv[1] == 'cpu':
    if sys.argv[2] == 'cputime': print  getKVMInfo(sys.argv[3]).cpuTime('cpu_time')
    if sys.argv[2] == 'systime': print  getKVMInfo(sys.argv[3]).cpuTime('system_time')
    if sys.argv[2] == 'usertime': print  getKVMInfo(sys.argv[3]).cpuTime('user_time')
    if sys.argv[2] == 'cpuinfo' : print getKVMInfo(sys.argv[3]).vcpuInfo()
