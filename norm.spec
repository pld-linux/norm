#
# Conditional build:
%bcond_without	java		# Java binding
%bcond_without	python		# Python binding
#
Summary:	NACK-Oriented Reliable Multicast library
Summary(pl.UTF-8):	Biblioteka NACK-Oriented Reliable Multicast
Name:		norm
# upstream changed versioning scheme 1.5r6 -> 1.5.7, but rpm says thay 1.5r6 > 1.5.8
# so let's delay switching to avoid epoch bumps until 1.6.x series
Version:	1.5r8
%define	fver	%(echo %{version} | tr r .)
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/USNavalResearchLaboratory/norm/releases
#Source0:	https://github.com/USNavalResearchLaboratory/norm/releases/download/v%{fver}/src-norm-with-protolib-%{fver}.tar.gz
Source0:	https://downloads.pf.itd.nrl.navy.mil/norm/src-%{name}-%{fver}.tgz
# Source0-md5:	6c4da91ea600643005297d8b6e8e1a04
Patch0:		%{name}-c++.patch
Patch1:		%{name}-link.patch
URL:		https://www.nrl.navy.mil/itd/ncs/products/norm
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libstdc++-devel
%{?with_python:BuildRequires:	python-devel >= 1:2.5}
BuildRequires:	waf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NACK-Oriented Reliable Multicast library.

%description -l pl.UTF-8
Biblioteka NACK-Oriented Reliable Multicast.

%package devel
Summary:	Header files for NORM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki NORM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for NORM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki NORM.

%package -n java-norm
Summary:	Java JNI bindings for NORM
Summary(pl.UTF-8):	Wiązania JNI Javy do biblioteki NORM
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jre

%description -n java-norm
Java JNI bindings for NORM C API.

%description -n java-norm -l pl.UTF-8
Wiązania JNI Javy do API C biblioteki NORM.

%package -n python-pynorm
Summary:	PyNORM - Python wrapper for NORM and Extras
Summary(pl.UTF-8):	PyNORM - interfejs Pythona do biblioteki NORM oraz dodatki
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-pynorm
PyNORM provides a thin wrapper around the NORM C API in the main
package. It also provides several additional modules in the extra
package to provide higher level usage of NORM.

%description -n python-pynorm -l pl.UTF-8
PyNORM udostępnia cienką warstwę obudowującą API C biblioteki NORM w
głównym pakiecie. Zawiera także kilka dodatkowych modułów w pakiecie
extra; pozwalają one na wykorzystanie NORM na wyższym poziomie.

%prep
%setup -q -n %{name}-%{fver}
%patch0 -p1
%patch1 -p1

%build
%waf configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	%{?with_java:--build-java} \
	%{?with_python:--build-python}

%waf \
	--verbose

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

%waf install \
	--destdir=$RPM_BUILD_ROOT \
	--verbose

cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}

%if %{with java}
install -D build/norm.jar $RPM_BUILD_ROOT%{_javadir}/norm.jar
%endif

%if %{with python}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-norm -p /sbin/ldconfig
%postun	-n java-norm -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.TXT README.TXT TODO.TXT VERSION.TXT
%attr(755,root,root) %{_libdir}/libnorm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnorm.so.1

%files devel
%defattr(644,root,root,755)
%doc NormSocketBindingNotes.txt doc/{NormDeveloperGuide.pdf,NormUserGuide.pdf,npcUsage.pdf}
%attr(755,root,root) %{_libdir}/libnorm.so
%{_includedir}/galois.h
%{_includedir}/norm*.h

%if %{with java}
%files -n java-norm
%defattr(644,root,root,755)
%doc README-Java.txt
%attr(755,root,root) %{_libdir}/libProtolibJni.so
%attr(755,root,root) %{_libdir}/libmil_navy_nrl_norm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmil_navy_nrl_norm.so.1
%attr(755,root,root) %{_libdir}/libmil_navy_nrl_norm.so
%{_javadir}/norm.jar
%endif

%if %{with python}
%files -n python-pynorm
%defattr(644,root,root,755)
%doc README-PyNorm.txt
%attr(755,root,root) %{py_sitedir}/protokit.so
%{py_sitescriptdir}/pynorm
%endif
