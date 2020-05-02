# Maintainer: Aditya Sirish <aditya.sirish@nyu.edu>

pkgname=('wavystats')
pkgver=0.1.1
pkgrel=1
pkgdesc="A dirty but dep-less way to stat your targets"
arch=('any')
license=('Apache')
url="https://wavybuilds.saky.in/"
depends=('python')
source=("wavystats.py"
        "setup.py")
sha256sums=('SKIP' 'SKIP')

package() {
	python setup.py build
	mkdir -p "${pkgdir}/usr/local/wavystats" "${pkgdir}/usr/bin"
	cp -dr --preserve=mode,timestamp build/exe.linux-x86_64-3.8/* "${pkgdir}/usr/local/wavystats/"
	ln -s "/usr/local/wavystats/wavystats" "${pkgdir}/usr/bin/wavystats"
}
