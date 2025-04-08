%define module mypy
# disabled tests on abf
%bcond_with test

Name:           python-mypy
Version:        1.15.0
Release:        1
Summary:        Optional static typing for Python
Group:          Development/Python
License:        MIT AND Python-2.0
URL:            https://github.com/python/mypy
Source:         https://files.pythonhosted.org/packages/source/m/mypy/%{module}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:	help2man
BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	python%{pyver}dist(typing-extensions)
BuildRequires:	python%{pyver}dist(mypy-extensions)
BuildRequires:	python%{pyver}dist(orjson)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(tomli)
BuildRequires:	python%{pyver}dist(types-psutil)
BuildRequires:	python%{pyver}dist(types-setuptools)
# for html doc generation
BuildRequires:	python%{pyver}dist(furo)
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(myst-parser)
BuildRequires:	python%{pyver}dist(sphinx-inline-tabs)
%if %{with test}
BuildRequires:  gcc-c++
BuildRequires:	python%{pyver}dist(attrs)
BuildRequires:	python%{pyver}dist(cfgv)
BuildRequires:	python%{pyver}dist(coverage)
BuildRequires:	python%{pyver}dist(distlib)
BuildRequires:	python%{pyver}dist(execnet)
BuildRequires:	python%{pyver}dist(filelock)
BuildRequires:	python%{pyver}dist(identify)
BuildRequires:	python%{pyver}dist(iniconfig)
BuildRequires:	python%{pyver}dist(lxml)
BuildRequires:	python%{pyver}dist(mypy-extensions)
BuildRequires:	python%{pyver}dist(nodeenv)
BuildRequires:	python%{pyver}dist(packaging)
BuildRequires:	python%{pyver}dist(platformdirs)
BuildRequires:	python%{pyver}dist(pluggy)
BuildRequires:	python%{pyver}dist(pre-commit)
BuildRequires:	python%{pyver}dist(psutil)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-cov)
BuildRequires:	python%{pyver}dist(pytest-forked)
BuildRequires:	python%{pyver}dist(pytest-xdist)
BuildRequires:	python%{pyver}dist(pyyaml)
BuildRequires:	python%{pyver}dist(tomli)
BuildRequires:	python%{pyver}dist(types-psutil)
BuildRequires:	python%{pyver}dist(types-setuptools)
BuildRequires:	python%{pyver}dist(typing-extensions)
BuildRequires:	python%{pyver}dist(virtualenv)
%endif


%description
Mypy is a static type checker for Python.

Type checkers help ensure that you're using variables and functions in your
code correctly. With mypy, add type hints (PEP 484) to your Python programs,
and mypy will warn you when you use those types incorrectly.

Python is a dynamic language, so usually you'll only see errors in your code
when you attempt to run it. Mypy is a static checker, so it finds bugs in
your programs without even running them!

%prep
%autosetup -n %{module}-%{version} -p1
# drop bundled egg-info
rm -rf *.egg-info/

sed -i '/env python3/d' ./mypy/stubgenc.py
sed -i '/env python3/d' ./mypy/stubgen.py


%build
%py_build
# docs
pushd docs
%make_build html
rm build/html/.buildinfo
popd

%install
%py3_install
rm -vrf %{buildroot}%{python3_sitelib}/mypy/{test,typeshed/tests}

# move html docs into buildroot
mkdir -p %{buildroot}%{_docdir}/%{name}/
mv -f docs/build/html %{buildroot}%{_docdir}/%{name}/

%if %{with test}
%check
export MYPYC_OPT_LEVEL=2
if [ $(getconf LONG_BIT) -ne 64 ]; then
  # https://github.com/python/mypy/issues/11148
  ignore+="not testSubclassSpecialize and not testMultiModuleSpecialize and "
fi

ignore+="not teststubtest and not testMathOps and not testFloatOps and not PEP561Suite"

%{__python} -m pytest -v tests/ -k "${ignore}"
%endif

%files
%license LICENSE
%doc README.md
%{_docdir}/%{name}/html
%{python_sitelib}/mypy
%{python_sitelib}/mypyc
%{python_sitelib}/mypy-%{version}.dist-info/
%{_bindir}/dmypy
%{_bindir}/mypy
%{_bindir}/mypyc
%{_bindir}/stubgen
%{_bindir}/stubtest
