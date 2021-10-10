pkgname = "awk"
pkgver = "20210215"
pkgrel = 0
_commit="c0f4e97e4561ff42544e92512bbaf3d7d1f6a671"
hostmakedepends = ["byacc"]
pkgdesc = "One true awk"
maintainer = "q66 <q66@chimera-linux.org>"
license = "SMLNJ"
url = "https://github.com/onetrueawk/awk"
source = f"https://github.com/onetrueawk/awk/archive/{_commit}.tar.gz"
sha256 = "8e727fc750fa96898786dc3b5b3206734cc399e4fa9f2d182ab2ad2473f31118"
# test suite uses local tools that are not present
options = ["bootstrap", "!check"]

def init_configure(self):
    from cbuild.util import make
    self.make = make.Make(self)

def do_build(self):
    self.make.build([
        "CC=" + self.get_tool("CC"),
        "HOSTCC=" + self.get_tool("CC"),
        "CFLAGS=" + self.get_cflags(shell = True) + " " + \
                    self.get_ldflags(shell = True) + " -DHAS_ISBLANK",
        "YACC=byacc -H awkgram.tab.h -o awkgram.tab.c",
    ])

def do_check(self):
    self.make.check()

def do_install(self):
    self.cp("a.out", "awk")
    self.install_bin("awk")
    self.install_man("awk.1")
    self.install_license("LICENSE")
