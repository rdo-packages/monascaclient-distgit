# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%global pypi_name monascaclient
%global cliname   monasca

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Python client for monasca REST API. Includes python library for monasca API \
and Command Line Interface (CLI) library.

Name:           python-%{pypi_name}
Version:        1.16.0
Release:        1%{?dist}
Summary:        Python client for monasca REST API

License:        ASL 2.0
URL:            https://github.com/openstack/python-monascaclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Python client for monasca REST API
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
# Required for tests
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-osc-lib
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  PyYAML
%else
BuildRequires:  python%{pyver}-PyYAML
%endif

Requires:       python%{pyver}-babel
Requires:       python%{pyver}-iso8601
Requires:       python%{pyver}-osc-lib >= 1.8.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-prettytable
Requires:       python%{pyver}-six >= 1.10.0

# Handle python2 exception
%if %{pyver} == 2
Requires:       PyYAML >= 3.10
%else
Requires:       python%{pyver}-PyYAML >= 3.10
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python%{pyver}-%{pypi_name} = %{version}-%{release}
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-stestr
Requires:  python%{pyver}-testscenarios
Requires:  python%{pyver}-testtools

%description -n python%{pyver}-%{pypi_name}-tests
%{common_desc}

This package contains the unit tests

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cliname} %{buildroot}%{_bindir}/%{cliname}-%{pyver}

rm -f %{buildroot}%{_datarootdir}/monasca.bash_completion

%check
PYTHON=%{pyver_bin} stestr-%{pyver} run

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/%{cliname}
%{_bindir}/%{cliname}-%{pyver}
%exclude %{pyver_sitelib}/%{pypi_name}/tests

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/%{pypi_name}/tests

%changelog
* Fri Sep 20 2019 RDO <dev@lists.rdoproject.org> 1.16.0-1
- Update to 1.16.0

