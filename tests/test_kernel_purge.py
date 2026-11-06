from pathlib import Path
import importlib.util,json,tempfile,unittest
path=Path(__file__).resolve().parents[1]/'boards/u3/support/kernel-package-postrm.py'
spec=importlib.util.spec_from_file_location('purge',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Purge(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.release='6.12.114-odroidu3-v1';(self.root/'boot/extlinux').mkdir(parents=True);(self.root/'boot/uImage').write_bytes(b'active');self.modules=self.root/'usr/lib/modules'/self.release;self.modules.mkdir(parents=True);(self.modules/'modules.dep').write_bytes(b'generated');self.hashes={}
  for source,template in m.BOOT_NAMES.items():
   p=self.root/'boot'/template.format(release=self.release);p.write_bytes(source.encode());self.hashes[source]=m.sha(p)
  (self.root/'boot/extlinux/extlinux.conf').write_text('DEFAULT live\nLABEL live\n LINUX /vmlinuz-live\nLABEL old\n LINUX /vmlinuz-'+self.release+'\n FDT /exynos4412-odroidu3-'+self.release+'.dtb\n')
 def tearDown(self):self.tmp.cleanup()
 def cleanup(self,running='7.3.1-odroidu3-v3'):return m.cleanup(self.root,self.release,self.hashes,running)
 def test_removes_only_uninstalled_kernel_boot_and_generated_indices(self):
  result=self.cleanup();self.assertEqual(result['removed_inactive_menu_entries'],['old']);self.assertFalse(self.modules.exists());self.assertEqual((self.root/'boot/uImage').read_bytes(),b'active')
  for template in m.BOOT_NAMES.values():self.assertFalse((self.root/'boot'/template.format(release=self.release)).exists())
  self.assertIn('LABEL live',(self.root/'boot/extlinux/extlinux.conf').read_text());self.assertTrue(list((self.root/'var/lib/odroid-kernel/removed').glob('*.conf')))
 def test_running_selected_and_fallback_are_protected(self):
  for field in ['running','active_release','previous_running']:
   with self.subTest(field=field):
    state=self.root/'var/lib/odroid-kernel/state.json';state.parent.mkdir(parents=True,exist_ok=True);state.write_text(json.dumps({field:self.release}))
    with self.assertRaises(RuntimeError):self.cleanup(self.release if field=='running' else 'other')
    self.assertTrue((self.modules/'modules.dep').exists())
 def test_preserves_modified_boot_and_unknown_modules(self):
  p=self.root/'boot'/('config-'+self.release);p.write_bytes(b'owner-change');(self.modules/'custom.ko').write_bytes(b'foreign');self.cleanup();self.assertEqual(p.read_bytes(),b'owner-change');self.assertEqual((self.modules/'custom.ko').read_bytes(),b'foreign')
 def test_selected_menu_refuses_before_any_cleanup(self):
  p=self.root/'boot/extlinux/extlinux.conf';p.write_text(p.read_text().replace('DEFAULT live','DEFAULT old'))
  with self.assertRaises(RuntimeError):self.cleanup()
  self.assertTrue((self.modules/'modules.dep').exists());self.assertTrue((self.root/'boot'/('config-'+self.release)).exists())
 def test_implicit_first_menu_entry_is_protected(self):
  p=self.root/'boot/extlinux/extlinux.conf';p.write_text('LABEL old\n LINUX /vmlinuz-'+self.release+'\n')
  with self.assertRaises(RuntimeError):self.cleanup()
 def test_symlink_module_directory_is_never_followed(self):
  (self.modules/'modules.dep').unlink();self.modules.rmdir();foreign=self.root/'foreign';foreign.mkdir();(foreign/'modules.dep').write_bytes(b'foreign');self.modules.symlink_to(foreign,target_is_directory=True)
  with self.assertRaises(RuntimeError):self.cleanup()
  self.assertEqual((foreign/'modules.dep').read_bytes(),b'foreign')
 def test_installed_payload_is_protected(self):
  (self.root/'usr/lib/odroid-u3/kernels'/self.release).mkdir(parents=True)
  with self.assertRaises(RuntimeError):self.cleanup()
 def test_shared_dtb_reference_is_kept(self):
  p=self.root/'boot/extlinux/extlinux.conf';p.write_text(p.read_text().replace(' LINUX /vmlinuz-live',' LINUX /vmlinuz-live\n FDT /exynos4412-odroidu3-'+self.release+'.dtb'));self.cleanup();self.assertTrue((self.root/'boot'/('exynos4412-odroidu3-'+self.release+'.dtb')).exists())
if __name__=='__main__':unittest.main()
