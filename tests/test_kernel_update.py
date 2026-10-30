from pathlib import Path
import importlib.machinery,importlib.util,json,hashlib,struct,tempfile,unittest,zlib
from unittest.mock import patch
path=Path(__file__).resolve().parents[1]/'boards/u3/support/odroid-kernel';loader=importlib.machinery.SourceFileLoader('kernel_update',str(path));spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
def image(data):
 h=struct.pack('>7I4B32s',0x27051956,0,0,len(data),0x40008000,0x40008000,zlib.crc32(data),5,2,2,0,b'test');h=bytearray(h);struct.pack_into('>I',h,4,zlib.crc32(h));return bytes(h)+data
class KernelUpdate(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'boot/extlinux').mkdir(parents=True);(self.root/'boot/uImage').write_bytes(b'original');(self.root/'boot/extlinux/extlinux.conf').write_text('DEFAULT ubuntu26\nLABEL ubuntu26\n LINUX /zImage\n FDT /exynos4412-odroidu3.dtb\n APPEND root=PARTUUID=abc-02 ro quiet\n');self.old={n:(self.root/'boot'/n).read_bytes() for n in m.FILES};(self.root/'usr/lib/modules/6.12.114-odroidu3-v1').mkdir(parents=True)
 def tearDown(self):self.tmp.cleanup()
 def payload(self,release):
  p=self.root/'usr/lib/odroid-u3/kernels'/release;p.mkdir(parents=True);(p/'zImage').write_bytes(release.encode());(p/'exynos4412-odroidu3.dtb').write_bytes(b'dtb');(p/'uImage').write_bytes(image((p/'zImage').read_bytes()+b'dtb'));ko=self.root/'usr/lib/modules'/release/'driver.ko';ko.parent.mkdir(parents=True);ko.write_bytes(b'module');(p/'config').write_bytes(b'config');(p/'System.map').write_bytes(b'map');manifest={'board':'ODROID-U3','architecture':'armhf','kernel_release':release,'files':{n:m.sha(p/n) for n in ['zImage','exynos4412-odroidu3.dtb','uImage','config','System.map']},'modules':{'driver.ko':m.sha(ko)}};(p/'MANIFEST.json').write_text(json.dumps(manifest));return p
 def test_activate_and_rollback_preserve_bootargs_and_old_data(self):
  r='6.12.115-odroidu3-v1';self.payload(r);result=m.activate(self.root,r,'abc-02','6.12.114-odroidu3-v1');self.assertTrue(result['changed']);self.assertIn('root=PARTUUID=abc-02 ro quiet',(self.root/'boot/extlinux/extlinux.conf').read_text());self.assertTrue((self.root/'boot'/('vmlinuz-'+r)).exists());m.rollback(self.root,'abc-02',r);self.assertEqual({n:(self.root/'boot'/n).read_bytes() for n in m.FILES},self.old)
 def test_second_file_failure_restores_all_files_and_state(self):
  def fail(path,data):
   if path==self.root/'boot/uImage':raise OSError('injected write failure')
   m.atomic(path,data)
  with self.assertRaises(OSError):m.commit_boot(self.root,{n:b'new' for n in m.FILES},{'active_release':'new'},write=fail)
  self.assertEqual({n:(self.root/'boot'/n).read_bytes() for n in m.FILES},self.old);self.assertFalse((self.root/'var/lib/odroid-kernel/state.json').exists())
 def test_corrupt_payload_cannot_change_boot(self):
  p=self.payload('6.12.115-odroidu3-v1');(p/'zImage').write_bytes(b'corrupt')
  with self.assertRaises(RuntimeError):m.activate(self.root,'6.12.115-odroidu3-v1','abc-02','6.12.114-odroidu3-v1')
  self.assertEqual((self.root/'boot/uImage').read_bytes(),b'original')
 def test_pending_updates_keep_known_running_fallback(self):
  self.payload('6.12.115-odroidu3-v1');self.payload('6.12.116-odroidu3-v1');m.activate(self.root,'6.12.115-odroidu3-v1','abc-02','6.12.114-odroidu3-v1');first=m.readstate(self.root)['previous_snapshot'];m.activate(self.root,'6.12.116-odroidu3-v1','abc-02','6.12.114-odroidu3-v1');self.assertEqual(m.readstate(self.root)['previous_snapshot'],first);text=(self.root/'boot/extlinux/extlinux.conf').read_text();prev=text.split('LABEL odroid-managed-previous',1)[1];self.assertIn('LINUX /zImage',prev);m.rollback(self.root,'abc-02','6.12.114-odroidu3-v1');self.assertEqual((self.root/'boot/uImage').read_bytes(),b'original')
 def test_wrong_media_rollback_is_refused(self):
  self.payload('6.12.115-odroidu3-v1');m.activate(self.root,'6.12.115-odroidu3-v1','abc-02','6.12.114-odroidu3-v1');before=(self.root/'boot/uImage').read_bytes()
  with self.assertRaises(RuntimeError):m.rollback(self.root,'wrong-02','6.12.115-odroidu3-v1')
  self.assertEqual((self.root/'boot/uImage').read_bytes(),before)
 def test_symlink_boot_payload_directory_is_refused(self):
  self.payload('6.12.115-odroidu3-v1');(self.root/'boot/vmlinuz-6.12.115-odroidu3-v1').symlink_to(self.root/'foreign')
  with self.assertRaises(RuntimeError):m.activate(self.root,'6.12.115-odroidu3-v1','abc-02','6.12.114-odroidu3-v1')
  self.assertFalse((self.root/'foreign').exists())
 def test_wrong_selected_root_is_refused_despite_valid_other_entry(self):
  self.payload('6.12.115-odroidu3-v1');(self.root/'boot/extlinux/extlinux.conf').write_text('DEFAULT wrong\nLABEL wrong\n LINUX /zImage\n APPEND root=PARTUUID=other-02 ro\nLABEL fallback\n LINUX /zImage\n APPEND root=PARTUUID=abc-02 ro\n')
  with self.assertRaises(RuntimeError):m.activate(self.root,'6.12.115-odroidu3-v1','abc-02','6.12.114-odroidu3-v1')
  self.assertEqual((self.root/'boot/uImage').read_bytes(),b'original')
 def test_existing_state_cannot_be_reused_for_another_root(self):
  r='6.12.115-odroidu3-v1';self.payload(r);m.activate(self.root,r,'abc-02','6.12.114-odroidu3-v1');before=(self.root/'boot/uImage').read_bytes()
  with self.assertRaises(RuntimeError):m.activate(self.root,r,'other-02',r)
  self.assertEqual((self.root/'boot/uImage').read_bytes(),before)
 def test_flat_collision_cannot_overwrite_existing_version(self):
  r='7.3.1-odroidu3-v2';self.payload(r);target=self.root/'boot'/('vmlinuz-'+r);target.write_bytes(b'foreign')
  with self.assertRaises(RuntimeError):m.activate(self.root,r,'abc-02','6.12.114-odroidu3-v1')
  self.assertEqual(target.read_bytes(),b'foreign');self.assertEqual((self.root/'boot/uImage').read_bytes(),b'original')
 def test_flat_boot_is_complete_and_activation_idempotent(self):
  r='7.3.1-odroidu3-v2';self.payload(r);m.activate(self.root,r,'abc-02','6.12.114-odroidu3-v1')
  for n,t in m.BOOT_NAMES.items():self.assertTrue((self.root/'boot'/t.format(release=r)).is_file())
  self.assertFalse((self.root/'boot/odroid-kernels').exists());self.assertFalse(m.activate(self.root,r,'abc-02',r)['changed'])
if __name__=='__main__':unittest.main()
