# TODO
# - use python-gdata?
# - dolphin (kde), nautilus (gnome), nemo (???), thunar (xfce) subpackages
# - if other DE .desktop added, fill them with OnlyShowIn fields
# - check over bundled libs -- rpm -qp --provides ..| grep ^lib | sed -e 's,(.*,,' | sort -u | sed -e 's,^,/usr/lib64/,' | xargs rpm -qf | sort -u
#   Qt4, flac, x11*, expat, gst*, vorbis, orc
#
# Conditional build:
%bcond_without	mate	# build MATE package (caja integration)

Summary:	Insync - Your Google Docs backup and sync tool
Name:		insync
Version:	1.0.28.31731
Release:	0.7
License:	?
Group:		X11/Applications
# DownloadUrl: https://www.insynchq.com/linux
Source0:	http://s.insynchq.com/builds/%{name}-%{version}-1.i686.rpm
# NoSource0-md5:	5459d29ce0e5b7fb7aae4c5ca52981b3
NoSource:	0
Source1:	http://s.insynchq.com/builds/%{name}-%{version}-1.x86_64.rpm
# NoSource1-md5:	aab26fd8635e7151e09872a93f02af65
NoSource:	0
Source2:	http://s.insynchq.com/builds/%{name}-caja_%{version}_all.deb
# NoSource2-md5:	f3d9371544be8f1810de720f8ded05e7
NoSource:	2
URL:		https://www.insynchq.com/linux
BuildRequires:	rpm-utils
BuildRequires:	sed >= 4.0
Requires:	glib2
Requires:	gtk-update-icon-cache
Requires:	gvfs
#Requires:	nautilus-python
#Requires:	python-gevent
#Requires:	xdotool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir			%{_prefix}/lib/%{name}
%define		caja_pyextdir	/usr/share/caja-python/extensions

# a zip and executable at the same time -- may not strip
%define		_noautostrip	.*/library.zip\\\\|.*/insync\\\\|.*/py\\\\|*/insync-headless

# bunch of Python symbols
%define		skip_post_check_so libpyglib-gi-2.0-python2.7.so.0

# Filter GLIBC_PRIVATE Requires
%define		_noautoreq	(GLIBC_PRIVATE)

# we don't want these to be provided as system libraries
%define		_noautoprov		libcrypto.so.1.0.0 libz.so.1 libsqlite3.so.0 libreadline.so.6 libdbus-glib-1.so.2 libgio-2.0.so.0 libICE.so.6 libSM.so.6

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
SOURCE1=%{SOURCE0}
%endif
%ifarch %{x8664}
SOURCE1=%{SOURCE1}
%endif

rpm2cpio $SOURCE1 | cpio -i -d

%if %{with mate}
ar x %{SOURCE2}
tar xzf data.tar.gz
%endif

mv usr/bin .
mv usr/lib*/insync lib
mv usr/share/icons .

%if %{with mate}
mv usr/share/applications/*.desktop .
cp -p insync.desktop insync-mate.desktop
mv usr/share/caja-python .
%endif

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
cmp lib/{insync,library.zip}
ln -sf insync lib/library.zip
# symlink other identical binaries
cmp lib/{insync,insync-headless}
ln -sf insync lib/insync-headless
cmp lib/{insync,py}
ln -sf insync lib/py

%{__sed} -i -e '
	1s,/bin/bash,/bin/sh,
s,%{_prefix}/lib/insync,%{_appdir},
' bin/%{name}*

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_iconsdir},%{_desktopdir},%{caja_pyextdir}}

cp -a lib/* $RPM_BUILD_ROOT%{_appdir}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a icons/* $RPM_BUILD_ROOT%{_iconsdir}

%if %{with mate}
cp -p insync-mate.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a caja-python/extensions/*  $RPM_BUILD_ROOT%{caja_pyextdir}
%endif

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
%attr(755,root,root) %{_appdir}/insync-headless
%attr(755,root,root) %{_appdir}/py
%{_appdir}/library.zip

%{_appdir}/gdata-2.0.15-py2.7.egg
%{_appdir}/isyncd.commonlib-0.7.0-py2.7.egg
%{_appdir}/isyncd.deskcore-1.0.27-py2.7.egg
%{_appdir}/isyncd.irp-0.1.0-py2.7.egg

%dir %{_appdir}/gevent-0.13.8-py*.egg
%{_appdir}/gevent-0.13.8-py*.egg/EGG-INFO
%dir %{_appdir}/gevent-0.13.8-py*.egg/gevent
%{_appdir}/gevent-0.13.8-py*.egg/gevent/*.py[co]
%attr(755,root,root) %{_appdir}/gevent-0.13.8-py*.egg/gevent/core.so

%dir %{_appdir}/greenlet-0.4.0-py*.egg
%{_appdir}/greenlet-0.4.0-py*.egg/EGG-INFO
%{_appdir}/greenlet-0.4.0-py*.egg/greenlet.py[co]
%attr(755,root,root) %{_appdir}/greenlet-0.4.0-py*.egg/greenlet.so

%dir %{_appdir}/faulthandler-2.1-py*.egg
%{_appdir}/faulthandler-2.1-py*.egg/EGG-INFO
%{_appdir}/faulthandler-2.1-py*.egg/*.py[co]
%attr(755,root,root) %{_appdir}/faulthandler-2.1-py*.egg/faulthandler.so

%dir %{_appdir}/notify2-0.3-py*.egg
%{_appdir}/notify2-0.3-py*.egg/notify2.py[co]
%{_appdir}/notify2-0.3-py*.egg/EGG-INFO

%dir %{_appdir}/pycrypto-2.6-py*.egg
%{_appdir}/pycrypto-2.6-py*.egg/Crypto
%{_appdir}/pycrypto-2.6-py*.egg/EGG-INFO

%dir %{_appdir}/python_ntlm-1.0.1-py*.egg
%{_appdir}/python_ntlm-1.0.1-py*.egg/ntlm
%{_appdir}/python_ntlm-1.0.1-py*.egg/EGG-INFO

%dir %{_appdir}/raven-3.1.0-py*.egg
%{_appdir}/raven-3.1.0-py*.egg/raven
%{_appdir}/raven-3.1.0-py*.egg/EGG-INFO

%{_iconsdir}/hicolor/*/apps/insync.svg
%{_iconsdir}/hicolor/*/mimetypes/application-vnd.insync.link.drive.*.png
%{_iconsdir}/hicolor/*/mimetypes/gd*.png
%{_iconsdir}/hicolor/*/places/insync-folder.png
%{_iconsdir}/hicolor/*/status/insync*.png

# wtf. resolve later
%dir %{_iconsdir}/hicolor/*/status/48x48
%{_iconsdir}/hicolor/*/status/48x48/insync-*.png

%if %{with mate}
%files -n caja-insync
%defattr(644,root,root,755)
%{_desktopdir}/insync-mate.desktop
%{caja_pyextdir}/insync-caja-plugin.py
#%dir %{caja_pyextdir}/libgio
#%{caja_pyextdir}/libgio/__init__.py

# FIXME
%dir %{caja_pyextdir}
%dir %{_datadir}/caja-python
%endif
