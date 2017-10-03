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
Version:        XXX
Release:        XXX
Summary:        Python client for monasca REST API

License:        ASL 2.0
URL:            https://github.com/openstack/python-monascaclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        Python client for monasca REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  git
# Required for tests
BuildRequires:  python-os-testr
BuildRequires:  python-osc-lib
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  PyYAML

Requires:       python-babel
Requires:       python-iso8601
Requires:       python-osc-lib >= 1.7.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-pbr
Requires:       python-prettytable
Requires:       PyYAML >= 3.10
Requires:       python-six >= 1.9.0

%description -n python2-%{pypi_name}
%{common_desc}

%package -n     python2-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python2-%{pypi_name} = %{version}-%{release}
Requires:  python-mock
Requires:  python-testrepository
Requires:  python-testscenarios
Requires:  python-testtools

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
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-pbr
Requires:       python3-prettytable
Requires:       python3-PyYAML >= 3.10
Requires:       python3-six >= 1.9.0

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
rm -f test-requirements.txt requirements.txt

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
