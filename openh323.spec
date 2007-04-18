# TODO:
# - separate plugins to subpackages
# - gsm-amr plugin (using system amrnb if possible)
# - use system libilbc or at least use optflags for plugins/audio/iLBC
#
%define	fver	%(echo %{version} | tr . _)
Summary:	OpenH323 Library
Summary(pl.UTF-8):	Biblioteka OpenH323
Name:		openh323
Version:	1.18.0
Release:	6
License:	MPL 1.0
Group:		Libraries
#Source0:	http://www.openh323.org/bin/%{name}_%{version}.tar.gz
Source0:	http://dl.sourceforge.net/openh323/%{name}-v%{fver}-src-tar.gz
# Source0-md5:	d7043ba34b5038f0113b099ede0884fb
#Source0:	http://www.seconix.com/%{name}-%{version}.tar.gz
Patch0:		%{name}-mak_files.patch
Patch1:		%{name}-asnparser.patch
Patch2:		%{name}-lib.patch
Patch3:		%{name}-system-libs.patch
Patch4:		%{name}-ffmpeg.patch
Patch5:		%{name}-configure_fix.patch
Patch6:		%{name}-install64.patch
Patch7:		%{name}-inc.patch
URL:		http://www.openh323.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	ffmpeg-devel >= 0.4.6
BuildRequires:	libgsm-devel >= 1.0.10
BuildRequires:	libstdc++-devel
BuildRequires:	lpc10-devel >= 1.5
BuildRequires:	pwlib-devel >= 1.10.0
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel >= 1:1.1.5
%requires_eq	pwlib
Requires:	pwlib >= 1.10.0
Requires:	speex >= 1:1.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenH323 project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%description -l pl.UTF-8
Celem projektu OpenH323 jest stworzenie w pełni funkcjonalnej i
wyposażonej implementacji protokołu telekonferencyjnego ITU H.323,
który może być używany przez użytkowników prywatnych i komercyjnych
bez opłat.

%package devel
Summary:	OpenH323 development files
Summary(pl.UTF-8):	Pliki dla developerów OpenH323
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ffmpeg-devel
Requires:	pwlib-devel >= 1.10.0

%description devel
Header files and libraries for developing applications that use
OpenH323.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do rozwoju aplikacji
używających OpenH323.

%package static
Summary:	OpenH323 static libraries
Summary(pl.UTF-8):	Biblioteki statyczne OpenH323
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OpenH323 static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenH323.

%prep
%setup -q -n %{name}_v%{fver}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%if "%{_lib}" == "lib64"
%patch6 -p1
%endif
%patch7 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPENH323DIR=`pwd`; export OPENH323DIR
OPENH323_BUILD="yes"; export OPENH323_BUILD
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--enable-localspeex=no \
	--enable-plugins

%{__make} %{?debug:debugshared}%{!?debug:optshared} \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

%{__make} -C samples/simple %{?debug:debugshared}%{!?debug:optshared} \
	CC="%{__cc}" \
	CPLUS=%{__cxx} \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}

# using cp as install won't preserve links
cp -d %{_lib}/lib*.a $RPM_BUILD_ROOT%{_libdir}
install samples/simple/obj_*/simph323 $RPM_BUILD_ROOT%{_bindir}
install version.h $RPM_BUILD_ROOT%{_includedir}/%{name}
sed -i -e 's@\$(OPENH323DIR)/include@&/openh323@' $RPM_BUILD_ROOT%{_datadir}/openh323/openh323u.mak

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libopenh323.so.*.*.*
%dir %{_libdir}/pwlib/codecs
%dir %{_libdir}/pwlib/codecs/audio
%attr(755,root,root) %{_libdir}/pwlib/codecs/audio/*_pwplugin.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenh323.so
%{_includedir}/openh323
%{_datadir}/openh323

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenh323.a
