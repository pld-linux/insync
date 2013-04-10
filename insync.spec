# TODO
# - use python-gdata?
# - todo, gnome, cinnamon, kde subpackages
#   https://forums.insynchq.com/discussion/1437/insync-for-linux-beta-4-0-9-19
# - if other DE .desktop added, fill them with OnlyShowIn fields
Summary:	Insync - Your Google Docs backup and sync tool
Name:		insync
Version:	0.9.41
Release:	0.4
License:	?
Group:		X11/Applications
# DownloadUrl: https://www.insynchq.com/linux
Source0:	http://s.insynchq.com/builds/%{name}-beta-mate_%{version}_i386.deb
# NoSource0-md5:	68299418714c494a7d80f6e1c2bc3c0d
NoSource:	0
Source1:	http://s.insynchq.com/builds/%{name}-beta-mate_%{version}_amd64.deb
# NoSource1-md5:	8126bb7915b77a88cc0f098d2398aeff
NoSource:	0
URL:		https://www.insynchq.com/
BuildRequires:	rpm-utils
BuildRequires:	sed >= 4.0
Requires:	glib2
Requires:	gtk-update-icon-cache
Requires:	gvfs
Requires:	nautilus-python
Requires:	python-gevent
Requires:	xdotool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir			%{_libdir}/%{name}
%define		caja_pyextdir	/usr/share/caja-python/extensions

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

%package -n caja-insync
Summary:	Insync context menu and emblems for Caja
Requires:	%{name} = %{version}-%{release}
Requires:	mate-file-manager

%description -n caja-insync
Insync context menu and emblems for Mate File Manager (Caja).

%prep
%setup -qcT
%ifarch %{ix86}
SOURCE=%{SOURCE0}
%endif
%ifarch %{x8664}
SOURCE=%{SOURCE1}
%endif
%if 0
rpm2cpio $SOURCE | cpio -i -d
%else
ar x $SOURCE
tar xzf data.tar.gz
%endif

mv usr/bin .
mv usr/lib/insync lib
mv usr/share/icons .

# mate
mv usr/share/applications/*.desktop .
cp -p insync.desktop insync-mate.desktop
mv usr/share/caja-python .

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
cmp lib/{insync,library.zip}
ln -sf insync lib/library.zip

%{__sed} -i -e '
	1s,/bin/bash,/bin/sh,
s,%{_prefix}/lib/insync,%{_appdir},
' bin/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_iconsdir},%{_desktopdir},%{caja_pyextdir}}

cp -a lib/* $RPM_BUILD_ROOT%{_appdir}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a icons/* $RPM_BUILD_ROOT%{_iconsdir}

# mate
cp -p insync-mate.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a caja-python/extensions/*  $RPM_BUILD_ROOT%{caja_pyextdir}

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

%files -n caja-insync
%defattr(644,root,root,755)
%{_desktopdir}/insync-mate.desktop
%{caja_pyextdir}/insync-caja-plugin.py
%dir %{caja_pyextdir}/libgio
%{caja_pyextdir}/libgio/__init__.py

# FIXME
%dir %{caja_pyextdir}
%dir /usr/share/caja-python
