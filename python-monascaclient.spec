%global pypi_name monascaclient
%global cliname   monasca

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Python client for monasca REST API. Includes python library for monasca API \
and Command Line Interface (CLI) library.

Name:           python-%{pypi_name}
Version:        1.10.1
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

%package -n     python2-%{pypi_name}
Summary:        Python client for monasca REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
# Required for tests
BuildRequires:  python2-os-testr
BuildRequires:  python2-osc-lib
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-oslotest
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python2-pyyaml
%else
BuildRequires:  PyYAML
%endif

Requires:       python2-babel
Requires:       python2-iso8601
Requires:       python2-osc-lib >= 1.8.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-pbr
Requires:       python2-prettytable
Requires:       python2-six >= 1.10.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python2-pyyaml >= 3.10
%else
Requires:       PyYAML >= 3.10
%endif

%description -n python2-%{pypi_name}
%{common_desc}

%package -n     python2-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python2-%{pypi_name} = %{version}-%{release}
Requires:  python2-mock
Requires:  python2-testrepository
Requires:  python2-testscenarios
Requires:  python2-testtools

%description -n python2-%{pypi_name}-tests
%{common_desc}

This package contains the unit tests

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Python client for monasca REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
# Required for tests
BuildRequires:  python3-os-testr
BuildRequires:  python3-osc-lib
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
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
Requires:       python3-PyYAML >= 3.10
Requires:       python3-six >= 1.10.0

%description -n python3-%{pypi_name}
%{common_desc}

%package -n     python3-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python3-%{pypi_name} = %{version}-%{release}
Requires:  python3-mock
Requires:  python3-testrepository
Requires:  python3-testscenarios
Requires:  python3-testtools

%description -n python3-%{pypi_name}-tests
%{common_desc}

This package contains the unit tests
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{cliname} %{buildroot}%{_bindir}/%{cliname}-%{python3_version}
ln -s ./%{cliname}-%{python3_version} %{buildroot}%{_bindir}/%{cliname}-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/%{cliname} %{buildroot}%{_bindir}/%{cliname}-%{python2_version}
ln -s %{_bindir}/%{cliname}-%{python2_version} %{buildroot}%{_bindir}/%{cliname}-2
ln -s %{_bindir}/%{cliname}-2 %{buildroot}%{_bindir}/%{cliname}

rm -f %{buildroot}%{_datarootdir}/monasca.bash_completion

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/%{cliname}
%{_bindir}/%{cliname}-2
%{_bindir}/%{cliname}-%{python2_version}
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/%{cliname}-%{python3_version}
%{_bindir}/%{cliname}-3
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests
%endif


%changelog
* Thu Oct 24 2019 RDO <dev@lists.rdoproject.org> 1.10.1-1
- Update to 1.10.1

* Tue Feb 13 2018 RDO <dev@lists.rdoproject.org> 1.10.0-1
- Update to 1.10.0

