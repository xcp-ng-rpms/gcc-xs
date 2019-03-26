%define _name gcc
Name: %{_name}-xs
Summary: GCC with modifications
Version: 7.3.0
Release: 1.0.0%{dist}

License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL: http://gcc.gnu.org
Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/%{_name}/archive?at=gcc-7_3_0-release&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: bison flex zlib-devel
BuildRequires: gmp-devel libmpc-devel mpfr-devel
# For multilib build
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so

%description
The GNU Compiler Collection version %{version} with some modifications.
Suitable for compiling C and C++ code.


%prep
%autosetup -p1


%build
# Install into a separate location to avoid affecting the system compiler.
%define prefix /opt/xensource/gcc

# Building out of tree is recommended for GCC
mkdir ../build
cd ../build

# These configure options were cobbled together from Arch Linux & Fedora.
# TODO enable isl for more optimizations
../%{name}-%{version}/configure \
    --prefix=%{prefix} \
    --enable-languages=c,c++ \
    --enable-shared \
    --enable-threads=posix \
    --enable-libmpx \
    --with-system-zlib \
    --without-isl \
    --enable-__cxa_atexit \
    --disable-libunwind-exceptions \
    --enable-clocale=gnu \
    --disable-libstdcxx-pch \
    --disable-libssp \
    --enable-gnu-unique-object \
    --enable-linker-build-id \
    --enable-lto \
    --enable-plugin \
    --with-linker-hash-style=gnu \
    --enable-gnu-indirect-function \
    --enable-multilib \
    --disable-werror \
    --enable-checking=release \
    --enable-default-pie \
    --enable-default-ssp \
    --enable-version-specific-runtime-libs \
    --with-tune=generic \
    --with-arch_32=x86-64
make %{?_smp_mflags}


%install
cd ../build

make install DESTDIR=%{buildroot}

# Remove useless libtool files
find %{buildroot}%{prefix} -name '*.la' -delete

# GCC installs libgcc_s.so into a location that isn't in its search path
# so move it into a more useful location.
mv %{buildroot}%{prefix}/lib/gcc/x86_64-pc-linux-gnu/lib/libgcc_s.so.1 %{buildroot}%{prefix}/lib/gcc/x86_64-pc-linux-gnu/%{version}/32/libgcc_s.so
rm -rf %{buildroot}%{prefix}/lib/gcc/x86_64-pc-linux-gnu/lib
mv %{buildroot}%{prefix}/lib/gcc/x86_64-pc-linux-gnu/lib64/libgcc_s.so.1 %{buildroot}%{prefix}/lib/gcc/x86_64-pc-linux-gnu/%{version}/libgcc_s.so
rm -rf %{buildroot}%{prefix}/lib/gcc/x86_64-pc-linux-gnu/lib64


%files
/opt/xensource/*


%changelog
* Thu Feb 22 2018 Andrew Cooper <andrew.cooper3@citrix.com> - 7.3.0-1.0.0
- Upadte to 7.3.0.

* Fri Dec 15 2017 Ross Lagerwall <ross.lagerwall@citrix.com> - 7.2.0-1.0.0
- Initial packaging.
