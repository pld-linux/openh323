Summary:	OpenH323 Library
Name:		openh323
Version:	1.1pl1
Release:	2
License:	MPL
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www.openh323.org/bin/%{name}_%{version}.tar.gz
Patch0:		%{name}-mak_files.patch
Patch1:		%{name}-asnparser.patch
Patch2:		%{name}-no_samples.patch
URL:		http://www.openh323.org/
BuildRequires:	pwlib-devel
#BuildRequires:	pwlib-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description 
he OpenH323 project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%package devel
Summary:	OpenH323 development files
Summary(pl):	Pliki dla developerów OpenH323
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files and libraries for developing applications that use
OpenH323.

%description -l pl devel
Pliki nag³ówkowe i biblioteki konieczne do rozwoju aplikacji
u¿ywaj±cych OpenH323.

%package static
Summary:	OpenH323 static libraries
Summary(pl):	Biblioteki statyczne OpenH323
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
OpenH323 static libraries.

%description -l pl static
Biblioteki statyczne OpenH323.

%prep
%setup -qn %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPENH323DIR=`pwd`; export OPENH323DIR
OPENH323_BUILD="yes"; export OPENH323_BUILD
%{__make} %{?debug:debugshared}%{!?debug:optshared} \
		OPTCCFLAGS="%{!?debug:$RPM_OPT_FLAGS}"
%{__make} %{?debug:debugnoshared}%{!?debug:optnoshared} \
		OPTCCFLAGS="%{!?debug:$RPM_OPT_FLAGS}"

cd samples/simple
%{__make} %{?debug:debugshared}%{!?debug:optshared} \
		OPTCCFLAGS="%{!?debug:$RPM_OPT_FLAGS}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/openh323,%{_bindir},%{_datadir}/misc}

#using cp as install won't preserve links
cp -d lib/lib* $RPM_BUILD_ROOT%{_libdir}
install include/*.h $RPM_BUILD_ROOT%{_includedir}/openh323
install samples/simple/obj_linux_x86_?/simph323 $RPM_BUILD_ROOT%{_bindir}

sed -e's@\$(OPENH323DIR)/include@&/openh323@' < openh323u.mak \
	> $RPM_BUILD_ROOT%{_datadir}/misc/openh323u.mak

gzip -9nf *.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/misc/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
