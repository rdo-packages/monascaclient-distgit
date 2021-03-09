%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name monascaclient
%global cliname   monasca

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Python client for monasca REST API. Includes python library for monasca API \
and Command Line Interface (CLI) library.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Python client for monasca REST API

License:        ASL 2.0
URL:            https://github.com/openstack/python-monascaclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Python client for monasca REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
# Required for tests
BuildRequires:  python3-stestr
BuildRequires:  python3-osc-lib
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslotest
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools

BuildRequires:  python3-PyYAML

Requires:       python3-babel
Requires:       python3-iso8601
Requires:       python3-osc-lib >= 1.8.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-pbr
Requires:       python3-prettytable

Requires:       python3-yaml >= 3.12

%description -n python3-%{pypi_name}
%{common_desc}

%package -n     python3-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python3-%{pypi_name} = %{version}-%{release}
Requires:  python3-mock
Requires:  python3-stestr
Requires:  python3-testscenarios
Requires:  python3-testtools

%description -n python3-%{pypi_name}-tests
%{common_desc}

This package contains the unit tests

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cliname} %{buildroot}%{_bindir}/%{cliname}-3

rm -f %{buildroot}%{_datarootdir}/monasca.bash_completion

%check
PYTHON=%{__python3} stestr-3 run

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*-py%{python3_version}.egg-info
%{_bindir}/%{cliname}
%{_bindir}/%{cliname}-3
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests

%changelog
