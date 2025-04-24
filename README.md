# dependencies-comparator

Compare two sets of pom.xml - dependencies in dependencyManagement section and their version. 
Read files locally or download then from url. 
Print result in csv file or on console.


### Example:

pom-one.xml
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.dependneciescomparator</groupId>
    <artifactId>reference</artifactId>
    <version>1.0.0</version>

    <properties>
        <com.sample.dependency.version>1.0.0</com.sample.dependency.version>
        <com.another.sample.dependency.version>1.0.0</com.another.sample.dependency.version>
        <com.yet-another.sample.dependency.version>1.0.0</com.yet-another.sample.dependency.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.dependneciescomparator</groupId>
                <artifactId>sample</artifactId>
                <version>${com.sample.dependency.version}</version>
            </dependency>
            <dependency>
                <groupId>com.dependneciescomparator</groupId>
                <artifactId>another-sample</artifactId>
                <version>${com.another.sample.dependency.version}</version>
            </dependency>
            <dependency>
                <groupId>com.dependneciescomparator</groupId>
                <artifactId>yet-another-sample</artifactId>
                <version>${com.yet-another.sample.dependency.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

pom-two.xml
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.dependneciescomparator</groupId>
    <artifactId>comapredto</artifactId>
    <version>1.0.0</version>

    <properties>
        <com.sample.dependency.version>2.0.0</com.sample.dependency.version>
        <com.another.sample.dependency.version>1.0.0</com.another.sample.dependency.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.dependneciescomparator</groupId>
                <artifactId>sample</artifactId>
                <version>${com.sample.dependency.version}</version>
            </dependency>
            <dependency>
                <groupId>com.dependneciescomparator</groupId>
                <artifactId>another-sample</artifactId>
                <version>${com.another.sample.dependency.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

config.json
```json
{
  "printer": "CSV",
  "providers": [
    {
      "name": "CURRENT_DIR",
      "path": "./",
      "strategy": "FILE"
    },
    {
      "name": "CENTRAL_MAVEN",
      "path": "https://repo1.maven.org/maven2/",
      "strategy": "HTTP"
    }
  ],
  "references": [
    {
      "path": "./pom-one.xml",
      "provider": "CURRENT_DIR"
    }
  ],
  "compared_to": [
    {
      "path": "./pom-two.xml",
      "provider": "CURRENT_DIR"
    }
  ]
}
```
run:

python main.py

CSV:
```csv
reference;operator;compared to
reference:com.dependneciescomparator:sample:1.0.0;ne;comapredto:com.dependneciescomparator:sample:2.0.0
reference:com.dependneciescomparator:another-sample:1.0.0;eq;comapredto:com.dependneciescomparator:another-sample:1.0.0
reference:com.dependneciescomparator:yet-another-sample:1.0.0;not found;
```

Console:
```console
[{'reference': 'reference:com.dependneciescomparator:sample:1.0.0', 'operator': 'ne', 'compared_to': 'comapredto:com.dependneciescomparator:sample:2.0.0'}, {'reference': 'reference:com.dependneciescomparator:another-sample:1.0.0', 'operator': 'eq', 'compared_to': 'comapredto:com.dependneciescomparator:another-sample:1.0.0'}, {'reference': 'reference:com.dependneciescomparator:yet-another-sample:1.0.0', 'operator': 'not found', 'compared_to': ''}]
```