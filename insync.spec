# TODO
# - use python-gdata?
# - todo, gnome, cinnamon, kde subpackages
#   https://forums.insynchq.com/discussion/1437/insync-for-linux-beta-4-0-9-19
# - if other DE .desktop added, fill them with OnlyShowIn fields
# - check over bundled libs -- rpm -qp --provides ..| grep ^lib | sed -e 's,(.*,,' | sort -u | sed -e 's,^,/usr/lib64/,' | xargs rpm -qf | sort -u
#   Qt4, flac, x11*, expat, gst*, vorbis, orc
Summary:	Insync - Your Google Docs backup and sync tool
Name:		insync
Version:	0.10.5
Release:	0.5
License:	?
Group:		X11/Applications
# DownloadUrl: https://www.insynchq.com/linux
Source0:	http://s.insynchq.com/builds/%{name}-beta_%{version}_i386.deb
# NoSource0-md5:	1b5f38aa68c8495d51c83d92202b9ce6
NoSource:	0
Source1:	http://s.insynchq.com/builds/%{name}-beta_%{version}_amd64.deb
# NoSource1-md5:	0397e2edafc3391179c9762254d95789
NoSource:	0
Source2:	http://s.insynchq.com/builds/%{name}-beta-mate_%{version}_i386.deb
# NoSource2-md5:	f6297b2109d2064c8ad95055e5690f66
NoSource:	2
Source3:	http://s.insynchq.com/builds/%{name}-beta-mate_%{version}_amd64.deb
# NoSource3-md5:	5d13065677de9d60eec8050efd5cce5b
NoSource:	2
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

# bunch of Python symbols
%define		skip_post_check_so libpyglib-gi-2.0-python2.7.so.0

# Filter GLIBC_PRIVATE Requires
%define		_noautoreq	(GLIBC_PRIVATE)

# we don't want these to be provided as system libraries
%define		_noautoprov		libcrypto.so.1.0.0 libz.so.1 libsqlite3.so.0 libreadline.so.6 libdbus-glib-1.so.2 libgio-2.0.so.0 libICE.so.6

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
SOURCE2=%{SOURCE2}
%endif
%ifarch %{x8664}
SOURCE1=%{SOURCE1}
SOURCE2=%{SOURCE3}
%endif
%if 0
rpm2cpio $SOURCE | cpio -i -d
%else
ar x $SOURCE1
tar xzf data.tar.gz
ar x $SOURCE2
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
#%{_iconsdir}/hicolor/*/emblems/*.png
%dir %{_iconsdir}/insync
%{_iconsdir}/insync/icons
#%{_iconsdir}/insync/Francesco-icons

%{_appdir}/res
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

%files -n caja-insync
%defattr(644,root,root,755)
%{_desktopdir}/insync-mate.desktop
%{caja_pyextdir}/insync-caja-plugin.py
#%dir %{caja_pyextdir}/libgio
#%{caja_pyextdir}/libgio/__init__.py

# FIXME
%dir %{caja_pyextdir}
%dir %{_datadir}/caja-python
