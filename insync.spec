# TODO
# - use python-gdata?
Summary:	Insync - Your Google Docs backup and sync tool
Name:		insync
Version:	0.1
Release:	0.5
License:	?
Group:		Applications
Source0:	http://s.insynchq.com/builds/%{name}-linux-beta1-py27.tar.bz2
# NoSource0-md5:	6f80f20423d2531f2efb27bee7ea6455
NoSource:	0
URL:		https://www.insynchq.com/
Requires:	glib2
Requires:	gtk-update-icon-cache
Requires:	gvfs
Requires:	nautilus-python
Requires:	python-gevent
Requires:	xdotool
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir			%{_prefix}/lib/%{name}

%description
Insync is Google Drive for business and power users that sync and
supports multiple accounts and offline Google Docs editing using local
applications.

%prep
%setup -qc
%{__tar} xf insync-linux-metapackage.tar

cat > %{name}.sh <<EOF
#!%{__python}
cd %{_appdir}
exec %{__python} insync.pyc "$@"
EOF
cat insync-headless <<EOF
#!/bin/sh
exec %{name} --headless "$@"
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_iconsdir}/{insync,hicolor/64x64/emblems}}

cp -a insync.pyc isyncd gdata atom py $RPM_BUILD_ROOT%{_appdir}
cp -a icons $RPM_BUILD_ROOT%{_iconsdir}/insync
cp -a emblems/*.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/64x64/emblems
install -p %{name}{,-{get,headless,set}} $RPM_BUILD_ROOT%{_bindir}

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt COMMAND_LINE_HELP.txt
%attr(755,root,root) %{_bindir}/insync*
%{_appdir}
%{_iconsdir}/hicolor/*/emblems/*.png
%dir %{_iconsdir}/insync
%dir %{_iconsdir}/insync/icons
%{_iconsdir}/insync/icons/*.png
%{_iconsdir}/insync/icons/*.svg
