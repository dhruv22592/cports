pkgname = "gobject-introspection"
pkgver = "1.78.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = ["meson", "pkgconf", "flex", "bison"]
makedepends = [
    "libffi-devel",
    "glib-devel",
    "python-devel",
    "python-mako",
    "python-markdown",
]
depends = ["libgirepository-devel", "python-mako", "python-markdown"]
pkgdesc = "Introspection system for GObject-based libraries"
maintainer = "q66 <q66@chimera-linux.org>"
license = "GPL-2.0-or-later AND LGPL-2.1-or-later"
url = "https://wiki.gnome.org/Projects/GObjectIntrospection"
source = f"$(GNOME_SITE)/{pkgname}/{pkgver[:-2]}/{pkgname}-{pkgver}.tar.xz"
sha256 = "84f5bd2038bd52abbce74a639832c5b46a2d17e9c5a8ae14f9788e8516c04166"
# FIXME int (fails e.g. gstreamer)
hardening = ["!int"]
# check creates a dependency cycle
# cross compiling tons of janky hackery
options = ["!check", "!cross"]


def post_install(self):
    from cbuild.util import python

    for f in (self.destdir / f"usr/lib/{pkgname}/giscanner").glob(
        "_giscanner*.so"
    ):
        self.mv(f, f.with_name("_giscanner.so"))

    python.precompile(self, f"usr/lib/{pkgname}/giscanner")


@subpackage("gir-freedesktop")
def _girfdo(self):
    self.pkgdesc = "Introspection data for some freedesktop components"

    return ["usr/lib/girepository-1.0"]


@subpackage("libgirepository")
def _libgir(self):
    self.pkgdesc = "Library for handling gir data (runtime library)"
    self.depends += [f"gir-freedesktop={pkgver}-r{pkgrel}"]

    return self.default_libs()


@subpackage("libgirepository-devel")
def _devel(self):
    self.pkgdesc = "Library for handling gir data (development files)"
    self.depends += ["cairo-devel", "libffi-devel"]

    return self.default_devel()
