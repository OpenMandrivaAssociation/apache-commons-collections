%global base_name       collections
%global short_name      commons-%{base_name}

Name:           apache-%{short_name}
Version:        3.2.1
Release:        10
Summary:        Provides new interfaces, implementations and utilities for Java Collections
License:        ASL 2.0
Group:          Development/Java
URL:            http://commons.apache.org/%{base_name}/
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source6:        collections-tomcat5-build.xml

Patch0:         jakarta-%{short_name}-javadoc-nonet.patch
Patch4:         commons-collections-3.2-build_xml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils >= 0:1.7.5
BuildRequires: maven2
BuildRequires: maven-antrun-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-idea-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-plugin-bundle
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: ant
BuildRequires: saxon
BuildRequires: saxon-scripts
BuildRequires: apache-commons-parent
Requires:      java
Requires:      jpackage-utils >= 0:1.7.5
Requires(post): jpackage-utils >= 0:1.7.5
Requires(postun): jpackage-utils >= 0:1.7.5

Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}

%description
The introduction of the Collections API by Sun in JDK 1.2 has been a
boon to quick and effective Java programming. Ready access to powerful
data structures has accelerated development by reducing the need for
custom container classes around each core object. Most Java2 APIs are
significantly easier to use because of the Collections API.
However, there are certain holes left unfilled by Sun's
implementations, and the Jakarta-Commons Collections Component strives
to fulfill them. Among the features of this package are:
- special-purpose implementations of Lists and Maps for fast access
- adapter classes from Java1-style containers (arrays, enumerations) to
Java2-style collections.
- methods to test or create typical set-theory properties of collections
such as union, intersection, and closure.

%package testframework
Summary:        Testframework for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Provides:       jakarta-%{short_name}-testframework = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-testframework < %{version}-%{release}

%description testframework
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils >= 0:1.7.5
Provides:       jakarta-%{short_name}-javadoc = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-javadoc < %{version}-%{release}

%description javadoc
%{summary}.

%package tomcat5
Summary:        Jakarta Commons Collection dependency for Tomcat5
Group:          Development/Java
Provides:       jakarta-%{short_name}-tomcat5 = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-tomcat5 < %{version}-%{release}

%description tomcat5
A package that is specifically designed to fulfill to a Tomcat5 dependency.

%package testframework-javadoc
Summary:        Javadoc for %{name}-testframework
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Provides:       jakarta-%{short_name}-testframework-javadoc = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-testframework-javadoc < %{version}-%{release}

%description testframework-javadoc
%{summary}.

%prep

%setup -q -n %{short_name}-%{version}-src
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0 -p1
%patch4 -b .sav
cp %{SOURCE6} .

# Fix file eof
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' PROPOSAL.html
%{__sed} -i 's/\r//' RELEASE-NOTES.html
%{__sed} -i 's/\r//' README.txt
%{__sed} -i 's/\r//' NOTICE.txt

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp -Dmaven.repo.local=$MAVEN_REPO_LOCAL install javadoc:javadoc

export MAVEN_HOME_LOCAL=$(pwd)/.maven

ant tf.javadoc

# commons-collections-tomcat5
ant -f collections-tomcat5-build.xml

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}
install -m 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 target/%{short_name}-testframework-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-testframework-%{version}.jar

# tomcat5
install -m 644 collections-tomcat5/%{short_name}-tomcat5.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tomcat5-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|apache-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf target/site/apidocs

# testframework-javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
cp -pr build/docs/testframework/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
ln -s %{name}-testframework-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework 

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc PROPOSAL.html README.txt LICENSE.txt RELEASE-NOTES.html NOTICE.txt
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{short_name}-%{version}.jar
%{_javadir}/%{short_name}.jar

%files testframework
%defattr(-,root,root,-)
%{_javadir}/%{name}-testframework-%{version}.jar
%{_javadir}/%{name}-testframework.jar
%{_javadir}/%{short_name}-testframework-%{version}.jar
%{_javadir}/%{short_name}-testframework.jar

%files tomcat5
%defattr(-,root,root,-)
%{_javadir}/*-tomcat5*.jar
%doc LICENSE.txt NOTICE.txt

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files testframework-javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-testframework-%{version}
%{_javadocdir}/%{name}-testframework

