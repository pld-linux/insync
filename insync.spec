# TODO
# - use python-gdata?
# - todo, gnome, cinnamon, kde subpackages
#   https://forums.insynchq.com/discussion/1437/insync-for-linux-beta-4-0-9-19
Summary:	Insync - Your Google Docs backup and sync tool
Name:		insync
Version:	0.9.41
Release:	0.1
License:	?
Group:		Applications
# DownloadUrl: https://www.insynchq.com/linux
Source0:	http://s.insynchq.com/builds/%{name}-beta-gnome-cinnamon-common-%{version}-1.i686.rpm
# NoSource0-md5:	7a30c504db7ecf0c4c3c330dc9c4cb5e
NoSource:	0
Source1:	http://s.insynchq.com/builds/%{name}-beta-gnome-cinnamon-common-%{version}-1.x86_64.rpm
# NoSource1-md5:	6de980f9a98d7ed729c6825c05433430
NoSource:	0
URL:		https://www.insynchq.com/
BuildRequires:	rpm-utils
Requires:	glib2
Requires:	gtk-update-icon-cache
Requires:	gvfs
Requires:	nautilus-python
Requires:	python-gevent
Requires:	xdotool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir			%{_libdir}/%{name}
%define		nautilus_pyextdir	/usr/share/nautilus-python/extensions

# a zip and executable at the same time
%define		_noautostrip	.*/library.zip\\|.*/insync\\|.*/py

# Filter GLIBC_PRIVATE Requires
%define		_noautoreq	(GLIBC_PRIVATE)

# we don't want these to be provided as system libraries
%define		_noautoprov		libcrypto.so.1.0.0 libz.so.1 libsqlite3.so.0 libreadline.so.6
# and as we don't provide them, don't require either
%define		_noautoreq		%{_noautoprov}

%description
Insync is Google Drive for business and power users that sync and
supports multiple accounts and offline Google Docs editing using local
applications.

%prep
%setup -qcT
%ifarch %{ix86}
SOURCE=%{SOURCE0}
%endif
%ifarch %{x8664}
SOURCE=%{SOURCE1}
%endif
rpm2cpio $SOURCE | cpio -i -d

mv usr/bin .
mv usr/lib/insync lib
mv usr/share/icons .

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
cmp lib/{insync,library.zip}
ln -sf insync lib/library.zip

%{__sed} -i -e '
	1s,/bin/bash,/bin/sh,
	s,/usr/lib/insync,%{_appdir},
' bin/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_iconsdir},%{_desktopdir},%{nautilus_pyextdir}}

cp -a lib/* $RPM_BUILD_ROOT%{_appdir}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a icons/* $RPM_BUILD_ROOT%{_iconsdir}

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc README.txt COMMAND_LINE_HELP.txt
%attr(755,root,root) %{_bindir}/insync*
%dir %{_appdir}
%attr(755,root,root) %{_appdir}/*.so*
%attr(755,root,root) %{_appdir}/insync
%{_appdir}/library.zip
%{_iconsdir}/hicolor/*/emblems/*.png
%dir %{_iconsdir}/insync
%{_iconsdir}/insync/icons
%{_iconsdir}/insync/Francesco-icons

%dir %{_libdir}/insync/gevent-0.13.8-py*.egg
%{_libdir}/insync/gevent-0.13.8-py*.egg/EGG-INFO
%dir %{_libdir}/insync/gevent-0.13.8-py*.egg/gevent
%{_libdir}/insync/gevent-0.13.8-py*.egg/gevent/*.py[co]
%attr(755,root,root) %{_libdir}/insync/gevent-0.13.8-py*.egg/gevent/core.so

%dir %{_libdir}/insync/greenlet-0.4.0-py*.egg
%{_libdir}/insync/greenlet-0.4.0-py*.egg/EGG-INFO
%{_libdir}/insync/greenlet-0.4.0-py*.egg/greenlet.py[co]
%attr(755,root,root) %{_libdir}/insync/greenlet-0.4.0-py*.egg/greenlet.so
