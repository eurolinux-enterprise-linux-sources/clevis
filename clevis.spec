%global _hardened_build 1

Name:           clevis
Version:        6
Release:        1%{?dist}
Summary:        Automated decryption framework

License:        GPLv3+
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  libjose-devel >= 8
BuildRequires:  libluksmeta-devel
BuildRequires:  libudisks2-devel
BuildRequires:  openssl-devel

BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig
BuildRequires:  systemd
BuildRequires:  dracut
BuildRequires:  tang >= 6
BuildRequires:  curl

Requires:       coreutils
Requires:       jose >= 8
Requires:       curl
Requires(pre):  shadow-utils

%description
Clevis is a framework for automated decryption. It allows you to encrypt
data using sophisticated unlocking policies which enable decryption to
occur automatically.

The clevis package provides basic encryption/decryption policy support.
Users can use this directly; but most commonly, it will be used as a
building block for other packages. For example, see the clevis-luks
and clevis-dracut packages for automatic root volume unlocking of LUKSv1
volumes during early boot.

%package luks
Summary:        LUKSv1 integration for clevis
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cryptsetup
Requires:       luksmeta

%description luks
LUKSv1 integration for clevis. This package allows you to bind a LUKSv1
volume to a clevis unlocking policy. For automated unlocking, an unlocker
will also be required. See, for example, clevis-dracut and clevis-udisks2.

%package dracut
Summary:        Dracut integration for clevis
Requires:       %{name}-luks%{?_isa} = %{version}-%{release}
Requires:       dracut-network
Requires:       nc

%description dracut
Automatically unlocks LUKSv1 block devices in early boot.

%package udisks2
Summary:        UDisks2/Storaged integration for clevis
Requires:       %{name}-luks%{?_isa} = %{version}-%{release}

%description udisks2
Automatically unlocks LUKSv1 block devices in desktop environments that
use UDisks2 or storaged (like GNOME).

%prep
%setup -q

%build
%configure --enable-user=clevis --enable-group=clevis
%make_build V=1

%install
%make_install

%check
desktop-file-validate \
  %{buildroot}/%{_sysconfdir}/xdg/autostart/%{name}-luks-udisks2.desktop
%make_build check

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_localstatedir}/cache/%{name} -s /sbin/nologin \
    -c "Clevis Decryption Framework unprivileged user" %{name}
exit 0

%files
%license COPYING
%{_bindir}/%{name}-decrypt-http
%{_bindir}/%{name}-decrypt-tang
%{_bindir}/%{name}-decrypt-sss
%{_bindir}/%{name}-decrypt
%{_bindir}/%{name}-encrypt-http
%{_bindir}/%{name}-encrypt-tang
%{_bindir}/%{name}-encrypt-sss
%{_bindir}/%{name}
%{_mandir}/man1/%{name}-encrypt-http.1*
%{_mandir}/man1/%{name}-encrypt-tang.1*
%{_mandir}/man1/%{name}-encrypt-sss.1*
%{_mandir}/man1/%{name}-decrypt.1*
%{_mandir}/man1/%{name}.1*

%files luks
%{_bindir}/%{name}-bind-luks
%{_mandir}/man1/%{name}-bind-luks.1*

%files dracut
%{_prefix}/lib/dracut/modules.d/60%{name}

%files udisks2
%{_sysconfdir}/xdg/autostart/%{name}-luks-udisks2.desktop
%attr(4755, root, root) %{_libexecdir}/%{name}-luks-udisks2

%changelog
* Tue Jun 27 2017 Nathaniel McCallum <npmccallum@redhat.com> - 6-1
- New upstream release
- Specify unprivileged user/group during configuration
- Move clevis user/group creation to base clevis package

* Mon Jun 26 2017 Nathaniel McCallum <npmccallum@redhat.com> - 5-1
- New upstream release
- Run clevis decryption from udisks2 under an unprivileged user
- Reenable udisks2 subpackage

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 4-1
- New upstream release
- Disable udisks2 subpackage

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 3-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 18 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2-1
- New upstream release

* Mon Nov 14 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1-1
- First release
