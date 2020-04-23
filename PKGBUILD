# Maintainer: Aditya Sirish <aditya.sirish@nyu.edu>

pkgname=('stat-script')
pkgver=0.1.6
pkgrel=1
pkgdesc="A dirty but dep-less way to stat your targets"
arch=('any')
license=('Apache')
url="https://saky.in"
depends=('python')
source=("stat-script.py"
        "setup.py")
sha256sums=('SKIP' 'SKIP')

package() {
	python setup.py build
	mkdir -p "${pkgdir}/usr/local/stat-script" "${pkgdir}/usr/bin"
	cp -dr --preserve=mode,timestamp build/exe.linux-x86_64-3.8/* "${pkgdir}/usr/local/stat-script/"
	ln -s "/usr/local/stat-script/stat-script" "${pkgdir}/usr/bin/stat-script"
}
