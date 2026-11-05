Name:		apache-commons-collections
Version:	3.2.2
Release:	1
Summary:	Interfaces and utilities that extend the Java Collections Framework
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-collections/
Source0:	https://archive.apache.org/dist/commons/collections/source/commons-collections-%{version}-src.tar.gz
Patch0:		java8-compat.patch
BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-collections --link %{name}

%description
Apache Commons Collections 3.2.2 adds bag, buffer, and map types on top
of the Java Collections Framework. Map.remove(Object, Object) is updated
to the Java 8 signature. Later 4.x releases are a different artifact.

%prep
%autosetup -n commons-collections-%{version}-src -p1
# Parent 39 is not the packaged commons-parent. A versionless antrun
# execution is bound to package and would try to build the test framework.
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def local(tag):
    return tag.split("}", 1)[-1]

tree = ET.parse("pom.xml")
root = tree.getroot()
for node in list(root):
    if local(node.tag) == "parent":
        root.remove(node)
tree.write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
