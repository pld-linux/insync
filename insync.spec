# TODO
# - use python-gdata?
# - todo, gnome, cinnamon, kde subpackages
#   https://forums.insynchq.com/discussion/1437/insync-for-linux-beta-4-0-9-19
Summary:	Insync - Your Google Docs backup and sync tool
Name:		insync
Version:	0.9.19
Release:	0.5
License:	?
Group:		Applications
Source0:	http://s.insynchq.com/builds/%{name}-beta-gnome-cinnamon-common-%{version}-1.i686.rpm
# NoSource0-md5:	116de4a900ab811bcd1f8717d71a7733
NoSource:	0
Source1:	http://s.insynchq.com/builds/%{name}-beta-gnome-cinnamon-common-%{version}-1.x86_64.rpm
# NoSource1-md5:	1ba9d25692397460f380f6d743bfc91b
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
mv usr/share/applications/*.desktop .
mv usr/share/icons .
mv usr/share/nautilus-python .

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
ln -sf insync lib/library.zip
ln -sf insync lib/py

mv bin/%{name} %{name}.orig
cat > bin/%{name} <<'EOF'
#!/bin/sh
cd %{_appdir}
exec ./%{name} "$@"
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_iconsdir},%{_desktopdir},%{nautilus_pyextdir}}

cp -a lib/* $RPM_BUILD_ROOT%{_appdir}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a icons/* $RPM_BUILD_ROOT%{_iconsdir}
cp -p insync.desktop $RPM_BUILD_ROOT%{_desktopdir}
install -p nautilus-python/extensions/*  $RPM_BUILD_ROOT%{nautilus_pyextdir}

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
%attr(755,root,root) %{_appdir}/py
%{_appdir}/library.zip
%{_iconsdir}/hicolor/*/emblems/*.png
%dir %{_iconsdir}/insync
%dir %{_iconsdir}/insync/icons
%{_iconsdir}/insync/*.png
%{_iconsdir}/insync/icons/*.png
%{_iconsdir}/insync/icons/*.svg
%{_desktopdir}/insync.desktop
%{nautilus_pyextdir}/insync_plugin.py
