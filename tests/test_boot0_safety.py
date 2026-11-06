# SPDX-License-Identifier: GPL-2.0-only
"""Destructive-path regression tests use private regular files, never devices."""
from pathlib import Path
import importlib.util,os,tempfile,unittest

spec=importlib.util.spec_from_file_location('boot0',Path(__file__).resolve().parents[1]/'scripts/u3-emmc-boot0.py')
boot=importlib.util.module_from_spec(spec);spec.loader.exec_module(boot)
class Boot0Safety(unittest.TestCase):
    def setUp(self):
        self.file=tempfile.TemporaryFile();self.fd=self.file.fileno()
        self.before=(bytes(range(256))*((boot.PREFIX_BYTES+65536)//256))
        self.file.write(self.before);self.file.flush();self.prefix=b'\xa5'*boot.PREFIX_BYTES
    def tearDown(self):self.file.close()
    def test_only_prefix_changes_and_tail_is_preserved(self):
        after=boot.replace_prefix(self.fd,self.before,self.prefix)
        self.assertEqual(os.pread(self.fd,len(self.before),0),self.prefix+self.before[boot.PREFIX_BYTES:])
        self.assertEqual(after[boot.PREFIX_BYTES:],self.before[boot.PREFIX_BYTES:])
    def test_partial_write_exception_restores_whole_previous_state(self):
        def failed(fd,data):os.pwrite(fd,data[:4096],0);raise OSError('Injected interruption')
        with self.assertRaises(OSError):boot.replace_prefix(self.fd,self.before,self.prefix,failed)
        self.assertEqual(os.pread(self.fd,len(self.before),0),self.before)
    def test_silent_short_write_is_detected_and_rolled_back(self):
        def short(fd,data):os.pwrite(fd,data[:4096],0)
        with self.assertRaisesRegex(RuntimeError,'readback'):boot.replace_prefix(self.fd,self.before,self.prefix,short)
        self.assertEqual(os.pread(self.fd,len(self.before),0),self.before)
    def test_wrong_payload_length_never_calls_writer(self):
        called=[]
        with self.assertRaises(RuntimeError):boot.replace_prefix(self.fd,self.before,b'bad',lambda *a:called.append(a))
        self.assertEqual(called,[]);self.assertEqual(os.pread(self.fd,len(self.before),0),self.before)
    def test_wrong_card_access_path_and_boot_configuration_are_refused(self):
        info={'cid':'1'*32,'sd_adapter_path':True,'root_on_selected_card':True,'partition_config':0x48,'boot_bus_width':1,'boot_write_protect':0,'force_ro':'1'}
        boot.write_guard(info,'1'*32)
        for key,value in [('cid','2'*32),('sd_adapter_path',False),('root_on_selected_card',False),('partition_config',0),('boot_bus_width',0),('boot_write_protect',1),('force_ro','0')]:
            with self.subTest(key=key),self.assertRaises(RuntimeError):boot.write_guard({**info,key:value},'1'*32)
if __name__=='__main__':unittest.main()
